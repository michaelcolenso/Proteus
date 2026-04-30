#!/usr/bin/env python3
"""Local dashboard for discovery, application packages, and tracker status."""

from __future__ import annotations

import argparse
import html
import mimetypes
import subprocess
import sys
import urllib.parse
from dataclasses import dataclass
from datetime import date
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[0]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from discover_jobs import DISCOVERY_DIR, JobPosting  # noqa: E402
from prepare_applications import (  # noqa: E402
    DEFAULT_OUTPUT_ROOT,
    build_application_package,
    load_ranked_jobs,
    tracker_row,
    write_application_package,
)

DEFAULT_TRACKER_PATH = REPO_ROOT / "applications/tracker.md"
VALID_STATUSES = {"Prepared", "Applied", "Skipped", "Withdrawn", "Rejected"}


@dataclass
class DashboardPaths:
    jobs_path: Path = DISCOVERY_DIR / "jobs.jsonl"
    packages_root: Path = DEFAULT_OUTPUT_ROOT
    tracker_path: Path = DEFAULT_TRACKER_PATH
    repo_root: Path = REPO_ROOT


@dataclass
class TrackerRow:
    date: str
    company: str
    position: str
    cv_variant: str
    letter: str
    status: str
    next_step: str
    notes: str
    package_path: str | None = None


@dataclass
class PackageSummary:
    company: str
    position: str
    job_url: str
    discovery_score: str
    ats_score: str
    cv_variant: str
    letter_template: str
    output_dir: Path
    relative_path: str
    has_cv: bool
    has_letter: bool
    status: str


@dataclass
class DashboardStats:
    discovered_count: int
    prepared_count: int
    tracker_count: int
    applied_count: int


@dataclass
class DashboardState:
    jobs: list[JobPosting]
    packages: list[PackageSummary]
    tracker_rows: list[TrackerRow]
    stats: DashboardStats


def parse_tracker_rows(content: str) -> list[TrackerRow]:
    rows: list[TrackerRow] = []
    in_active = False
    saw_active_heading = "## Active Applications" in content
    for line in content.splitlines():
        if line.startswith("## Active Applications"):
            in_active = True
            continue
        if in_active and line.startswith("## "):
            break
        if saw_active_heading and not in_active:
            continue
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            continue
        if cells[0] in {"Date", ""} or set(cells[0]) == {"-"}:
            continue
        package_path = extract_package_path(cells[7])
        rows.append(
            TrackerRow(
                date=cells[0],
                company=cells[1],
                position=cells[2],
                cv_variant=cells[3],
                letter=cells[4],
                status=cells[5],
                next_step=cells[6],
                notes=cells[7],
                package_path=package_path,
            )
        )
    return rows


def extract_package_path(notes: str) -> str | None:
    marker = "Package:"
    if marker not in notes:
        return None
    return notes.split(marker, 1)[1].strip()


def update_tracker_status(tracker_path: Path, package_path: str, status: str) -> bool:
    if status not in VALID_STATUSES:
        raise ValueError(f"Unsupported status: {status}")
    if not tracker_path.exists():
        return False

    changed = False
    output: list[str] = []
    for line in tracker_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("|") and f"Package: {package_path}" in line:
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) == 8:
                cells[5] = status
                if status == "Applied":
                    cells[6] = f"Follow up {date.today().isoformat()}"
                if status == "Skipped":
                    cells[6] = "No follow-up"
                line = "| " + " | ".join(cells) + " |"
                changed = True
        output.append(line)
    tracker_path.write_text("\n".join(output) + "\n", encoding="utf-8")
    return changed


def upsert_tracker_row(tracker_path: Path, row: str) -> None:
    package_path = extract_package_path(row)
    if not tracker_path.exists() or not package_path:
        return

    lines = tracker_path.read_text(encoding="utf-8").splitlines()
    output: list[str] = []
    replaced = False
    inserted = False
    for line in lines:
        if f"Package: {package_path}" in line:
            if not replaced:
                output.append(row)
                replaced = True
            continue
        if not replaced and not inserted and line.startswith("|  |  |  |  |  |  |  |  |"):
            output.append(row)
            inserted = True
        output.append(line)

    if not replaced and not inserted:
        output.append(row)
    tracker_path.write_text("\n".join(output) + "\n", encoding="utf-8")


