#!/usr/bin/env python3
"""
Job Discovery Module
Multi-source scanner that surfaces relevant construction PM roles as soon as
they're posted. Scores each job against your CV using the existing JobAnalyzer,
and optionally auto-generates application materials for top matches.

Usage:
    python3 scripts/job_discovery.py                  # one-shot scan
    python3 scripts/job_discovery.py --auto           # scan + autopilot on >=80% matches
    python3 scripts/job_discovery.py --daemon         # continuous polling
    python3 scripts/job_discovery.py --interval 30    # daemon, 30-min interval
    python3 scripts/job_discovery.py --reset          # clear seen-jobs dedup cache

Sources:
    - RSS feeds  (Indeed, ZipRecruiter, Craigslist, SimplyHired)
    - ATS APIs   (Greenhouse, Lever — public, no auth required)
    - Company career pages (HTML scraping)

Dependencies (optional — missing deps skip that source):
    pip install feedparser requests beautifulsoup4 pyyaml
"""

import argparse
import hashlib
import json
import re
import math
import subprocess
import sys
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from urllib.error import URLError
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen

try:
    from zoneinfo import ZoneInfo
    HAS_ZONEINFO = True
except ImportError:
    HAS_ZONEINFO = False

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required.  pip install pyyaml", file=sys.stderr)
    sys.exit(1)

try:
    import feedparser
    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

# ── Path constants ─────────────────────────────────────────────────────────────

REPO_ROOT   = Path(__file__).parent.parent
DATA_DIR    = REPO_ROOT / "data"
SCRIPTS_DIR = Path(__file__).parent
APPS_DIR    = REPO_ROOT / "applications"
ALERTS_DIR  = APPS_DIR / "job_alerts"

DEFAULT_CONFIG    = DATA_DIR / "discovery_config.yaml"
SEEN_JOBS_FILE    = DATA_DIR / "seen_jobs.yaml"
DISCOVERED_FILE   = DATA_DIR / "discovered_jobs.yaml"
METADATA_TOML     = REPO_ROOT / "metadata.toml"

# Add scripts dir so we can import from sibling scripts
sys.path.insert(0, str(SCRIPTS_DIR))
from analyze_job import JobAnalyzer, load_cv_keywords  # noqa: E402


# ── Data classes ───────────────────────────────────────────────────────────────

@dataclass
class RawJob:
    title: str
    company: str
    url: str
    location: str = ""
    posted_date: str = ""
    description: str = ""
    source: str = ""

    def url_hash(self) -> str:
        return hashlib.md5(self.url.encode()).hexdigest()[:12]


@dataclass
class ScoredJob:
    title: str
    company: str
    url: str
    location: str
    source: str
    score: float
    matched: List[str]
    missing: List[str]
    discovered_at: str = field(default_factory=lambda: datetime.now().isoformat())
    description: str = ""

    @classmethod
    def from_raw(cls, job: RawJob, score: float,
                 matched: List[str], missing: List[str]) -> "ScoredJob":
        return cls(
            title=job.title, company=job.company, url=job.url,
            location=job.location, source=job.source,
            score=score, matched=matched, missing=missing,
            description=job.description,
        )


# ── Main class ─────────────────────────────────────────────────────────────────

