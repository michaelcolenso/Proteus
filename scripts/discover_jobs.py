#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import hashlib
import re
from html.parser import HTMLParser
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / "applications/discovery/sources.yaml"
DISCOVERY_DIR = REPO_ROOT / "applications/discovery"
TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "gh_src",
}

try:  # pragma: no cover - optional dependency
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - local fallback
    yaml = None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonicalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    query_pairs = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if key.lower() not in TRACKING_PARAMS
    ]
    query_pairs.sort()
    path = parts.path or ""
    if path.endswith("/") and path != "/":
        path = path.rstrip("/")
    canonical = urlunsplit(
        (
            parts.scheme.lower(),
            parts.netloc.lower(),
            path,
            urlencode(query_pairs, doseq=True),
            "",
        )
    )
    return canonical


def _contains(text: str, term: str) -> bool:
    if not text or not term:
        return False
    return re.search(rf"\b{re.escape(term.lower())}\b", text.lower()) is not None


def _format_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()


def parse_posted_at(value: str | None) -> str | None:
    if not value:
        return None

    text = value.strip()
    if not text:
        return None

    lowered = text.lower()

    if lowered == "today":
        return _format_utc(datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0))

    if lowered == "yesterday":
        return _format_utc(
            datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        )

    date_only = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", text)
    if date_only:
        year, month, day = map(int, date_only.groups())
        return _format_utc(datetime(year, month, day, tzinfo=timezone.utc))

    slash_date = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", text)
    if slash_date:
        month, day, year = map(int, slash_date.groups())
        return _format_utc(datetime(year, month, day, tzinfo=timezone.utc))

    relative = re.fullmatch(r"(\d+)\+?\s*(h|hr|hrs|hour|hours|d|day|days|w|wk|wks|week|weeks)\s+ago", lowered)
    if relative:
        amount = int(relative.group(1))
        unit = relative.group(2)
        now = datetime.now(timezone.utc).replace(microsecond=0)
        if unit in {"h", "hr", "hrs", "hour", "hours"}:
            return _format_utc(now - timedelta(hours=amount))
        if unit in {"w", "wk", "wks", "week", "weeks"}:
            return _format_utc(now - timedelta(days=amount * 7))
        return _format_utc(now - timedelta(days=amount))

    iso_text = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(iso_text)
    except ValueError:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return _format_utc(parsed)


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._current_href: str | None = None
        self._current_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        self._current_href = dict(attrs).get("href")
        self._current_text = []

    def handle_data(self, data: str) -> None:
        if self._current_href is not None:
            self._current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "a" or self._current_href is None:
            return
        text = re.sub(r"\s+", " ", "".join(self._current_text)).strip()
        self.links.append((self._current_href, text))
        self._current_href = None
        self._current_text = []


def fetch_text(url: str, timeout: int = 12) -> str:
    request = Request(url, headers={"User-Agent": "ProteusJobDiscovery/1.0 (+public job discovery)"})
    with urlopen(request, timeout=timeout) as response:
        data = response.read()
        return data.decode("utf-8", errors="replace")


def _first_string(*values: Any) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def parse_lever_jobs(payload: Any, source: dict[str, Any]) -> list["JobPosting"]:
    if not isinstance(payload, list):
        return []

    company = str(source.get("company") or source.get("name", "Unknown Company"))
    source_name = str(source.get("name", "lever"))
    jobs: list[JobPosting] = []

    for item in payload:
        if not isinstance(item, dict):
            continue

        title = _first_string(item.get("text"), item.get("title"))
        url = _first_string(item.get("hostedUrl"), item.get("applyUrl"))
        if not title or not url:
            continue

        categories = item.get("categories")
        location = ""
        if isinstance(categories, dict):
            location = _first_string(categories.get("location"))

        description = _first_string(item.get("descriptionPlain"), item.get("description"))
        snippet_source = _first_string(item.get("additionalPlain"))
        snippet = snippet_source[:300] if snippet_source else ""

        jobs.append(
            JobPosting(
                title=title,
                company=company,
                location=location,
                url=url,
                source=source_name,
                description=description,
                snippet=snippet,
            )
        )

    return jobs


def parse_career_page(html: str, source: dict[str, Any]) -> list["JobPosting"]:
    collector = LinkCollector()
    collector.feed(html)

    company = str(source.get("company") or source.get("name", "Unknown Company"))
    source_name = str(source.get("name", "career_page"))
    location = str(source.get("location", ""))
    base_url = str(source["url"])
    keywords = ("project manager", "construction manager", "superintendent", "estimator", "preconstruction")

    jobs: list[JobPosting] = []
    for href, text in collector.links:
        if not href or not text:
            continue
        normalized_text = re.sub(r"\s+", " ", text).strip()
        lowered = normalized_text.lower()
        if not any(keyword in lowered for keyword in keywords):
            continue
        jobs.append(
            JobPosting(
                title=normalized_text,
                company=company,
                location=location,
                url=urljoin(base_url, href),
                source=source_name,
            )
        )

    return jobs


