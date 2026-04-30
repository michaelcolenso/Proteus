#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Iterable

try:
    import tomllib as toml_loader
except ModuleNotFoundError:  # pragma: no cover
    toml_loader = None
    import toml as toml_legacy

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[0]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from analyze_job import JobAnalyzer, load_cv_keywords  # noqa: E402
from application_autopilot import PROFILE_TO_VARIANT, choose_best_profile, choose_letter_template, recommended_achievements  # noqa: E402
from discover_jobs import DISCOVERY_DIR, JobPosting  # noqa: E402

DEFAULT_JOBS_PATH = DISCOVERY_DIR / "jobs.jsonl"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "applications/packages"
NOISE_TERMS = (
    ".serp-page",
    "assistant project manager",
    "atlanta",
    "civil engineer",
    "rail transit",
    "rail project",
    "electrical",
    "lexington",
    "mechanical",
    "software",
    "product manager",
    "program manager",
    "account executive",
    "coordinator",
    "salaries",
)


@dataclass
class ApplicationPackage:
    job: JobPosting
    cv_variant: str
    letter_template: str
    match_score: float
    output_dir: Path
    compiled_files: list[Path] | None = None


def slugify(value: str) -> str:
    cleaned = []
    last_dash = False
    for char in value.lower():
        if char.isalnum():
            cleaned.append(char)
            last_dash = False
        elif not last_dash:
            cleaned.append("-")
            last_dash = True
    return "".join(cleaned).strip("-") or "unknown"


def package_slug(job: JobPosting) -> str:
    return f"{slugify(job.company)}-{slugify(job.title)}"[:100].rstrip("-")


def load_ranked_jobs(path: Path | str = DEFAULT_JOBS_PATH) -> list[JobPosting]:
    jobs_path = Path(path)
    jobs: list[JobPosting] = []
    if not jobs_path.exists():
        return jobs

    for line in jobs_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        jobs.append(job_from_record(record))

    return sorted(jobs, key=lambda job: job.score, reverse=True)


def job_from_record(record: dict[str, Any]) -> JobPosting:
    fields = {
        "title": str(record.get("title", "")),
        "company": str(record.get("company", "")),
        "location": str(record.get("location", "")),
        "url": str(record.get("url", "")),
        "source": str(record.get("source", "")),
        "description": str(record.get("description", "") or ""),
        "snippet": str(record.get("snippet", "") or ""),
        "posted_at": record.get("posted_at"),
        "discovered_at": str(record.get("discovered_at", "")) or None,
        "tags": list(record.get("tags", []) or []),
        "score": float(record.get("score", 0.0) or 0.0),
        "score_reasons": list(record.get("score_reasons", []) or []),
    }
    if fields["discovered_at"] is None:
        fields.pop("discovered_at")
    return JobPosting(**fields)


def select_application_jobs(
    jobs: Iterable[JobPosting],
    limit: int,
    min_score: float = 25.0,
    include_noisy: bool = False,
) -> list[JobPosting]:
    selected: list[JobPosting] = []
    for job in jobs:
        if job.score < min_score:
            continue
        if not include_noisy and is_noisy_job(job):
            continue
        selected.append(job)
        if limit > 0 and len(selected) >= limit:
            break
    return selected


def is_noisy_job(job: JobPosting) -> bool:
    title = job.title.strip().lower()
    haystack = " ".join([job.title, job.company, job.location, job.description, job.snippet]).lower()
    if any(term in haystack for term in NOISE_TERMS):
        return True
    if "{" in title or "}" in title or len(title) > 120:
        return True
    if "jobs in " in title:
        return True
    if job.company == "Multiple employers" and not (job.description or job.snippet):
        generic_titles = {
            "project manager",
            "project manager construction",
            "construction project manager",
            "what: construction project manager",
            "project manager jobs",
        }
        if title in generic_titles:
            return True
    return False


def job_text(job: JobPosting) -> str:
    lines = [
        f"Company: {job.company}",
        f"Title: {job.title}",
        f"Location: {job.location}",
        f"Source: {job.source}",
        f"URL: {job.url}",
        f"Discovery score: {job.score:.1f}",
    ]
    detail = job.description or job.snippet
    if detail:
        lines.extend(["", detail.strip()])
    return "\n".join(lines).rstrip() + "\n"


