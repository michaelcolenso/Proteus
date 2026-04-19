# Job Discovery Scraper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a public-source job discovery command that finds fresh construction PM postings, deduplicates and ranks them, writes local reports, and can feed top matches into the existing autopilot workflow.

**Architecture:** Add a self-contained Python module at `scripts/discover_jobs.py` with focused units for config loading, source adapters, normalization, scoring, dedupe/state, report output, and CLI orchestration. Use standard-library HTTP and parsing for v1, plus existing project patterns for writing Markdown and invoking autopilot. Keep live network access out of normal tests by using unittest fixtures.

**Tech Stack:** Python 3, standard library (`argparse`, `dataclasses`, `json`, `html.parser`, `urllib.request`, `unittest`), a tiny local YAML-subset parser for the editable discovery config, existing `scripts/application_autopilot.py`, shell integration through `generate.sh`.

---

## File Structure

- Create: `scripts/discover_jobs.py` - discovery CLI, model, adapters, scoring, state, and report generation.
- Create: `applications/discovery/sources.yaml` - editable starter config with queries, locations, scoring terms, and source examples.
- Create: `tests/test_discover_jobs.py` - standard-library unittest coverage for config, parsing fixtures, scoring, dedupe, and state.
- Modify: `generate.sh` - add `discover` command and help text.
- Runtime output, not committed unless intentionally reviewed: `applications/discovery/seen.json`, `applications/discovery/jobs.jsonl`, `applications/discovery/latest.md`, `applications/discovery/job_texts/`.

---

### Task 1: Config Loading And Job Model

**Files:**
- Create: `scripts/discover_jobs.py`
- Create: `applications/discovery/sources.yaml`
- Create: `tests/test_discover_jobs.py`

- [ ] **Step 1: Write failing config/model tests**

Create `tests/test_discover_jobs.py` with:

```python
import tempfile
import unittest
from pathlib import Path

from scripts.discover_jobs import DiscoveryConfig, JobPosting, canonicalize_url, load_config


class ConfigAndModelTests(unittest.TestCase):
    def test_load_config_from_json_compatible_yaml(self):
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "sources.yaml"
            config_path.write_text(
                """
queries:
  - construction project manager
locations:
  - Seattle, WA
include_terms:
  - project manager
exclude_terms:
  - software
sources:
  - type: lever
    name: test-co
    url: https://jobs.lever.co/test-co
""".strip()
                + "\n",
                encoding="utf-8",
            )

            config = load_config(config_path)

        self.assertIsInstance(config, DiscoveryConfig)
        self.assertEqual(config.queries, ["construction project manager"])
        self.assertEqual(config.locations, ["Seattle, WA"])
        self.assertEqual(config.sources[0]["type"], "lever")

    def test_job_posting_id_is_stable_from_url_and_fields(self):
        job = JobPosting(
            title="Senior Project Manager",
            company="Acme Builders",
            location="Seattle, WA",
            url="https://example.com/job?utm_source=x",
            source="fixture",
            description="Construction project manager role",
        )

        self.assertEqual(job.canonical_url, "https://example.com/job")
        self.assertEqual(job.id, "85538a4c99df")

    def test_canonicalize_url_removes_tracking_params_and_fragments(self):
        url = "https://example.com/jobs/123?utm_source=mail&gh_src=abc&query=pm#apply"
        self.assertEqual(canonicalize_url(url), "https://example.com/jobs/123?query=pm")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests and verify they fail**

Run:

```bash
python3 -m unittest tests.test_discover_jobs -v
```

Expected: FAIL because `scripts.discover_jobs` does not exist.

- [ ] **Step 3: Implement config loading and model**

Create `scripts/discover_jobs.py` with the initial complete content:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover
    yaml = None


DEFAULT_CONFIG = Path("applications/discovery/sources.yaml")
DISCOVERY_DIR = Path("applications/discovery")
TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gh_src"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonicalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    query = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True) if k not in TRACKING_PARAMS]
    return urlunparse((parsed.scheme, parsed.netloc.lower(), parsed.path.rstrip("/") or "/", "", urlencode(query), ""))


@dataclass
class DiscoveryConfig:
    queries: List[str] = field(default_factory=list)
    locations: List[str] = field(default_factory=list)
    include_terms: List[str] = field(default_factory=list)
    exclude_terms: List[str] = field(default_factory=list)
    sources: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class JobPosting:
    title: str
    company: str
    location: str
    url: str
    source: str
    description: str = ""
    snippet: str = ""
    posted_at: Optional[str] = None
    discovered_at: str = field(default_factory=utc_now)
    tags: List[str] = field(default_factory=list)
    score: float = 0.0
    score_reasons: List[str] = field(default_factory=list)

    @property
    def canonical_url(self) -> str:
        return canonicalize_url(self.url)

    @property
    def id(self) -> str:
        raw = "|".join([self.canonical_url, self.company.lower().strip(), self.title.lower().strip()])
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]

    def to_record(self) -> Dict[str, Any]:
        record = asdict(self)
        record["id"] = self.id
        record["canonical_url"] = self.canonical_url
        return record


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    return value


def load_simple_yaml(text: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    current_key: Optional[str] = None
    current_item: Optional[Dict[str, Any]] = None
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if not raw_line.startswith(" "):
            current_key = raw_line.strip().rstrip(":")
            data[current_key] = []
            current_item = None
            continue
        if current_key is None:
            continue
        stripped = raw_line.strip()
        if stripped.startswith("- "):
            value = stripped[2:]
            if current_key == "sources" and ":" in value:
                key, raw_value = value.split(":", 1)
                current_item = {key.strip(): parse_scalar(raw_value)}
                data[current_key].append(current_item)
            else:
                data[current_key].append(parse_scalar(value))
            continue
        if current_item is not None and ":" in stripped:
            key, raw_value = stripped.split(":", 1)
            current_item[key.strip()] = parse_scalar(raw_value)
    return data


def load_config(path: Path = DEFAULT_CONFIG) -> DiscoveryConfig:
    if not path.exists():
        return DiscoveryConfig()
    text = path.read_text(encoding="utf-8")
    if yaml:
        raw = yaml.safe_load(text) or {}
    else:
        raw = load_simple_yaml(text)
    return DiscoveryConfig(
        queries=list(raw.get("queries", [])),
        locations=list(raw.get("locations", [])),
        include_terms=list(raw.get("include_terms", [])),
        exclude_terms=list(raw.get("exclude_terms", [])),
        sources=list(raw.get("sources", [])),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover fresh construction job postings")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    args = parser.parse_args()
    config = load_config(Path(args.config))
    print(f"Loaded {len(config.sources)} sources, {len(config.queries)} queries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Create `applications/discovery/sources.yaml`:

```yaml
queries:
  - construction project manager
  - senior project manager construction
  - multifamily project manager
  - construction superintendent
  - construction estimator
  - owner's representative construction

locations:
  - Seattle, WA
  - Bellevue, WA
  - Remote

include_terms:
  - project manager
  - senior project manager
  - construction manager
  - superintendent
  - estimator
  - preconstruction
  - owner representative
  - multifamily
  - luxury residential
  - general contractor

exclude_terms:
  - software engineer
  - product manager
  - account executive
  - internship
  - unpaid

sources:
  - type: lever
    name: sample-lever
    url: https://jobs.lever.co/example
    enabled: false
  - type: career_page
    name: sample-career-page
    url: https://example.com/careers
    enabled: false