class JobDiscovery:
    def __init__(self, config_path: Path = DEFAULT_CONFIG):
        self.config = self._load_yaml(config_path, default={})
        cv_keywords = load_cv_keywords(str(METADATA_TOML))
        self.analyzer = JobAnalyzer(cv_keywords)
        self.seen_jobs: Dict = self._load_seen_jobs()

        search = self.config.get("search", {})
        # Precompute token lists for partial-token keyword matching
        self._search_kw: List[List[str]] = [
            re.findall(r"\b\w+\b", k.lower()) for k in search.get("keywords", [])
        ]
        self._exclude_kw = [k.lower() for k in search.get("exclude_keywords", [])]
        self._target_city = search.get("location", "Seattle, WA").split(",")[0].strip().lower()

    # ── Config & persistence ───────────────────────────────────────────────────

    @staticmethod
    def _load_yaml(path: Path, default=None):
        if not path.exists():
            return default if default is not None else {}
        with open(path) as f:
            return yaml.safe_load(f) or (default if default is not None else {})

    def _load_seen_jobs(self) -> Dict:
        data = self._load_yaml(SEEN_JOBS_FILE, default={})
        # Strip YAML comments header (returns None/str for comment-only files)
        return data if isinstance(data, dict) else {}

    def _save_seen_jobs(self):
        DATA_DIR.mkdir(exist_ok=True)
        with open(SEEN_JOBS_FILE, "w") as f:
            f.write("# seen_jobs.yaml — auto-generated, do not edit manually\n")
            yaml.dump(self.seen_jobs, f, default_flow_style=False, allow_unicode=True)

    def _save_discovered_jobs(self, auto: List[ScoredJob], review: List[ScoredJob]):
        DATA_DIR.mkdir(exist_ok=True)
        data = {
            "last_updated": datetime.now().isoformat(),
            "auto_apply": [asdict(j) for j in auto],
            "review":     [asdict(j) for j in review],
        }
        with open(DISCOVERED_FILE, "w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    # ── Deduplication ──────────────────────────────────────────────────────────

    # Query-string keys that vary between feeds for the same posting
    _TRACKING_PARAMS = frozenset({
        "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
        "ref", "source", "from", "trk", "ss", "pk_campaign", "via",
    })

    @classmethod
    def _canonical_url(cls, url: str) -> str:
        """Strip tracking params and fragment so equivalent URLs hash the same."""
        if not url:
            return ""
        try:
            parsed = urlparse(url)
            qs = parse_qs(parsed.query, keep_blank_values=True)
            cleaned = {k: v for k, v in qs.items() if k.lower() not in cls._TRACKING_PARAMS}
            new_query = urlencode(sorted(cleaned.items()), doseq=True)
            return urlunparse(parsed._replace(query=new_query, fragment=""))
        except Exception:
            return url

    def is_seen(self, url: str) -> bool:
        return hashlib.md5(self._canonical_url(url).encode()).hexdigest()[:12] in self.seen_jobs

    def mark_seen(self, job, score: Optional[float] = None):
        """Accept RawJob or ScoredJob — both carry title, company, url."""
        url = self._canonical_url(job.url)
        h = hashlib.md5(url.encode()).hexdigest()[:12]
        self.seen_jobs[h] = {
            "title":      job.title,
            "company":    job.company,
            "url":        url,
            "score":      score if score is not None else getattr(job, "score", None),
            "first_seen": datetime.now().isoformat(),
        }

    def reset_seen(self):
        self.seen_jobs = {}
        self._save_seen_jobs()
        print("Dedup cache cleared.")

    # ── Keyword & location filters ─────────────────────────────────────────────

    def _matches_keywords(self, job: RawJob) -> bool:
        text = f"{job.title} {job.company} {job.location} {job.description}".lower()
        text_words = set(re.findall(r"\b\w+\b", text))
        if self._search_kw:
            # Partial-token matching: a keyword phrase matches when at least
            # ceil(60%) of its tokens appear as individual words anywhere in
            # the text.  This lets "Senior Project Manager" match the phrase
            # "construction project manager" (2/3 tokens present) without
            # requiring the exact multi-word sequence.
            matched = any(
                sum(1 for t in tokens if t in text_words) >= math.ceil(len(tokens) * 0.6)
                for tokens in self._search_kw
                if tokens
            )
            if not matched:
                return False
        if any(re.search(r"\b" + re.escape(ex) + r"\b", text) for ex in self._exclude_kw):
            return False
        return True

    def _matches_location(self, job: RawJob) -> bool:
        if not job.location:
            return True  # unknown location — include to avoid false negatives
        loc = job.location.lower()
        return self._target_city in loc or "remote" in loc or "nationwide" in loc

    # ── RSS scanning ───────────────────────────────────────────────────────────

    def scan_rss_feeds(self) -> List[RawJob]:
        if not HAS_FEEDPARSER:
            print("  [RSS] Skipped — install feedparser:  pip install feedparser",
                  file=sys.stderr)
            return []

        jobs: List[RawJob] = []
        for feed_conf in self.config.get("sources", {}).get("rss", []):
            name = feed_conf.get("name", "RSS")
            url  = feed_conf.get("url", "")
            try:
                feed = feedparser.parse(url)
                count = 0
                for entry in feed.entries:
                    title = (entry.get("title") or "").strip()
                    link  = (entry.get("link")  or "").strip()
                    if not title or not link:
                        continue
                    summary = entry.get("summary") or entry.get("description") or ""
                    jobs.append(RawJob(
                        title=title,
                        company=entry.get("author") or name,
                        url=link,
                        location=self._extract_location(summary or title),
                        posted_date=entry.get("published", ""),
                        description=self._strip_html(summary),
                        source=name,
                    ))
                    count += 1
                print(f"  [RSS] {name}: {count} entries")
            except Exception as exc:
                print(f"  [RSS] {name}: failed — {exc}", file=sys.stderr)
        return jobs

    # ── ATS API scanning ───────────────────────────────────────────────────────

    def scan_ats_apis(self) -> List[RawJob]:
        """Hit public Greenhouse and Lever JSON APIs — no credentials needed."""
        jobs: List[RawJob] = []
        ats = self.config.get("sources", {}).get("ats_apis", {})

        for slug in ats.get("greenhouse", []):
            url = f"https://boards.greenhouse.io/api/v1/boards/{slug}/jobs"
            try:
                data = self._fetch_json(url)
                board_name = data.get("board", {}).get("name") or slug.replace("-", " ").title()
                count = 0
                for item in data.get("jobs", []):
                    loc = (item.get("location") or {}).get("name", "")
                    jobs.append(RawJob(
                        title=item.get("title", ""),
                        company=board_name,
                        url=item.get("absolute_url", ""),
                        location=loc,
                        posted_date=item.get("updated_at", ""),
                        source="Greenhouse",
                    ))
                    count += 1
                print(f"  [Greenhouse] {slug}: {count} jobs")
            except Exception as exc:
                print(f"  [Greenhouse] {slug}: failed — {exc}", file=sys.stderr)

        for slug in ats.get("lever", []):
            url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
            try:
                data = self._fetch_json(url)
                items = data if isinstance(data, list) else []
                count = 0
                for item in items:
                    jobs.append(RawJob(
                        title=item.get("text", ""),
                        company=slug.replace("-", " ").title(),
                        url=item.get("hostedUrl", ""),
                        location=(item.get("categories") or {}).get("location", ""),
                        posted_date=str(item.get("createdAt", "")),
                        description=item.get("descriptionPlain", ""),
                        source="Lever",
                    ))
                    count += 1
                print(f"  [Lever] {slug}: {count} jobs")
            except Exception as exc:
                print(f"  [Lever] {slug}: failed — {exc}", file=sys.stderr)

        return jobs

    # ── Company page scanning ──────────────────────────────────────────────────

    def scan_company_pages(self) -> List[RawJob]:
        pages = self.config.get("sources", {}).get("company_pages", [])
        if not pages:
            return []
        if not (HAS_REQUESTS and HAS_BS4):
            print("  [Pages] Skipped — install requests + beautifulsoup4", file=sys.stderr)
            return []

        jobs: List[RawJob] = []
        for page_conf in pages:
            name     = page_conf.get("name", "Unknown")
            base_url = page_conf.get("url", "")
            selector = page_conf.get("selector", "")
            try:
                resp = requests.get(
                    base_url, timeout=15,
                    headers={"User-Agent": "Mozilla/5.0 (compatible; job-scanner/1.0)"},
                )
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")
                found: List[Tuple[str, str]] = []

                if selector:
                    for el in soup.select(selector):
                        text = el.get_text(strip=True)
                        href = el.get("href") or (el.find("a") and el.find("a").get("href"))
                        if text and href:
                            found.append((text, self._resolve_url(base_url, href)))
                else:
                    for a in soup.find_all("a", href=True):
                        text = a.get_text(strip=True)
                        href = self._resolve_url(base_url, a["href"])
                        if self._looks_like_job(text, href):
                            found.append((text, href))

                count = 0
                for title, job_url in found:
                    jobs.append(RawJob(title=title, company=name, url=job_url, source=name))
                    count += 1
                print(f"  [Page] {name}: {count} potential listings")
            except Exception as exc:
                print(f"  [Page] {name}: failed — {exc}", file=sys.stderr)

        return jobs

    # ── Scoring & triage ───────────────────────────────────────────────────────

    def score_and_triage(
        self, jobs: List[RawJob]
    ) -> Tuple[List[ScoredJob], List[ScoredJob], int]:
        scoring = self.config.get("scoring", {})
        thresh_auto   = scoring.get("auto_apply_threshold", 80)
        thresh_review = scoring.get("review_threshold", 60)

        auto_list: List[ScoredJob] = []
        review_list: List[ScoredJob] = []
        skipped = 0

        for job in jobs:
            # Fetch full description if we only have a title
            if not job.description and HAS_REQUESTS and HAS_BS4:
                job.description = self._fetch_description(job.url)

            text = f"{job.title} {job.company} {job.location} {job.description}"
            kw    = self.analyzer.extract_keywords(text)
            match = self.analyzer.calculate_match_score(kw)
            score = match["score"]

            scored = ScoredJob.from_raw(job, score, match["matches"], match["missing"])

            if score >= thresh_auto:
                # Do NOT mark seen here — run() will mark seen only after a
                # successful autopilot so failed jobs are retried next scan.
                auto_list.append(scored)
            elif score >= thresh_review:
                self.mark_seen(job, score)
                review_list.append(scored)
            else:
                self.mark_seen(job, score)
                skipped += 1

        auto_list.sort(key=lambda x: x.score, reverse=True)
        review_list.sort(key=lambda x: x.score, reverse=True)
        return auto_list, review_list, skipped

    # ── HTTP helpers ───────────────────────────────────────────────────────────

    def _fetch_json(self, url: str) -> dict:
        req = Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        })
        with urlopen(req, timeout=12) as resp:
            return json.loads(resp.read().decode())

    def _fetch_description(self, url: str) -> str:
        try:
            resp = requests.get(
                url, timeout=15,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for el in soup(["script", "style", "nav", "header", "footer"]):
                el.decompose()
            return soup.get_text(separator=" ", strip=True)[:6000]
        except Exception:
            return ""

    # ── Autopilot integration ──────────────────────────────────────────────────

    def run_autopilot(self, job: ScoredJob) -> bool:
        ALERTS_DIR.mkdir(parents=True, exist_ok=True)
        tmp = ALERTS_DIR / f"_tmp_{hashlib.md5(job.url.encode()).hexdigest()[:8]}.txt"
        body = (
            f"{job.title}\nCompany: {job.company}\n{job.location}\n\n"
            f"Job URL: {job.url}\nATS Score: {job.score:.0f}%\n"
        )
        if job.description:
            body += f"\n\n{job.description}\n"
        tmp.write_text(body)
        # Snapshot mtimes before so we detect both newly created files AND
        # in-place overwrites (autopilot writes a deterministic filename; if
        # that file already exists it overwrites in-place, yielding an empty
        # new_files set under a pure set-difference approach).
        before_mtimes = {f: f.stat().st_mtime for f in ALERTS_DIR.glob("*.md")}
        cmd = [
            "python3", str(SCRIPTS_DIR / "application_autopilot.py"),
            "--file", str(tmp),
            "--output-dir", str(ALERTS_DIR),
            "--update-tracker",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        tmp.unlink(missing_ok=True)
        if result.returncode == 0:
            # Rename the affected brief to include the job title so multiple
            # same-company postings on the same day don't share a filename.
            after = set(ALERTS_DIR.glob("*.md"))
            before_set = set(before_mtimes)
            changed = (after - before_set) | {
                f for f in (after & before_set)
                if f.stat().st_mtime != before_mtimes[f]
            }
            if changed:
                generated = next(iter(changed))
                title_slug = re.sub(r"[^\w]+", "-", job.title.lower()).strip("-")[:40]
                base = generated.stem.replace("_autopilot", "") + f"_{title_slug}"
                unique = generated.with_name(f"{base}_autopilot.md")
                if unique.exists():
                    url_suffix = hashlib.md5(job.url.encode()).hexdigest()[:6]
                    unique = generated.with_name(f"{base}_{url_suffix}_autopilot.md")
                generated.rename(unique)
        return result.returncode == 0

    # ── String helpers ─────────────────────────────────────────────────────────

    @staticmethod
    def _extract_location(text: str) -> str:
        m = re.search(r"\b([A-Z][a-zA-Z ]+,\s*[A-Z]{2})\b", text or "")
        return m.group(1).strip() if m else ""

    @staticmethod
    def _strip_html(text: str) -> str:
        return re.sub(r"<[^>]+>", " ", text or "").strip()

    @staticmethod
    def _looks_like_job(text: str, url: str) -> bool:
        if not (5 < len(text) < 120):
            return False
        job_words = ["manager", "superintendent", "estimator", "director",
                     "engineer", "coordinator", "foreman", "executive"]
        url_patterns = ["/job", "/career", "/position", "/opening", "/apply",
                        "lever.co", "greenhouse.io", "workday", "icims"]
        tl = text.lower()
        ul = url.lower()
        return any(w in tl for w in job_words) or any(p in ul for p in url_patterns)

    @staticmethod
    def _resolve_url(base: str, href: str) -> str:
        return urljoin(base, href)

    # ── Main run ───────────────────────────────────────────────────────────────

    def run(self, auto_apply: bool = False) -> dict:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"\n{'='*62}")
        print(f"  Job Discovery  [{ts}]")
        print(f"{'='*62}\n")

        all_jobs: List[RawJob] = []
        all_jobs.extend(self.scan_rss_feeds())
        all_jobs.extend(self.scan_ats_apis())
        all_jobs.extend(self.scan_company_pages())

        relevant = [j for j in all_jobs
                    if self._matches_keywords(j) and self._matches_location(j)]
        # Deduplicate by canonical URL within this scan (same posting from
        # multiple sources, possibly with different tracking params)
        # then filter against the persistent seen-jobs cache.
        seen_in_run: set = set()
        deduped = []
        for j in relevant:
            canon = self._canonical_url(j.url)
            if not canon:
                continue  # skip jobs with null/empty URLs from malformed ATS payloads
            if canon not in seen_in_run:
                seen_in_run.add(canon)
                j.url = canon  # normalise stored URL for consistent hashing
                deduped.append(j)
        new_jobs = [j for j in deduped if not self.is_seen(j.url)]

        print(f"\n  Found {len(all_jobs)} total  |  "
              f"{len(relevant)} relevant  |  {len(new_jobs)} new\n")

        if not new_jobs:
            print("  No new jobs. Check back later.\n")
            self._save_discovered_jobs([], [])  # clear stale entries from prior run
            return {"auto_apply": [], "review": [], "skipped": 0, "total_new": 0}

        print(f"  Scoring {len(new_jobs)} new job(s)...\n")
        auto, review, skipped = self.score_and_triage(new_jobs)

        self._save_discovered_jobs(auto, review)
        self._print_results(auto, review, skipped)

        if auto_apply and auto:
            ALERTS_DIR.mkdir(parents=True, exist_ok=True)
            print(f"  Auto-generating briefs for {len(auto)} high-match job(s)...\n")
            for sj in auto:
                print(f"  Autopilot → {sj.title} @ {sj.company} ({sj.score:.0f}%)")
                ok = self.run_autopilot(sj)
                if ok:
                    # Mark seen only on success so failures are retried next scan
                    self.mark_seen(sj)
                    print(f"    ✓ Brief saved to applications/job_alerts/")
                else:
                    print(f"    ✗ Autopilot failed — will retry on next scan")
        else:
            # Not running autopilot — mark auto candidates seen so they don't
            # flood every non-auto scan (user has seen them in the output).
            for sj in auto:
                self.mark_seen(sj)

        # Single save after all mark_seen calls so auto-candidate entries are
        # persisted regardless of which branch above ran.
        self._save_seen_jobs()

        return {
            "auto_apply": auto,
            "review":     review,
            "skipped":    skipped,
            "total_new":  len(new_jobs),
        }

    def _print_results(
        self, auto: List[ScoredJob], review: List[ScoredJob], skipped: int
    ):
        scoring = self.config.get("scoring", {})
        t_auto   = scoring.get("auto_apply_threshold", 80)
        t_review = scoring.get("review_threshold", 60)

        if auto:
            print(f"  APPLY NOW  (>={t_auto}% match)")
            print(f"  {'-'*56}")
            for sj in auto:
                print(f"  [{sj.score:5.1f}%]  {sj.title}")
                print(f"           {sj.company}  |  {sj.location or 'location N/A'}")
                print(f"           {sj.url}")
                if sj.missing:
                    top_missing = ", ".join(sj.missing[:4])
                    print(f"           Missing: {top_missing}")
                print()

        if review:
            print(f"  WORTH A LOOK  ({t_review}–{t_auto - 1}% match)")
            print(f"  {'-'*56}")
            for sj in review:
                print(f"  [{sj.score:5.1f}%]  {sj.title}  @  {sj.company}")
                print(f"           {sj.url}")
            print()

        if skipped:
            print(f"  {skipped} job(s) below {t_review}% — logged to seen_jobs (won't appear again)\n")

        if not auto and not review:
            print("  No jobs above review threshold this scan.\n")


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Job Discovery — multi-source scanner for construction PM roles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                      # one-shot scan
  %(prog)s --auto               # scan + auto-generate application briefs
  %(prog)s --daemon             # poll continuously (Ctrl+C to stop)
  %(prog)s --daemon --interval 30  # poll every 30 minutes
  %(prog)s --reset              # clear the seen-jobs cache and rescan everything
  %(prog)s --config custom.yaml # use a different config file
        """,
    )
    parser.add_argument(
        "--config", default=str(DEFAULT_CONFIG),
        help="Path to discovery_config.yaml (default: data/discovery_config.yaml)",
    )
    parser.add_argument(
        "--auto", action="store_true",
        help="Auto-run autopilot on jobs that score >=auto_apply_threshold",
    )
    parser.add_argument(
        "--daemon", action="store_true",
        help="Run continuously, polling at the configured interval",
    )
    parser.add_argument(
        "--interval", type=int, default=None,
        help="Polling interval in minutes (overrides config)",
    )
    parser.add_argument(
        "--reset", action="store_true",
        help="Clear the seen-jobs dedup cache so all jobs are re-evaluated",
    )
    args = parser.parse_args()

    discovery = JobDiscovery(config_path=Path(args.config))

    if args.reset:
        discovery.reset_seen()

    if not args.daemon:
        discovery.run(auto_apply=args.auto)
        return

    # Daemon mode — poll on a configurable interval
    polling = discovery.config.get("polling", {})
    interval = args.interval or polling.get("business_hours_interval_min", 15)
    print(f"Daemon mode active — polling every {interval} min.  Ctrl+C to stop.\n")

    while True:
        try:
            discovery.run(auto_apply=args.auto)
            # Use business/off-hours interval if no explicit override
            if not args.interval:
                tz_name = polling.get("timezone", "America/Los_Angeles")
                try:
                    hour = datetime.now(ZoneInfo(tz_name)).hour if HAS_ZONEINFO else datetime.now().hour
                except Exception:
                    hour = datetime.now().hour
                interval = (
                    polling.get("business_hours_interval_min", 15)
                    if 6 <= hour < 18
                    else polling.get("off_hours_interval_min", 60)
                )
            print(f"  Next scan in {interval} min...")
            time.sleep(interval * 60)
            # Reload seen_jobs in case another process also wrote to it
            discovery.seen_jobs = discovery._load_seen_jobs()
        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as exc:
            print(f"\nScan error: {exc} — retrying in {interval} min...", file=sys.stderr)
            time.sleep(interval * 60)


if __name__ == "__main__":
    main()