def recommend_package(job: JobPosting, metadata: dict[str, Any], repo_root: Path) -> tuple[str, str, float, dict[str, Any]]:
    analyzer = JobAnalyzer(load_cv_keywords(str(repo_root / "metadata.toml")))
    keywords = analyzer.extract_keywords(job_text(job))
    match = analyzer.calculate_match_score(keywords)
    best_profile = choose_best_profile(keywords, metadata)
    cv_variant = PROFILE_TO_VARIANT.get(best_profile, "cv_senior_pm")
    letter_template = choose_letter_template(keywords)
    return cv_variant, letter_template, float(match["score"]), keywords


def load_metadata(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    text = (repo_root / "metadata.toml").read_text(encoding="utf-8")
    if toml_loader:
        return toml_loader.loads(text)
    return toml_legacy.loads(text)


def typst_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def typst_text(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("$", "\\$")
        .replace("#", "\\#")
        .replace("[", "\\[")
        .replace("]", "\\]")
    )


def draft_cover_letter_typ(
    job: JobPosting,
    letter_template: str,
    repo_root: Path = REPO_ROOT,
    base_dir: Path | None = None,
) -> str:
    company = job.company if job.company and job.company != "Multiple employers" else "the hiring team"
    role = job.title or "Construction Project Manager"
    focus = letter_focus(job, letter_template)
    paragraph_two = evidence_paragraph(job, letter_template)
    paragraph_three = closing_paragraph(company)
    subject = f"Re: {role} Position"
    recipient_name = company if company != "the hiring team" else "Hiring Manager"
    metadata_path = typst_path(repo_root / "metadata.toml", base_dir)
    signature_path = typst_path(repo_root / "src/signature.png", base_dir)

    return f'''// Generated application cover letter
#import "@preview/brilliant-cv:2.0.3": letter
#let metadata = toml("{typst_string(metadata_path)}")

#show: letter.with(
  metadata,
  myAddress: "Seattle, Washington",
  recipientName: "{typst_string(recipient_name)}",
  recipientAddress: "{typst_string(job.location or "Seattle, WA")}",
  date: datetime.today().display("[month repr:long] [day], [year]"),
  subject: "{typst_string(subject)}",
  signature: image("{typst_string(signature_path)}"),
)

#set par(leading: 0.65em, spacing: 1.2em, justify: true, first-line-indent: 0pt)
#set text(size: 11pt, font: metadata.layout.fonts.regular_fonts.at(0))

Dear Hiring Manager,

{typst_text(focus)}

{typst_text(paragraph_two)}

{typst_text(paragraph_three)}

I'd welcome a conversation about how I can contribute.

#v(1.2em)

Best,

Mike
'''


def typst_path(target: Path, base_dir: Path | None = None) -> str:
    if base_dir is None:
        return str(target)
    return Path(target).resolve().relative_to(base_dir.resolve(), walk_up=True).as_posix()


def letter_focus(job: JobPosting, letter_template: str) -> str:
    company = job.company if job.company and job.company != "Multiple employers" else "your team"
    role = job.title or "this role"
    if letter_template == "multifamily":
        return (
            f"I'm interested in the {role} role with {company}. My background includes hands-on delivery of multifamily, "
            "mixed-use, hospitality, and high-end residential projects where schedule discipline, owner communication, "
            "budget control, and field coordination all mattered every day."
        )
    if letter_template == "lean_construction":
        return (
            f"I'm interested in the {role} role with {company}. I bring a construction management background grounded in "
            "collaborative planning, Last Planner System habits, direct trade coordination, and steady communication with "
            "owners, design teams, and field leadership."
        )
    return (
        f"I'm interested in the {role} role with {company}. I bring 20+ years of construction management experience across "
        "commercial interiors, multifamily, hospitality, senior living, high-rise, and luxury residential work."
    )


def evidence_paragraph(job: JobPosting, letter_template: str) -> str:
    text = " ".join([job.title, job.description, job.snippet]).lower()
    if letter_template == "multifamily" or "multifamily" in text:
        return (
            "At STS Construction, I led a Seattle multifamily project with full responsibility for budget, schedule, "
            "subcontractor coordination, client communication, quality, and safety. Earlier work on mixed-use and hospitality "
            "projects strengthened the same fundamentals: clear planning, early issue resolution, and calm execution under pressure."
        )
    if "superintendent" in text:
        return (
            "I have spent much of my career close to the field, coordinating trades, sequencing work, managing safety expectations, "
            "and keeping owners informed before small issues become project problems. That field-first perspective helps me lead "
            "teams with practical judgment and accountability."
        )
    if "estimator" in text or "preconstruction" in text:
        return (
            "My experience includes estimating, value engineering, buyout, cost forecasting, and change management on projects from "
            "small negotiated work to large technical builds. I understand how early scope clarity and disciplined cost control protect "
            "both the project and the client relationship."
        )
    return (
        "I lead projects by combining strong field presence with disciplined scheduling, budget ownership, subcontractor coordination, "
        "and direct client communication. Teams rely on me for predictable planning, fast problem-solving, and a clear understanding "
        "of what needs to happen next."
    )


def closing_paragraph(company: str) -> str:
    if company == "the hiring team":
        return (
            "The role looks aligned with the kind of work I do best: leading construction teams, protecting schedule and budget, "
            "and keeping stakeholders confident from preconstruction through closeout."
        )
    return (
        f"{company}'s work appears aligned with the kind of projects I do best: complex construction where planning, field execution, "
        "cost control, and client trust all have to hold together."
    )


def build_application_package(job: JobPosting, output_root: Path, repo_root: Path = REPO_ROOT) -> ApplicationPackage:
    metadata = load_metadata(repo_root)
    cv_variant, letter_template, match_score, _keywords = recommend_package(job, metadata, repo_root)
    output_dir = output_root / date.today().isoformat() / f"{package_slug(job)}-{job.id}"
    return ApplicationPackage(
        job=job,
        cv_variant=cv_variant,
        letter_template=letter_template,
        match_score=match_score,
        output_dir=output_dir,
    )


def write_application_package(package: ApplicationPackage, repo_root: Path = REPO_ROOT, compile_outputs: bool = True) -> None:
    package.output_dir.mkdir(parents=True, exist_ok=True)
    (package.output_dir / "job_posting.txt").write_text(job_text(package.job), encoding="utf-8")
    (package.output_dir / "cover_letter.typ").write_text(
        draft_cover_letter_typ(package.job, package.letter_template, repo_root, base_dir=package.output_dir),
        encoding="utf-8",
    )
    (package.output_dir / "application.md").write_text(application_markdown(package), encoding="utf-8")

    compiled: list[Path] = []
    if compile_outputs:
        compiled.extend(compile_package_outputs(package, repo_root))
    package.compiled_files = compiled


def application_markdown(package: ApplicationPackage) -> str:
    follow_up = (date.today() + timedelta(days=7)).isoformat()
    job = package.job
    return "\n".join(
        [
            f"# {job.company} - {job.title}",
            "",
            f"**Prepared**: {date.today().isoformat()}",
            f"**Job URL**: {job.url}",
            f"**Location**: {job.location or 'Unknown'}",
            f"**Discovery Score**: {job.score:.1f}",
            f"**ATS Match Score**: {package.match_score:.1f}%",
            f"**CV Variant**: `{package.cv_variant}`",
            f"**Cover Letter Template**: `{package.letter_template}`",
            f"**Follow-up Target**: {follow_up}",
            "",
            "## Discovery Reasons",
            *(f"- {reason}" for reason in package.job.score_reasons),
            "",
            "## Package Files",
            "- `job_posting.txt`",
            "- `cover_letter.typ`",
            "- `cover_letter.pdf` when compiled",
            "- `cv.pdf` when compiled",
            "",
        ]
    )


def compile_package_outputs(package: ApplicationPackage, repo_root: Path) -> list[Path]:
    if not shutil.which("typst"):
        return []

    compiled: list[Path] = []
    typst_root = Path(os.path.commonpath([repo_root.resolve(), package.output_dir.resolve()]))
    cv_source = repo_root / f"{package.cv_variant}.typ"
    if not cv_source.exists():
        cv_source = repo_root / "cv.typ"
    cv_output = package.output_dir / "cv.pdf"
    subprocess.run(["typst", "compile", "--root", str(typst_root), str(cv_source), str(cv_output)], cwd=repo_root, check=True)
    compiled.append(cv_output)

    letter_source = package.output_dir / "cover_letter.typ"
    letter_output = package.output_dir / "cover_letter.pdf"
    subprocess.run(["typst", "compile", "--root", str(typst_root), str(letter_source), str(letter_output)], cwd=repo_root, check=True)
    compiled.append(letter_output)
    return compiled


def write_manifest(packages: Iterable[ApplicationPackage], output_dir: Path) -> Path:
    package_list = list(packages)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "manifest.md"
    lines = [
        "# Prepared Application Packages",
        "",
        f"Generated: {date.today().isoformat()}",
        f"Packages: {len(package_list)}",
        "",
        "| Company | Position | Score | CV | Letter | Folder |",
        "|---------|----------|-------|----|--------|--------|",
    ]
    for package in package_list:
        job = package.job
        lines.append(
            f"| {job.company} | {job.title} | {job.score:.1f} | `{package.cv_variant}` | "
            f"`{package.letter_template}` | `{package.output_dir.name}` |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def append_tracker_rows(packages: Iterable[ApplicationPackage], tracker_path: Path = REPO_ROOT / "applications/tracker.md") -> None:
    if not tracker_path.exists():
        return
    content = [
        line
        for line in tracker_path.read_text(encoding="utf-8").splitlines()
        if f"Package: applications/packages/{date.today().isoformat()}/" not in line
    ]
    rows = [tracker_row(package) for package in packages]
    output: list[str] = []
    inserted = False
    for line in content:
        if not inserted and line.startswith("|  |  |  |  |  |  |  |  |"):
            output.extend(rows)
            inserted = True
        output.append(line)
    if not inserted:
        output.extend(rows)
    tracker_path.write_text("\n".join(output) + "\n", encoding="utf-8")


def tracker_row(package: ApplicationPackage) -> str:
    follow_up = (date.today() + timedelta(days=7)).isoformat()
    folder = package.output_dir.relative_to(REPO_ROOT) if package.output_dir.is_relative_to(REPO_ROOT) else package.output_dir
    return (
        f"| {date.today().isoformat()} | {package.job.company} | {package.job.title} | {package.cv_variant} | "
        f"{package.letter_template} | Prepared | Follow up {follow_up} | Package: {folder} |"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare CV and cover-letter packages from discovered jobs.")
    parser.add_argument("--jobs", default=str(DEFAULT_JOBS_PATH), help="Path to discovery jobs.jsonl")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT), help="Root directory for application packages")
    parser.add_argument("--limit", type=int, default=25, help="Maximum packages to prepare; use 0 with --all for every selected job")
    parser.add_argument("--min-score", type=float, default=25.0, help="Minimum discovery score to package")
    parser.add_argument("--all", action="store_true", help="Prepare all jobs above min-score")
    parser.add_argument("--include-noisy", action="store_true", help="Include obvious noisy matches such as rail/electrical roles")
    parser.add_argument("--no-compile", action="store_true", help="Write sources only; skip PDF compilation")
    parser.add_argument("--update-tracker", action="store_true", help="Append prepared packages to applications/tracker.md")
    args = parser.parse_args()

    ranked_jobs = load_ranked_jobs(args.jobs)
    limit = 0 if args.all else args.limit
    selected = select_application_jobs(
        ranked_jobs,
        limit=limit,
        min_score=args.min_score,
        include_noisy=args.include_noisy,
    )

    output_root = Path(args.output_root)
    packages = [build_application_package(job, output_root, REPO_ROOT) for job in selected]
    for package in packages:
        write_application_package(package, REPO_ROOT, compile_outputs=not args.no_compile)

    manifest = write_manifest(packages, output_root / date.today().isoformat())
    if args.update_tracker:
        append_tracker_rows(packages)

    print(f"Prepared {len(packages)} application packages; wrote {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