```

- [ ] **Step 4: Run tests and verify they pass**

Run:

```bash
python3 -m unittest tests.test_discover_jobs -v
```

Expected: PASS for the three tests.

- [ ] **Step 5: Commit**

```bash
git add scripts/discover_jobs.py applications/discovery/sources.yaml tests/test_discover_jobs.py
git commit -m "Add discovery config and job model"
```

---

### Task 2: Ranking, Dedupe, And State

**Files:**
- Modify: `scripts/discover_jobs.py`
- Modify: `tests/test_discover_jobs.py`

- [ ] **Step 1: Add failing scoring and state tests**

Append to `tests/test_discover_jobs.py` before the `if __name__ == "__main__"` block:

```python
class ScoringAndStateTests(unittest.TestCase):
    def test_score_jobs_rewards_relevance_location_and_penalizes_exclusions(self):
        config = DiscoveryConfig(
            locations=["Seattle, WA"],
            include_terms=["project manager", "multifamily", "construction"],
            exclude_terms=["software"],
        )
        jobs = [
            JobPosting(
                title="Senior Project Manager",
                company="Builder",
                location="Seattle, WA",
                url="https://example.com/a",
                source="fixture",
                description="Lead multifamily construction projects.",
            ),
            JobPosting(
                title="Software Product Manager",
                company="Tech",
                location="Seattle, WA",
                url="https://example.com/b",
                source="fixture",
                description="Software roadmap role.",
            ),
        ]

        ranked = score_jobs(jobs, config)

        self.assertGreater(ranked[0].score, ranked[1].score)
        self.assertIn("matched: project manager", ranked[0].score_reasons)
        self.assertIn("location: Seattle, WA", ranked[0].score_reasons)
        self.assertIn("penalty: software", ranked[1].score_reasons)

    def test_discovery_state_filters_seen_jobs_and_preserves_first_seen(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = DiscoveryState(Path(tmp))
            job = JobPosting(
                title="Project Manager",
                company="Builder",
                location="Seattle, WA",
                url="https://example.com/job",
                source="fixture",
            )

            fresh = state.filter_new([job])
            state.record_jobs(fresh)
            repeated = state.filter_new([job])

        self.assertEqual(len(fresh), 1)
        self.assertEqual(repeated, [])
```

Update the import line:

```python
from scripts.discover_jobs import DiscoveryConfig, DiscoveryState, JobPosting, canonicalize_url, load_config, parse_posted_at, score_jobs
```

Also add this test inside `ScoringAndStateTests`:

```python
    def test_parse_posted_at_normalizes_common_public_formats(self):
        self.assertEqual(parse_posted_at("2026-04-18"), "2026-04-18T00:00:00+00:00")
        self.assertEqual(parse_posted_at("2026-04-18T12:30:00Z"), "2026-04-18T12:30:00+00:00")
        self.assertIsNotNone(parse_posted_at("2 days ago"))
```

- [ ] **Step 2: Run tests and verify they fail**

Run:

```bash
python3 -m unittest tests.test_discover_jobs -v
```

Expected: FAIL because `score_jobs` and `DiscoveryState` are not implemented.

- [ ] **Step 3: Implement scoring and local state**

Add to `scripts/discover_jobs.py` after `load_config`:

```python
def parse_posted_at(value: str | None) -> Optional[str]:
    if not value:
        return None
    cleaned = value.strip().lower().replace("posted", "").strip()
    if cleaned.endswith("z"):
        cleaned = cleaned[:-1] + "+00:00"
    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(cleaned, fmt).replace(tzinfo=timezone.utc).isoformat()
        except ValueError:
            pass
    try:
        parsed = datetime.fromisoformat(cleaned)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).replace(microsecond=0).isoformat()
    except ValueError:
        pass
    relative = re.search(r"(\d+)\s+(hour|hours|day|days)\s+ago", cleaned)
    if relative:
        amount = int(relative.group(1))
        unit = relative.group(2)
        delta = timedelta(hours=amount) if unit.startswith("hour") else timedelta(days=amount)
        return (datetime.now(timezone.utc) - delta).replace(microsecond=0).isoformat()
    return None


def _contains(text: str, term: str) -> bool:
    return re.search(r"\b" + re.escape(term.lower()) + r"\b", text.lower()) is not None


def score_jobs(jobs: Iterable[JobPosting], config: DiscoveryConfig) -> List[JobPosting]:
    scored = []
    for job in jobs:
        haystack = " ".join([job.title, job.company, job.location, job.description, job.snippet]).lower()
        score = 0.0
        reasons: List[str] = []

        for term in config.include_terms:
            if _contains(haystack, term):
                score += 10.0
                reasons.append(f"matched: {term}")

        for location in config.locations:
            if location.lower() in job.location.lower() or location.lower() in haystack:
                score += 8.0
                reasons.append(f"location: {location}")
                break

        title_lower = job.title.lower()
        if "senior" in title_lower:
            score += 4.0
            reasons.append("seniority: senior")
        if "project manager" in title_lower:
            score += 6.0
            reasons.append("role: project manager")

        if job.posted_at:
            score += 5.0
            reasons.append("has posted date")
        else:
            score += 2.0
            reasons.append("freshly discovered")

        for term in config.exclude_terms:
            if _contains(haystack, term):
                score -= 25.0
                reasons.append(f"penalty: {term}")

        job.score = score
        job.score_reasons = reasons
        job.tags = [reason.removeprefix("matched: ") for reason in reasons if reason.startswith("matched: ")]
        scored.append(job)

    return sorted(scored, key=lambda item: item.score, reverse=True)