def load_dashboard_state(paths: DashboardPaths = DashboardPaths()) -> DashboardState:
    jobs = load_ranked_jobs(paths.jobs_path)
    tracker_rows = parse_tracker_rows(paths.tracker_path.read_text(encoding="utf-8")) if paths.tracker_path.exists() else []
    tracker_by_package = {row.package_path: row for row in tracker_rows if row.package_path}
    packages = load_packages(paths, tracker_by_package)
    stats = DashboardStats(
        discovered_count=len(jobs),
        prepared_count=len(packages),
        tracker_count=len(tracker_rows),
        applied_count=sum(1 for row in tracker_rows if row.status == "Applied"),
    )
    return DashboardState(jobs=jobs, packages=packages, tracker_rows=tracker_rows, stats=stats)


def load_packages(paths: DashboardPaths, tracker_by_package: dict[str | None, TrackerRow]) -> list[PackageSummary]:
    if not paths.packages_root.exists():
        return []
    packages: list[PackageSummary] = []
    for application_file in sorted(paths.packages_root.glob("*/*/application.md"), reverse=True):
        output_dir = application_file.parent
        relative = relative_to_repo(output_dir, paths.repo_root)
        fields = parse_application_markdown(application_file.read_text(encoding="utf-8"))
        tracker = tracker_by_package.get(relative)
        packages.append(
            PackageSummary(
                company=fields.get("company", output_dir.name),
                position=fields.get("position", ""),
                job_url=fields.get("Job URL", ""),
                discovery_score=fields.get("Discovery Score", ""),
                ats_score=fields.get("ATS Match Score", ""),
                cv_variant=fields.get("CV Variant", ""),
                letter_template=fields.get("Cover Letter Template", ""),
                output_dir=output_dir,
                relative_path=relative,
                has_cv=(output_dir / "cv.pdf").exists(),
                has_letter=(output_dir / "cover_letter.pdf").exists(),
                status=tracker.status if tracker else "Prepared",
            )
        )
    return packages