def fetch_source(source: dict[str, Any]) -> list["JobPosting"]:
    if source.get("enabled") is False:
        return []

    source_type = str(source.get("type", ""))
    if source_type == "lever":
        payload = json.loads(fetch_text(str(source["url"]).rstrip("/") + "?mode=json"))
        return parse_lever_jobs(payload, source)

    if source_type == "career_page":
        html = fetch_text(str(source["url"]))
        return parse_career_page(html, source)

    raise ValueError(f"Unsupported source type: {source_type}")


def parse_scalar(value: str) -> Any:
    text = value.strip()
    if text == "":
        return ""
    lowered = text.lower()
    if lowered in {"null", "~", "none"}:
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        inner = text[1:-1]
        if text.startswith('"'):
            inner = inner.replace('\\"', '"').replace("\\\\", "\\")
        else:
            inner = inner.replace("\\'", "'").replace("\\\\", "\\")
        return inner
    if re.fullmatch(r"[-+]?\d+", text):
        try:
            return int(text)
        except ValueError:
            pass
    if re.fullmatch(r"[-+]?(?:\d+\.\d*|\d*\.\d+)", text):
        try:
            return float(text)
        except ValueError:
            pass
    return text


def _strip_comments(line: str) -> str:
    if "#" not in line:
        return line.rstrip()
    in_single = False
    in_double = False
    for index, char in enumerate(line):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            return line[:index].rstrip()
    return line.rstrip()