class DiscoveryState:
    def __init__(self, discovery_dir: Path = DISCOVERY_DIR):
        self.discovery_dir = discovery_dir
        self.seen_path = discovery_dir / "seen.json"
        self.jobs_path = discovery_dir / "jobs.jsonl"
        self.discovery_dir.mkdir(parents=True, exist_ok=True)
        self.seen: Dict[str, str] = self._load_seen()

    def _load_seen(self) -> Dict[str, str]:
        if not self.seen_path.exists():
            return {}
        return json.loads(self.seen_path.read_text(encoding="utf-8"))

    def filter_new(self, jobs: Iterable[JobPosting]) -> List[JobPosting]:
        return [job for job in jobs if job.id not in self.seen]

    def record_jobs(self, jobs: Iterable[JobPosting]) -> None:
        records = list(jobs)
        if not records:
            return
        with self.jobs_path.open("a", encoding="utf-8") as handle:
            for job in records:
                self.seen.setdefault(job.id, job.discovered_at)
                record = job.to_record()
                record["discovered_at"] = self.seen[job.id]
                handle.write(json.dumps(record, sort_keys=True) + "\n")
        self.seen_path.write_text(json.dumps(self.seen, indent=2, sort_keys=True) + "\n", encoding="utf-8")
```

- [ ] **Step 4: Run tests and verify they pass**

Run:

```bash
python3 -m unittest tests.test_discover_jobs -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/discover_jobs.py tests/test_discover_jobs.py
git commit -m "Add discovery scoring and state"
```

---

### Task 3: Source Adapters And Fixture Parsing

**Files:**
- Modify: `scripts/discover_jobs.py`
- Modify: `tests/test_discover_jobs.py`

- [ ] **Step 1: Add failing adapter tests**

Append to `tests/test_discover_jobs.py` before the `if __name__ == "__main__"` block:

```python
class AdapterTests(unittest.TestCase):
    def test_parse_lever_jobs(self):
        payload = [
            {
                "text": "Senior Project Manager",
                "hostedUrl": "https://jobs.lever.co/acme/123",
                "categories": {"location": "Seattle, WA"},
                "descriptionPlain": "Manage multifamily construction.",
            }
        ]

        jobs = parse_lever_jobs(payload, {"name": "acme", "url": "https://jobs.lever.co/acme"})

        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].title, "Senior Project Manager")
        self.assertEqual(jobs[0].company, "acme")
        self.assertEqual(jobs[0].location, "Seattle, WA")

    def test_parse_generic_career_page_links(self):
        html = '''
        <html><body>
          <a href="/careers/senior-project-manager">Senior Project Manager - Seattle</a>
          <a href="/about">About</a>
        </body></html>
        '''

        jobs = parse_career_page(html, {"name": "Acme Builders", "url": "https://example.com/careers"})

        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].url, "https://example.com/careers/senior-project-manager")
        self.assertEqual(jobs[0].title, "Senior Project Manager - Seattle")
```

Update the import line:

```python
from scripts.discover_jobs import DiscoveryConfig, DiscoveryState, JobPosting, canonicalize_url, load_config, parse_career_page, parse_lever_jobs, parse_posted_at, score_jobs
```

- [ ] **Step 2: Run tests and verify they fail**

Run:

```bash
python3 -m unittest tests.test_discover_jobs -v
```

Expected: FAIL because parser functions do not exist.

- [ ] **Step 3: Implement adapter parsing and public fetch helpers**

Add imports near the top of `scripts/discover_jobs.py`:

```python
from html.parser import HTMLParser
from urllib.parse import urljoin
from urllib.request import Request, urlopen
```

Add after `DiscoveryState`:

```python
class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: List[Dict[str, str]] = []
        self._href: Optional[str] = None
        self._text: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        if tag == "a":
            attr_map = dict(attrs)
            self._href = attr_map.get("href")
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._href:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href:
            text = " ".join(part.strip() for part in self._text if part.strip())
            if text:
                self.links.append({"href": self._href, "text": text})
            self._href = None
            self._text = []


