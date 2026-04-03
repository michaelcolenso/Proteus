#!/usr/bin/env python3
"""
Application Autopilot
Turns a job posting into a tailored application package recommendation.

Features:
- Analyze job description keywords and ATS match score
- Recommend best CV variant and cover letter template
- Recommend top achievements to emphasize
- Generate an application briefing markdown file
- Optionally append a row to applications/tracker.md
"""

import argparse
import re
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import tomllib as toml_loader
except ModuleNotFoundError:  # pragma: no cover
    toml_loader = None
    import toml as toml_legacy

from analyze_job import JobAnalyzer, load_cv_keywords
PROFILE_TO_VARIANT = {
    "senior_pm": "cv_senior_pm",
    "superintendent": "cv_superintendent",
    "estimator": "cv_estimator",
    "lean_specialist": "cv",
    "multifamily": "cv_senior_pm",
    "luxury_residential": "cv",
}


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return cleaned or "unknown-company"


def extract_company_name(job_text: str) -> str:
    lines = [line.strip() for line in job_text.splitlines() if line.strip()]
    for line in lines[:8]:
        if line.lower().startswith(("company:", "about ", "at ")):
            return line.split(":", 1)[-1].strip()[:80]
    return "Unknown Company"


def choose_best_profile(job_keywords: Dict[str, List[Tuple[str, int]]], metadata: Dict) -> str:
    all_job_terms = set()
    for category in ("roles", "skills", "project_types", "tools", "certifications", "methods"):
        for keyword, _ in job_keywords.get(category, []):
            all_job_terms.add(keyword.lower())

    profiles = metadata.get("keywords", {})
    best_profile = "senior_pm"
    best_score = -1

    for profile_name, profile_data in profiles.items():
        keywords = [k.lower() for k in profile_data.get("injected_keywords_list", [])]
        score = sum(1 for k in keywords if k in all_job_terms)
        if score > best_score:
            best_score = score
            best_profile = profile_name

    return best_profile


def choose_letter_template(job_keywords: Dict[str, List[Tuple[str, int]]]) -> str:
    methods = {k for k, _ in job_keywords.get("methods", [])}
    project_types = {k for k, _ in job_keywords.get("project_types", [])}
    if "multifamily" in project_types:
        return "multifamily"
    if "lean construction" in {m.lower() for m in methods}:
        return "lean_construction"
    return "senior_pm"


def recommended_achievements(achievements: List[Dict], job_keywords: Dict[str, List[Tuple[str, int]]], top_n: int = 8):
    role_tags = {k for k, _ in job_keywords.get("roles", [])}
    skill_tags = {k for k, _ in job_keywords.get("skills", [])}
    project_tags = {k for k, _ in job_keywords.get("project_types", [])}
    all_terms = {t.lower() for t in (role_tags | skill_tags | project_tags)}

    ranked = []
    for achievement in achievements:
        tags = {tag.lower() for tag in achievement.get("tags", [])}
        score = len(tags.intersection(all_terms))
        score += 1 if achievement.get("metric") == "project_value" else 0
        if score > 0:
            ranked.append((score, achievement))

    ranked.sort(key=lambda x: (x[0], x[1].get("year", 0), x[1].get("value_numeric", 0)), reverse=True)
    return [a for _, a in ranked[:top_n]]


def append_tracker_row(tracker_path: Path, row: str):
    content = tracker_path.read_text(encoding="utf-8").splitlines()
    new_lines = []
    inserted = False
    for line in content:
        if not inserted and line.startswith("|  |  |  |  |  |  |  |  |"):
            new_lines.append(row)
            inserted = True
        new_lines.append(line)
    if not inserted:
        new_lines.append(row)
    tracker_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate a tailored application package from a job posting.")
    parser.add_argument("--file", required=True, help="Path to job posting text file")
    parser.add_argument("--output-dir", default="applications/generated", help="Directory for generated brief")
    parser.add_argument("--profile-name", default="autopilot_custom", help="Name for suggested keyword profile")
    parser.add_argument("--update-tracker", action="store_true", help="Append recommendation row to tracker")
    args = parser.parse_args()

    job_text = Path(args.file).read_text(encoding="utf-8")
    metadata_text = Path("metadata.toml").read_text(encoding="utf-8")
    metadata = toml_loader.loads(metadata_text) if toml_loader else toml_legacy.loads(metadata_text)
    analyzer = JobAnalyzer(load_cv_keywords())
    keywords = analyzer.extract_keywords(job_text)
    match = analyzer.calculate_match_score(keywords)
    suggestions = analyzer.suggest_keywords(keywords, top_n=12)
    keyword_profile = analyzer.generate_keyword_profile(keywords, args.profile_name)

    best_profile = choose_best_profile(keywords, metadata)
    cv_variant = PROFILE_TO_VARIANT.get(best_profile, "cv")
    letter_template = choose_letter_template(keywords)

    achievements = []
    achievements_warning = None
    try:
        from achievements import AchievementDatabase

        db = AchievementDatabase()
        achievements = recommended_achievements(db.achievements, keywords)
    except ModuleNotFoundError:
        achievements_warning = (
            "PyYAML is not installed, so achievement ranking was skipped. "
            "Install with: pip install pyyaml"
        )

    company = extract_company_name(job_text)
    today = date.today().isoformat()
    follow_up = (date.today() + timedelta(days=7)).isoformat()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"{today}_{slugify(company)}_autopilot.md"

    lines = [
        f"# Application Autopilot Brief - {company}",
        "",
        f"**Generated**: {today}",
        f"**ATS Match Score (current keyword set)**: {match['score']}%",
        "",
        "## Recommended Package",
        f"- **CV Variant**: `{cv_variant}` (profile: `{best_profile}`)",
        f"- **Cover Letter Template**: `{letter_template}`",
        f"- **Follow-up Date**: {follow_up}",
        "",
        "## Priority Keywords To Add/Emphasize",
    ]

    for keyword, score, category, freq in suggestions[:10]:
        lines.append(f"- {keyword.title()} ({category}, {freq}x, weighted score {score:.1f})")

    lines.extend(["", "## Recommended Achievement Evidence"])
    if achievements:
        for achievement in achievements:
            lines.append(
                f"- `{achievement.get('id')}`: {achievement.get('value')} — "
                f"{achievement.get('project', achievement.get('company', 'N/A'))} ({achievement.get('year', 'N/A')})"
            )
    else:
        lines.append("- Achievement ranking unavailable in this environment.")
        if achievements_warning:
            lines.append(f"- Note: {achievements_warning}")

    lines.extend(
        [
            "",
            "## Suggested Commands",
            f"- `./generate.sh {cv_variant.replace('cv_', '') if cv_variant != 'cv' else 'cv'}`",
            f"- `cp letters/{letter_template}.typ letter.typ`",
            "- `typst compile letter.typ`",
            "",
            "## Suggested Keyword Profile Snippet",
            "```toml",
            keyword_profile.rstrip(),
            "```",
            "",
        ]
    )

    out_file.write_text("\n".join(lines), encoding="utf-8")

    if args.update_tracker:
        tracker_path = Path("applications/tracker.md")
        row = (
            f"| {today} | {company} | [Role from posting] | {cv_variant} | {letter_template} "
            f"| Applied | Follow up {follow_up} | Added via autopilot |"
        )
        append_tracker_row(tracker_path, row)

    print(f"Created autopilot brief: {out_file}")
    print(f"Recommendation: CV={cv_variant}, Letter={letter_template}, Match={match['score']}%")


if __name__ == "__main__":
    main()