def load_simple_yaml(text: str) -> dict[str, Any]:
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        cleaned = _strip_comments(raw)
        if not cleaned.strip():
            continue
        indent = len(cleaned) - len(cleaned.lstrip(" "))
        lines.append((indent, cleaned.strip()))

    if not lines:
        return {}

    def parse_mapping(start_index: int, indent: int) -> tuple[dict[str, Any], int]:
        result: dict[str, Any] = {}
        index = start_index
        while index < len(lines):
            current_indent, content = lines[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                break
            if content.startswith("- "):
                break
            if ":" not in content:
                raise ValueError(f"Invalid YAML mapping line: {content!r}")
            key, raw_value = content.split(":", 1)
            key = key.strip()
            raw_value = raw_value.strip()
            index += 1
            if raw_value:
                result[key] = parse_scalar(raw_value)
                continue
            if index >= len(lines) or lines[index][0] <= indent:
                result[key] = None
                continue
            child_indent, child_content = lines[index]
            if child_content.startswith("- "):
                value, index = parse_sequence(index, child_indent)
            else:
                value, index = parse_mapping(index, child_indent)
            result[key] = value
        return result, index

    def parse_inline_mapping(text: str) -> dict[str, Any]:
        if ":" not in text:
            return {"value": parse_scalar(text)}
        key, raw_value = text.split(":", 1)
        mapping: dict[str, Any] = {key.strip(): parse_scalar(raw_value.strip()) if raw_value.strip() else None}
        return mapping

    def parse_sequence(start_index: int, indent: int) -> tuple[list[Any], int]:
        result: list[Any] = []
        index = start_index
        while index < len(lines):
            current_indent, content = lines[index]
            if current_indent < indent:
                break
            if current_indent != indent or not content.startswith("- "):
                break
            item_text = content[2:].strip()
            index += 1
            if not item_text:
                if index >= len(lines) or lines[index][0] <= indent:
                    result.append(None)
                    continue
                child_indent, child_content = lines[index]
                if child_content.startswith("- "):
                    value, index = parse_sequence(index, child_indent)
                else:
                    value, index = parse_mapping(index, child_indent)
                result.append(value)
                continue
            if ":" in item_text:
                item = parse_inline_mapping(item_text)
                while index < len(lines) and lines[index][0] > indent:
                    child_indent, child_content = lines[index]
                    if child_content.startswith("- "):
                        value, index = parse_sequence(index, child_indent)
                        item.setdefault("_items", []).append(value)
                        continue
                    child_key, child_raw_value = child_content.split(":", 1)
                    index += 1
                    if child_raw_value.strip():
                        item[child_key.strip()] = parse_scalar(child_raw_value.strip())
                    else:
                        if index < len(lines) and lines[index][0] > child_indent:
                            next_indent, next_content = lines[index]
                            if next_content.startswith("- "):
                                value, index = parse_sequence(index, next_indent)
                            else:
                                value, index = parse_mapping(index, next_indent)
                            item[child_key.strip()] = value
                        else:
                            item[child_key.strip()] = None
                result.append(item)
                continue
            result.append(parse_scalar(item_text))
        return result, index

    first_indent, first_content = lines[0]
    if first_content.startswith("- "):
        parsed, _ = parse_sequence(0, first_indent)
        return {"items": parsed}
    parsed, _ = parse_mapping(0, first_indent)
    return parsed


@dataclass
class DiscoveryConfig:
    queries: list[str] = field(default_factory=list)
    locations: list[str] = field(default_factory=list)
    include_terms: list[str] = field(default_factory=list)
    exclude_terms: list[str] = field(default_factory=list)
    sources: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class JobPosting:
    title: str
    company: str
    location: str
    url: str
    source: str
    description: str = ""
    snippet: str = ""
    posted_at: str | None = None
    discovered_at: str = field(default_factory=utc_now)
    tags: list[str] = field(default_factory=list)
    score: float = 0.0
    score_reasons: list[str] = field(default_factory=list)

    @property
    def canonical_url(self) -> str:
        return canonicalize_url(self.url)

    @property
    def id(self) -> str:
        payload = "|".join(
            [
                self.canonical_url,
                self.company.strip().lower(),
                self.title.strip().lower(),
            ]
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]

    def to_record(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "url": self.url,
            "canonical_url": self.canonical_url,
            "source": self.source,
            "description": self.description,
            "snippet": self.snippet,
            "posted_at": self.posted_at,
            "discovered_at": self.discovered_at,
            "tags": list(self.tags),
            "score": self.score,
            "score_reasons": list(self.score_reasons),
        }


def score_jobs(jobs: list[JobPosting], config: DiscoveryConfig) -> list[JobPosting]:
    scored_jobs: list[JobPosting] = []
    for job in jobs:
        haystack = " ".join(
            part
            for part in [job.title, job.company, job.location, job.description, job.snippet]
            if part
        ).lower()
        score = 0.0
        reasons: list[str] = []
        tags: list[str] = []

        for term in config.include_terms:
            if _contains(haystack, term):
                score += 10
                reasons.append(f"matched: {term}")
                tags.append(term)

        for location in config.locations:
            if _contains(job.location, location) or _contains(haystack, location):
                score += 8
                reasons.append(f"location: {location}")
                break

        if _contains(job.title, "senior"):
            score += 4
            reasons.append("seniority: senior")

        if _contains(job.title, "project manager"):
            score += 6
            reasons.append("role: project manager")

        if job.posted_at:
            score += 5
            reasons.append("has posted date")
        else:
            score += 2
            reasons.append("freshly discovered")

        for term in config.exclude_terms:
            if _contains(haystack, term):
                score -= 25
                reasons.append(f"penalty: {term}")

        job.score = score
        job.score_reasons = reasons
        job.tags = tags
        scored_jobs.append(job)

    return sorted(scored_jobs, key=lambda item: item.score, reverse=True)


class DiscoveryState:
    def __init__(self, discovery_dir: Path | str = DISCOVERY_DIR) -> None:
        self.discovery_dir = Path(discovery_dir)
        self.discovery_dir.mkdir(parents=True, exist_ok=True)
        self.seen_path = self.discovery_dir / "seen.json"
        self.jobs_path = self.discovery_dir / "jobs.jsonl"
        self._seen = self._load_seen()

    def _load_seen(self) -> dict[str, dict[str, Any]]:
        if not self.seen_path.exists():
            return {}
        data = json.loads(self.seen_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("seen.json must contain a JSON object")
        result: dict[str, dict[str, Any]] = {}
        for key, value in data.items():
            if isinstance(value, dict):
                result[str(key)] = dict(value)
        return result

    def filter_new(self, jobs: Iterable[JobPosting]) -> list[JobPosting]:
        fresh: list[JobPosting] = []
        batch_seen: set[str] = set()
        for job in jobs:
            if job.id in self._seen or job.id in batch_seen:
                continue
            batch_seen.add(job.id)
            fresh.append(job)
        return fresh

    def record_jobs(self, jobs: Iterable[JobPosting]) -> None:
        records = list(jobs)
        if not records:
            return

        with self.jobs_path.open("a", encoding="utf-8") as handle:
            for job in records:
                handle.write(json.dumps(job.to_record(), ensure_ascii=False, sort_keys=True))
                handle.write("\n")
                if job.id not in self._seen:
                    self._seen[job.id] = {
                        "discovered_at": job.discovered_at,
                        "canonical_url": job.canonical_url,
                        "title": job.title,
                        "company": job.company,
                    }

        self.seen_path.write_text(
            json.dumps(self._seen, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def _normalize_list(values: Iterable[Any] | None) -> list[str]:
    if not values:
        return []
    return [str(value) for value in values]


def load_config(path: Path | str = DEFAULT_CONFIG) -> DiscoveryConfig:
    config_path = Path(path)
    text = config_path.read_text(encoding="utf-8")
    data: dict[str, Any]
    if yaml is not None:  # pragma: no cover - exercised when PyYAML is available
        loaded = yaml.safe_load(text) or {}
        if not isinstance(loaded, dict):
            raise ValueError("Discovery config must be a mapping")
        data = loaded
    else:
        data = load_simple_yaml(text)

    return DiscoveryConfig(
        queries=_normalize_list(data.get("queries")),
        locations=_normalize_list(data.get("locations")),
        include_terms=_normalize_list(data.get("include_terms")),
        exclude_terms=_normalize_list(data.get("exclude_terms")),
        sources=[dict(source) for source in data.get("sources", []) or []],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Load the job discovery config and report basic counts.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to discovery sources config")
    args = parser.parse_args()

    config = load_config(args.config)
    print(f"Loaded {len(config.sources)} sources, {len(config.queries)} queries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