def fetch_text(url: str, timeout: int = 12) -> str:
    request = Request(url, headers={"User-Agent": "ProteusJobDiscovery/1.0 (+public job discovery)"})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_lever_jobs(payload: List[Dict[str, Any]], source: Dict[str, Any]) -> List[JobPosting]:
    jobs = []
    company = source.get("company") or source.get("name", "Unknown Company")
    for item in payload:
        title = item.get("text") or item.get("title")
        url = item.get("hostedUrl") or item.get("applyUrl")
        if not title or not url:
            continue
        categories = item.get("categories") or {}
        jobs.append(
            JobPosting(
                title=title,
                company=company,
                location=categories.get("location", ""),
                url=url,
                source=source.get("name", "lever"),
                description=item.get("descriptionPlain", "") or item.get("description", ""),
                snippet=item.get("additionalPlain", "")[:300],
            )
        )
    return jobs


def parse_career_page(html: str, source: Dict[str, Any]) -> List[JobPosting]:
    collector = LinkCollector()
    collector.feed(html)
    jobs = []
    terms = ("project manager", "construction manager", "superintendent", "estimator", "preconstruction")
    for link in collector.links:
        text = re.sub(r"\s+", " ", link["text"]).strip()
        if not any(term in text.lower() for term in terms):
            continue
        jobs.append(
            JobPosting(
                title=text,
                company=source.get("company") or source.get("name", "Unknown Company"),
                location=source.get("location", ""),
                url=urljoin(source["url"], link["href"]),
                source=source.get("name", "career_page"),
                snippet=text,
            )
        )
    return jobs


def fetch_source(source: Dict[str, Any]) -> List[JobPosting]:
    if source.get("enabled") is False:
        return []
    source_type = source.get("type")
    if source_type == "lever":
        base = source["url"].rstrip("/")
        api_url = base + "?mode=json"
        return parse_lever_jobs(json.loads(fetch_text(api_url)), source)
    if source_type == "career_page":
        return parse_career_page(fetch_text(source["url"]), source)
    raise ValueError(f"Unsupported source type: {source_type}")
```

- [ ] **Step 4: Run tests and verify they pass**

Run:

```bash
python3 -m unittest tests.test_discover_jobs -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/discover_jobs.py tests/test_discover_jobs.py
git commit -m "Add discovery source adapters"
```

---

### Task 4: CLI Orchestration, Reports, And Autopilot Handoff

**Files:**
- Modify: `scripts/discover_jobs.py`
- Modify: `tests/test_discover_jobs.py`

- [ ] **Step 1: Add failing report and dry-run tests**

Append to `tests/test_discover_jobs.py` before the `if __name__ == "__main__"` block:

```python
class ReportTests(unittest.TestCase):
    def test_render_latest_report_includes_ranked_jobs_and_errors(self):
        job = JobPosting(
            title="Senior Project Manager",
            company="Acme",
            location="Seattle, WA",
            url="https://example.com/job",
            source="fixture",
            score=31.0,
            score_reasons=["matched: project manager", "location: Seattle, WA"],
        )

        report = render_latest_report([job], ["broken-source: timeout"], limit=10)

        self.assertIn("# Latest Job Discovery", report)
        self.assertIn("Senior Project Manager", report)
        self.assertIn("broken-source: timeout", report)

    def test_load_fixture_jobs_reads_json_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "jobs.json"
            fixture.write_text(
                '[{"title":"Estimator","company":"Acme","location":"Seattle, WA","url":"https://example.com/e","source":"fixture"}]',
                encoding="utf-8",
            )

            jobs = load_fixture_jobs(fixture)

        self.assertEqual(jobs[0].title, "Estimator")

    def test_filter_recent_jobs_uses_since_hours(self):
        fresh = JobPosting(
            title="Project Manager",
            company="Acme",
            location="Seattle, WA",
            url="https://example.com/fresh",
            source="fixture",
            posted_at="2026-04-19T10:00:00+00:00",
        )
        stale = JobPosting(
            title="Project Manager",
            company="Acme",
            location="Seattle, WA",
            url="https://example.com/stale",
            source="fixture",
            posted_at="2026-04-17T10:00:00+00:00",
        )

        jobs = filter_recent_jobs([fresh, stale], since_hours=24, now=datetime(2026, 4, 19, 12, 0, tzinfo=timezone.utc))

        self.assertEqual([job.url for job in jobs], ["https://example.com/fresh"])
