#!/usr/bin/env python3
"""
Automated Job Search & Application Pipeline

This script ties together the keyword analysis and CV export workflow into a
single command. It generates:

1) A Markdown analysis report under applications/reports/
2) A TOML keyword profile snippet under applications/keywords/
3) Optional CV exports for a selected .typ variant

Usage:
    ./scripts/job_pipeline.py --file sample_job_posting.txt --variant cv_senior_pm.typ
    ./scripts/job_pipeline.py --text "Senior Project Manager..." --company "ACME" --title "Senior PM"
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import toml

from analyze_job import JobAnalyzer
from export_cv import CVExporter


REPORTS_DIR = Path("applications/reports")
KEYWORDS_DIR = Path("applications/keywords")


def slugify(value: str) -> str:
    """Create a filesystem-friendly slug."""
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "job"


def load_job_text(file_path: str | None, inline_text: str | None) -> str:
    """Load job text from a file or inline text."""
    if file_path:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Job posting file not found: {file_path}")
        return path.read_text(encoding="utf-8")
    if inline_text:
        return inline_text
    raise ValueError("Provide either --file or --text")


def load_cv_keywords(metadata_path: str = "metadata.toml") -> List[str]:
    """Load the current injected keyword list from metadata.toml."""
    metadata = toml.load(metadata_path)
    inject = metadata.get("inject", {})
    return list(inject.get("injected_keywords_list", []))


def pick_top_keywords(job_keywords: Dict[str, List[Tuple[str, int]]], limit: int) -> List[str]:
    """Pick top keywords across categories by frequency."""
    scored: List[Tuple[str, int]] = []
    for category, entries in job_keywords.items():
        if category in {"requirements", "numbers"}:
            continue
        scored.extend(entries)
    scored.sort(key=lambda item: item[1], reverse=True)

    ordered: List[str] = []
    seen = set()
    for keyword, _count in scored:
        if keyword in seen:
            continue
        seen.add(keyword)
        ordered.append(keyword)
        if len(ordered) >= limit:
            break
    return ordered


def format_keyword_section(title: str, entries: Sequence[Tuple[str, int]]) -> str:
    """Format a keyword section for the report."""
    if not entries:
        return f"#### {title}\n\n- None detected\n"
    lines = [f"#### {title}", ""]
    lines.extend(f"- {keyword} ({count})" for keyword, count in entries)
    lines.append("")
    return "\n".join(lines)


def build_keyword_profile(keywords: Iterable[str]) -> Dict[str, Dict[str, List[str]]]:
    """Build a TOML-compatible keyword profile structure."""
    return {
        "inject": {
            "inject_keywords": True,
            "injected_keywords_list": list(dict.fromkeys(keywords)),
        }
    }


def format_toml_profile(profile: Dict[str, Dict[str, List[str]]]) -> str:
    """Render the keyword profile as TOML."""
    return toml.dumps(profile)


@dataclass
class PipelineOutputs:
    report_path: Path
    keyword_path: Path
    match_score: float
    suggested_keywords: List[str]
    missing_keywords: List[str]
    exports: List[Path]


def ensure_directories() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    KEYWORDS_DIR.mkdir(parents=True, exist_ok=True)


def run_exports(variant: str | None, formats: Sequence[str]) -> List[Path]:
    """Run CV exports if the variant exists and typst is available."""
    if not variant:
        return []

    variant_path = Path(variant)
    if not variant_path.exists():
        raise FileNotFoundError(f"Variant not found: {variant}")

    if not shutil.which("typst"):
        print("Warning: typst not installed; skipping exports.")
        return []

    exporter = CVExporter(str(variant_path))
    return exporter.export_multiple(list(formats))


def render_report(
    *,
    company: str,
    title: str,
    source_label: str,
    job_keywords: Dict[str, List[Tuple[str, int]]],
    match: Dict[str, object],
    suggested_keywords: Sequence[str],
    keyword_file: Path,
    exports: Sequence[Path],
) -> str:
    """Render the Markdown report."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# Job Analysis: {title} @ {company}",
        "",
        f"- Generated: {timestamp}",
        f"- Source: {source_label}",
        f"- ATS Match Score: **{match['score']}%** ({match['matched_keywords']}/{match['total_job_keywords']})",
        "",
        "## Top Suggested Keywords",
        "",
    ]

    if suggested_keywords:
        lines.extend(f"- {kw}" for kw in suggested_keywords)
    else:
        lines.append("- No suggestions (no missing keywords detected).")

    lines.extend(
        [
            "",
            "## Missing Keywords",
            "",
        ]
    )
    missing = match.get("missing", [])
    if missing:
        lines.extend(f"- {kw}" for kw in missing)
    else:
        lines.append("- None 🎉")

    lines.extend(
        [
            "",
            "## Keyword Breakdown",
            "",
            format_keyword_section("Roles", job_keywords.get("roles", [])),
            format_keyword_section("Skills", job_keywords.get("skills", [])),
            format_keyword_section("Project Types", job_keywords.get("project_types", [])),
            format_keyword_section("Tools", job_keywords.get("tools", [])),
            format_keyword_section("Certifications", job_keywords.get("certifications", [])),
            format_keyword_section("Methods", job_keywords.get("methods", [])),
        ]
    )

    lines.extend(
        [
            "",
            "## Next Steps",
            "",
            f"1. Review and merge keywords from `{keyword_file}` into `metadata.toml`.",
            "2. Re-run `./generate.sh cv` (or export) after updating keywords.",
        ]
    )

    if exports:
        lines.extend(["", "## Generated Exports", ""])
        lines.extend(f"- {path}" for path in exports)

    return "\n".join(lines).rstrip() + "\n"