def parse_application_markdown(content: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in content.splitlines():
        if line.startswith("# "):
            heading = line[2:].strip()
            if " - " in heading:
                fields["company"], fields["position"] = heading.split(" - ", 1)
            else:
                fields["position"] = heading
        elif line.startswith("**") and "**:" in line:
            label, value = line.split("**:", 1)
            fields[label.strip("*")] = value.strip().strip("`")
    return fields


def relative_to_repo(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def prepare_job_by_id(job_id: str, paths: DashboardPaths, compile_outputs: bool = True) -> Path | None:
    jobs = load_ranked_jobs(paths.jobs_path)
    matches = [job for job in jobs if job.id == job_id]
    if not matches:
        return None
    package = build_application_package(matches[0], paths.packages_root, paths.repo_root)
    write_application_package(package, paths.repo_root, compile_outputs=compile_outputs)
    upsert_tracker_row(paths.tracker_path, tracker_row(package))
    return package.output_dir


CSS = """
:root { color-scheme: light; --ink: #171717; --muted: #686f76; --line: #d9ded8; --paper: #f5f5f2; --panel: #ffffff; --accent: #0f766e; --warn: #a16207; --bad: #b91c1c; }
* { box-sizing: border-box; }
body { margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: var(--ink); background: var(--paper); }
a { color: inherit; }
button, .button { border: 1px solid var(--ink); border-radius: 6px; background: var(--ink); color: #fff; padding: 8px 10px; font: inherit; font-weight: 650; cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; min-height: 36px; }
button.secondary, .button.secondary { background: transparent; color: var(--ink); }
button.subtle { background: transparent; border-color: var(--line); color: var(--muted); }
.page { max-width: 1440px; margin: 0 auto; padding: 24px; }
header { display: flex; justify-content: space-between; gap: 16px; align-items: end; border-bottom: 1px solid var(--line); padding-bottom: 18px; }
h1 { margin: 0; font-size: 32px; line-height: 1.05; letter-spacing: 0; }
p { margin: 0; color: var(--muted); line-height: 1.45; }
.stats { display: grid; grid-template-columns: repeat(4, minmax(120px, 1fr)); gap: 1px; background: var(--line); border: 1px solid var(--line); margin: 20px 0; }
.stat { background: var(--panel); padding: 14px; }
.stat strong { display: block; font-size: 26px; line-height: 1; }
.stat span { color: var(--muted); font-size: 13px; }
.grid { display: grid; grid-template-columns: minmax(280px, 0.9fr) minmax(420px, 1.3fr) minmax(300px, 0.9fr); gap: 18px; align-items: start; }
section { min-width: 0; }
h2 { margin: 0 0 12px; font-size: 15px; text-transform: uppercase; letter-spacing: 0; }
.list { display: grid; gap: 10px; }
.item { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 14px; }
.item h3 { margin: 0 0 6px; font-size: 17px; line-height: 1.25; letter-spacing: 0; overflow-wrap: anywhere; }
.meta { display: flex; flex-wrap: wrap; gap: 8px; margin: 8px 0 12px; }
.pill { border: 1px solid var(--line); border-radius: 999px; padding: 3px 8px; color: var(--muted); font-size: 12px; }
.status { color: var(--accent); border-color: color-mix(in srgb, var(--accent), white 65%); }
.actions { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
form { margin: 0; display: inline; }
.empty { border: 1px dashed var(--line); border-radius: 8px; padding: 18px; background: rgba(255,255,255,.45); }
.tracker-table { width: 100%; border-collapse: collapse; background: var(--panel); border: 1px solid var(--line); }
.tracker-table th, .tracker-table td { text-align: left; border-bottom: 1px solid var(--line); padding: 8px; vertical-align: top; font-size: 13px; }
.tracker-table th { color: var(--muted); font-weight: 650; }
@media (max-width: 1080px) { .grid { grid-template-columns: 1fr; } .stats { grid-template-columns: repeat(2, 1fr); } header { align-items: start; flex-direction: column; } }
@media (max-width: 560px) { .page { padding: 14px; } .stats { grid-template-columns: 1fr; } h1 { font-size: 27px; } }
"""


def render_dashboard(state: DashboardState, message: str = "") -> str:
    message_html = f"<p>{html.escape(message)}</p>" if message else "<p>Review matches, open packages, and update status.</p>"
    jobs_html = render_jobs(state.jobs[:30])
    packages_html = render_packages(state.packages)
    tracker_html = render_tracker(state.tracker_rows)
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Proteus Applications</title><style>{CSS}</style></head>
<body><main class="page">
<header>
  <div><h1>Proteus Applications</h1>{message_html}</div>
  <div class="actions">
    <form method="post" action="/run-discovery"><button class="secondary" type="submit">Run discovery</button></form>
    <form method="post" action="/prepare-all"><button type="submit">Prepare matches</button></form>
  </div>
</header>
<div class="stats">
  <div class="stat"><strong>{state.stats.discovered_count}</strong><span>Discovered</span></div>
  <div class="stat"><strong>{state.stats.prepared_count}</strong><span>Packages</span></div>
  <div class="stat"><strong>{state.stats.tracker_count}</strong><span>Tracker rows</span></div>
  <div class="stat"><strong>{state.stats.applied_count}</strong><span>Applied</span></div>
</div>
<div class="grid">
  <section><h2>Discovered Matches</h2>{jobs_html}</section>
  <section><h2>Prepared Packages</h2>{packages_html}</section>
  <section><h2>Tracker</h2>{tracker_html}</section>
</div>
</main></body></html>"""


def render_jobs(jobs: Iterable[JobPosting]) -> str:
    items = []
    for job in jobs:
        items.append(
            f"""<article class="item">
<h3>{html.escape(job.title)}</h3>
<p>{html.escape(job.company)} · {html.escape(job.location or "Unknown")}</p>
<div class="meta"><span class="pill">Score {job.score:.1f}</span><span class="pill">{html.escape(job.source)}</span></div>
<div class="actions">
  <a class="button secondary" href="{html.escape(job.url)}" target="_blank" rel="noreferrer">Job post</a>
  <form method="post" action="/prepare"><input type="hidden" name="job_id" value="{html.escape(job.id)}"><button type="submit">Prepare</button></form>
</div>
</article>"""
        )
    return f"<div class='list'>{''.join(items)}</div>" if items else "<div class='empty'>No discovered jobs yet.</div>"


def render_packages(packages: Iterable[PackageSummary]) -> str:
    items = []
    for package in packages:
        items.append(
            f"""<article class="item">
<h3>{html.escape(package.position)}</h3>
<p>{html.escape(package.company)}</p>
<div class="meta"><span class="pill status">{html.escape(package.status)}</span><span class="pill">Discovery {html.escape(package.discovery_score)}</span><span class="pill">ATS {html.escape(package.ats_score)}</span></div>
<div class="actions">
  {file_link(package.relative_path + "/cv.pdf", "CV", package.has_cv)}
  {file_link(package.relative_path + "/cover_letter.pdf", "Letter", package.has_letter)}
  {file_link(package.relative_path + "/application.md", "Brief", True)}
  <a class="button secondary" href="{html.escape(package.job_url)}" target="_blank" rel="noreferrer">Job post</a>
  {status_form(package.relative_path, "Applied", "Applied")}
  {status_form(package.relative_path, "Skipped", "Skip")}
</div>
</article>"""
        )
    return f"<div class='list'>{''.join(items)}</div>" if items else "<div class='empty'>No packages prepared yet.</div>"


def file_link(relative_path: str, label: str, enabled: bool) -> str:
    if not enabled:
        return f"<button class='subtle' type='button' disabled>{html.escape(label)}</button>"
    query = urllib.parse.urlencode({"path": relative_path})
    return f"<a class='button secondary' href='/file?{query}' target='_blank'>{html.escape(label)}</a>"


def status_form(package_path: str, status: str, label: str) -> str:
    return (
        f"<form method='post' action='/status'>"
        f"<input type='hidden' name='package_path' value='{html.escape(package_path)}'>"
        f"<input type='hidden' name='status' value='{html.escape(status)}'>"
        f"<button class='subtle' type='submit'>{html.escape(label)}</button></form>"
    )


def render_tracker(rows: Iterable[TrackerRow]) -> str:
    body = []
    for row in rows:
        body.append(
            f"<tr><td>{html.escape(row.company)}</td><td>{html.escape(row.position)}</td><td>{html.escape(row.status)}</td><td>{html.escape(row.next_step)}</td></tr>"
        )
    if not body:
        return "<div class='empty'>No active tracker rows.</div>"
    return "<table class='tracker-table'><thead><tr><th>Company</th><th>Role</th><th>Status</th><th>Next</th></tr></thead><tbody>" + "".join(body) + "</tbody></table>"


class DashboardHandler(BaseHTTPRequestHandler):
    paths = DashboardPaths()

    def send_html(self, body: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def redirect_home(self, message: str = "") -> None:
        location = "/" + (f"?message={urllib.parse.quote(message)}" if message else "")
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", location)
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/file":
            self.send_file(parsed.query)
            return
        message = urllib.parse.parse_qs(parsed.query).get("message", [""])[0]
        self.send_html(render_dashboard(load_dashboard_state(self.paths), message))

    def do_POST(self) -> None:
        size = int(self.headers.get("Content-Length", 0))
        data = urllib.parse.parse_qs(self.rfile.read(size).decode("utf-8"))
        parsed = urllib.parse.urlparse(self.path)
        try:
            if parsed.path == "/status":
                package_path = data.get("package_path", [""])[0]
                status = data.get("status", [""])[0]
                changed = update_tracker_status(self.paths.tracker_path, package_path, status)
                self.redirect_home(f"Updated {package_path} to {status}." if changed else "Package row not found in tracker.")
            elif parsed.path == "/prepare":
                job_id = data.get("job_id", [""])[0]
                output_dir = prepare_job_by_id(job_id, self.paths)
                self.redirect_home(f"Prepared {relative_to_repo(output_dir, self.paths.repo_root)}." if output_dir else "Job not found.")
            elif parsed.path == "/prepare-all":
                self.run_command(["./generate.sh", "prepare-applications", "--limit", "25", "--update-tracker"], "Prepared current matches.")
            elif parsed.path == "/run-discovery":
                self.run_command(["./generate.sh", "discover", "--since-hours", "0", "--limit", "50"], "Discovery refreshed.")
            else:
                self.send_html("Not found", HTTPStatus.NOT_FOUND)
        except Exception as exc:  # pragma: no cover
            self.redirect_home(f"Action failed: {exc}")

    def run_command(self, command: list[str], success_message: str) -> None:
        subprocess.run(command, cwd=self.paths.repo_root, check=True)
        self.redirect_home(success_message)

    def send_file(self, query: str) -> None:
        relative = urllib.parse.parse_qs(query).get("path", [""])[0]
        target = (self.paths.repo_root / relative).resolve()
        try:
            target.relative_to(self.paths.repo_root.resolve())
        except ValueError:
            self.send_html("Forbidden", HTTPStatus.FORBIDDEN)
            return
        if not target.exists() or not target.is_file():
            self.send_html("Not found", HTTPStatus.NOT_FOUND)
            return
        payload = target.read_bytes()
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the local Proteus application dashboard")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8790)
    parser.add_argument("--jobs", default=str(DISCOVERY_DIR / "jobs.jsonl"))
    parser.add_argument("--packages-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--tracker", default=str(DEFAULT_TRACKER_PATH))
    args = parser.parse_args()

    DashboardHandler.paths = DashboardPaths(
        jobs_path=Path(args.jobs),
        packages_root=Path(args.packages_root),
        tracker_path=Path(args.tracker),
        repo_root=REPO_ROOT,
    )
    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"Proteus dashboard running at http://{args.host}:{args.port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