```

Update the import line:

```python
from datetime import datetime, timezone

from scripts.discover_jobs import DiscoveryConfig, DiscoveryState, JobPosting, canonicalize_url, filter_recent_jobs, load_config, load_fixture_jobs, parse_career_page, parse_lever_jobs, parse_posted_at, render_latest_report, score_jobs
```

- [ ] **Step 2: Run tests and verify they fail**

Run:

```bash
python3 -m unittest tests.test_discover_jobs -v
```

Expected: FAIL because report and fixture helpers do not exist.

- [ ] **Step 3: Implement orchestration helpers and report output**

Add to `scripts/discover_jobs.py` after `fetch_source`:

```python
def load_fixture_jobs(path: Path) -> List[JobPosting]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [JobPosting(**item) for item in payload]


def render_latest_report(jobs: List[JobPosting], errors: List[str], limit: int) -> str:
    lines = [
        "# Latest Job Discovery",
        "",
        f"Generated: {utc_now()}",
        "",
        "## Top Matches",
        "",
    ]
    if not jobs:
        lines.append("No matching jobs found.")
    for index, job in enumerate(jobs[:limit], 1):
        reasons = "; ".join(job.score_reasons) or "no score reasons"
        lines.extend(
            [
                f"### {index}. {job.title}",
                "",
                f"- Company: {job.company}",
                f"- Location: {job.location or 'Unknown'}",
                f"- Score: {job.score:.1f}",
                f"- Source: {job.source}",
                f"- URL: {job.canonical_url}",
                f"- Reasons: {reasons}",
                "",
            ]
        )
    if errors:
        lines.extend(["## Source Errors", ""])
        lines.extend(f"- {error}" for error in errors)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_autopilot_inputs(jobs: List[JobPosting], output_dir: Path) -> List[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for job in jobs:
        path = output_dir / f"{job.id}.txt"
        text = "\n".join([f"Company: {job.company}", f"Title: {job.title}", f"Location: {job.location}", job.description or job.snippet])
        path.write_text(text.strip() + "\n", encoding="utf-8")
        paths.append(path)
    return paths


def discover(config: DiscoveryConfig, fixture_path: Optional[Path] = None) -> tuple[List[JobPosting], List[str]]:
    errors: List[str] = []
    jobs: List[JobPosting] = []
    if fixture_path:
        return load_fixture_jobs(fixture_path), errors
    for source in config.sources:
        try:
            jobs.extend(fetch_source(source))
        except Exception as exc:
            errors.append(f"{source.get('name', 'unknown')}: {exc}")
    return jobs, errors


def filter_recent_jobs(jobs: List[JobPosting], since_hours: int, now: Optional[datetime] = None) -> List[JobPosting]:
    if since_hours <= 0:
        return jobs
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=since_hours)
    recent = []
    for job in jobs:
        timestamp = job.posted_at or job.discovered_at
        try:
            parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            recent.append(job)
            continue
        if parsed >= cutoff:
            recent.append(job)
    return recent
```

Replace `main()` in `scripts/discover_jobs.py` with:

```python
def main() -> int:
    parser = argparse.ArgumentParser(description="Discover fresh construction job postings")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--since-hours", type=int, default=48)
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--autopilot-top", type=int, default=0)
    parser.add_argument("--dry-run-fixtures", help="Path to JSON fixture jobs")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    state = DiscoveryState(DISCOVERY_DIR)
    jobs, errors = discover(config, Path(args.dry_run_fixtures) if args.dry_run_fixtures else None)
    recent_jobs = filter_recent_jobs(jobs, args.since_hours)
    ranked = score_jobs(recent_jobs, config)
    fresh = state.filter_new(ranked)
    state.record_jobs(fresh)

    latest_path = DISCOVERY_DIR / "latest.md"
    latest_path.write_text(render_latest_report(ranked, errors, args.limit), encoding="utf-8")

    if args.autopilot_top > 0:
        paths = write_autopilot_inputs(ranked[: args.autopilot_top], DISCOVERY_DIR / "job_texts")
        print("Autopilot input files:")
        for path in paths:
            print(" -", path)
        print("Run ./generate.sh autopilot <file> for any selected posting.")

    print(f"Discovered {len(jobs)} jobs; {len(fresh)} new; wrote {latest_path}")
    if errors:
        print(f"{len(errors)} source errors; see {latest_path}")
    return 0
