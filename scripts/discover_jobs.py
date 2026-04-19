#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

DEFAULT_CONFIG = Path("applications/discovery/sources.yaml")
DISCOVERY_DIR = Path("applications/discovery")
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