def run_pipeline(args: argparse.Namespace) -> PipelineOutputs:
    ensure_directories()

    job_text = load_job_text(args.file, args.text)
    cv_keywords = load_cv_keywords(args.metadata)

    analyzer = JobAnalyzer(cv_keywords=cv_keywords)
    job_keywords = analyzer.extract_keywords(job_text)
    match = analyzer.calculate_match_score(job_keywords)

    suggestions_raw = analyzer.suggest_keywords(job_keywords, top_n=args.suggestions)
    suggested_keywords = [keyword for keyword, *_rest in suggestions_raw]
    top_keywords = pick_top_keywords(job_keywords, limit=args.profile_size)

    profile_keywords = list(dict.fromkeys([*cv_keywords, *top_keywords]))
    profile = build_keyword_profile(profile_keywords)

    company = args.company or "Unknown Company"
    title = args.title or "Unknown Title"
    slug = slugify(f"{company}-{title}")

    report_path = REPORTS_DIR / f"{slug}.md"
    keyword_path = KEYWORDS_DIR / f"{slug}.toml"

    keyword_path.write_text(format_toml_profile(profile), encoding="utf-8")

    source_label = args.file or "inline text"
    exports = run_exports(args.variant, args.formats)

    report = render_report(
        company=company,
        title=title,
        source_label=source_label,
        job_keywords=job_keywords,
        match=match,
        suggested_keywords=suggested_keywords,
        keyword_file=keyword_path,
        exports=exports,
    )
    report_path.write_text(report, encoding="utf-8")

    return PipelineOutputs(
        report_path=report_path,
        keyword_path=keyword_path,
        match_score=float(match["score"]),
        suggested_keywords=list(suggested_keywords),
        missing_keywords=list(match.get("missing", [])),
        exports=list(exports),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Automate job analysis and CV exports")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", help="Path to a job posting text file")
    source.add_argument("--text", help="Inline job posting text")

    parser.add_argument("--company", help="Company name for report naming")
    parser.add_argument("--title", help="Job title for report naming")
    parser.add_argument("--variant", help="Typst CV variant to export (e.g., cv_senior_pm.typ)")
    parser.add_argument(
        "--formats",
        nargs="+",
        default=["pdf", "txt"],
        help="Export formats to generate when --variant is provided",
    )
    parser.add_argument("--metadata", default="metadata.toml", help="Path to metadata.toml")
    parser.add_argument("--suggestions", type=int, default=12, help="Number of keyword suggestions")
    parser.add_argument(
        "--profile-size",
        type=int,
        default=20,
        help="Number of top job keywords to merge into the keyword profile",
    )
    parser.add_argument(
        "--print-json",
        action="store_true",
        help="Print a machine-readable JSON summary",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    outputs = run_pipeline(args)

    summary = {
        "report": str(outputs.report_path),
        "keyword_profile": str(outputs.keyword_path),
        "match_score": outputs.match_score,
        "suggested_keywords": outputs.suggested_keywords,
        "missing_keywords": outputs.missing_keywords,
        "exports": [str(p) for p in outputs.exports],
    }

    if args.print_json:
        print(json.dumps(summary, indent=2))
    else:
        print("Generated report:", outputs.report_path)
        print("Generated keyword profile:", outputs.keyword_path)
        print(f"ATS match score: {outputs.match_score}%")
        if outputs.exports:
            print("Generated exports:")
            for path in outputs.exports:
                print(" -", path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