```

- [ ] **Step 4: Run tests and verify they pass**

Run:

```bash
python3 -m unittest tests.test_discover_jobs -v
```

Expected: PASS.

- [ ] **Step 5: Smoke test dry-run CLI**

Run:

```bash
mkdir -p /tmp/proteus-discovery
printf '[{"title":"Senior Project Manager","company":"Acme","location":"Seattle, WA","url":"https://example.com/job","source":"fixture","description":"Multifamily construction project manager role."}]' > /tmp/proteus-discovery/jobs.json
python3 scripts/discover_jobs.py --dry-run-fixtures /tmp/proteus-discovery/jobs.json --limit 5
```

Expected: prints `Discovered 1 jobs; 1 new; wrote applications/discovery/latest.md`.

- [ ] **Step 6: Commit**

```bash
git add scripts/discover_jobs.py tests/test_discover_jobs.py applications/discovery
git commit -m "Add discovery CLI reports"
```

---

### Task 5: Shell Integration And Final Verification

**Files:**
- Modify: `generate.sh`
- Modify: `README.md`

- [ ] **Step 1: Add `generate.sh discover` command**

In `generate.sh`, add this case before `clean`:

```bash
    "discover")
        shift
        echo "=== Discovering fresh job postings ==="
        python3 scripts/discover_jobs.py "$@"
        ;;
```

In help output, add:

```bash
  discover [args] Discover fresh public job postings
```

And add an example:

```bash
  ./generate.sh discover --limit 25
  ./generate.sh discover --dry-run-fixtures /tmp/proteus-discovery/jobs.json
```

- [ ] **Step 2: Add README usage section**

In `README.md`, add this section after Application Autopilot:

    ### Job Discovery

    Discover fresh public job postings and rank them for construction PM relevance:

    ```bash
    ./generate.sh discover --limit 25
    ./generate.sh discover --autopilot-top 5
    ```

    Discovery reads editable source settings from `applications/discovery/sources.yaml` and writes the latest ranked report to `applications/discovery/latest.md`. The first version uses public sources only and does not use logged-in accounts, captcha solving, or access-control bypasses.

- [ ] **Step 3: Run unit tests**

Run:

```bash
python3 -m unittest tests.test_discover_jobs -v
```

Expected: PASS.

- [ ] **Step 4: Run shell dry-run smoke test**

Run:

```bash
./generate.sh discover --dry-run-fixtures /tmp/proteus-discovery/jobs.json --limit 5
```

Expected: prints `=== Discovering fresh job postings ===` and `Discovered 1 jobs`.

- [ ] **Step 5: Inspect latest report**

Run:

```bash
sed -n '1,120p' applications/discovery/latest.md
```

Expected: report contains `# Latest Job Discovery`, `Senior Project Manager`, `Acme`, and `Score:`.

- [ ] **Step 6: Commit**

```bash
git add generate.sh README.md applications/discovery/latest.md
git commit -m "Wire discovery command into project workflow"
```

---

## Final Verification

- [ ] Run all discovery tests:

```bash
python3 -m unittest tests.test_discover_jobs -v
```

Expected: all tests pass.

- [ ] Run a dry-run discovery:

```bash
./generate.sh discover --dry-run-fixtures /tmp/proteus-discovery/jobs.json --limit 5
```

Expected: `applications/discovery/latest.md` is written and includes the fixture job.

- [ ] Check working tree scope:

```bash
git status --short
```

Expected: only intentional discovery-related files are modified or untracked. Existing unrelated user changes may still be present and must not be reverted.

---

## Spec Coverage Review

- Public-only source boundary: covered by source strategy, adapter implementation, README text, and no auth/browser/captcha steps.
- Broad source architecture: covered by adapter-based `fetch_source` and starter config.
- Freshness and relevance ranking: covered by `parse_posted_at`, `filter_recent_jobs`, `--since-hours`, and `score_jobs`.
- Dedupe and repeated-run behavior: covered by `DiscoveryState`.
- Local outputs: covered by `seen.json`, `jobs.jsonl`, `latest.md`, and job text handoff files.
- Autopilot handoff: v1 writes selected job text files and prints the existing autopilot command rather than invoking nested commands directly.
- Testing without live network: covered by parser tests and dry-run fixture support.
