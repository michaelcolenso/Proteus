#!/usr/bin/env python3
"""Minimal local web UI for the application autopilot feature."""

import argparse
import html
import urllib.parse
from datetime import date, timedelta
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, List, Tuple

from analyze_job import JobAnalyzer, load_cv_keywords
from application_autopilot import (
    PROFILE_TO_VARIANT,
    append_tracker_row,
    choose_best_profile,
    choose_letter_template,
    extract_company_name,
    recommended_achievements,
    slugify,
)

try:
    import tomllib as toml_loader
except ModuleNotFoundError:  # pragma: no cover
    toml_loader = None
    import toml as toml_legacy


def run_autopilot(job_text: str, output_dir: str, profile_name: str, update_tracker: bool) -> Dict[str, str]:
    metadata_text = Path("metadata.toml").read_text(encoding="utf-8")
    metadata = toml_loader.loads(metadata_text) if toml_loader else toml_legacy.loads(metadata_text)

    analyzer = JobAnalyzer(load_cv_keywords())
    keywords = analyzer.extract_keywords(job_text)
    match = analyzer.calculate_match_score(keywords)
    suggestions = analyzer.suggest_keywords(keywords, top_n=12)
    keyword_profile = analyzer.generate_keyword_profile(keywords, profile_name)

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
        achievements_warning = "PyYAML is not installed, so achievement ranking was skipped."

    company = extract_company_name(job_text)
    today = date.today().isoformat()
    follow_up = (date.today() + timedelta(days=7)).isoformat()
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{today}_{slugify(company)}_autopilot.md"

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

    if update_tracker:
        tracker_path = Path("applications/tracker.md")
        row = (
            f"| {today} | {company} | [Role from posting] | {cv_variant} | {letter_template} "
            f"| Applied | Follow up {follow_up} | Added via autopilot UI |"
        )
        append_tracker_row(tracker_path, row)

    return {
        "company": company,
        "match_score": str(match["score"]),
        "cv_variant": cv_variant,
        "letter_template": letter_template,
        "output_file": str(out_file),
    }


CSS = """
body { font-family: Inter, system-ui, sans-serif; margin: 0; background: #f7f9fc; }
main { max-width: 980px; margin: 24px auto; background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 2px 14px rgba(0,0,0,.08); }
h1 { margin-top: 0; }
label { font-weight: 600; display: block; margin: 12px 0 6px; }
textarea, input[type=text] { width: 100%; box-sizing: border-box; padding: 10px; border: 1px solid #c7d2e5; border-radius: 8px; }
textarea { min-height: 260px; resize: vertical; }
button { margin-top: 14px; background: #1f6feb; color: #fff; border: 0; padding: 10px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; }
.result { margin-top: 18px; padding: 14px; border-radius: 8px; background: #eef6ff; border: 1px solid #bfdcff; }
.error { background: #fff1f2; border-color: #fecdd3; }
small { color: #51607a; }
"""


def render_form(message: str = "", error: bool = False, job_text: str = "", output_dir: str = "applications/generated", profile_name: str = "autopilot_custom", update_tracker: bool = False) -> str:
    status_html = ""
    if message:
        klass = "result error" if error else "result"
        status_html = f"<div class='{klass}'>{message}</div>"

    checked = "checked" if update_tracker else ""
    return f"""<!doctype html>
<html><head><meta charset='utf-8'><title>Autopilot UI</title><style>{CSS}</style></head>
<body><main>
<h1>Application Autopilot UI</h1>
<small>Paste a job posting and generate a tailored brief in one click.</small>
<form method='post'>
  <label>Job posting text</label>
  <textarea name='job_text' required>{html.escape(job_text)}</textarea>

  <label>Output directory</label>
  <input type='text' name='output_dir' value='{html.escape(output_dir)}' />

  <label>Profile name</label>
  <input type='text' name='profile_name' value='{html.escape(profile_name)}' />

  <label><input type='checkbox' name='update_tracker' {checked}/> Update applications/tracker.md</label>
  <button type='submit'>Generate brief</button>
</form>
{status_html}
</main></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send_html(self, body: str, status: int = HTTPStatus.OK):
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        self._send_html(render_form())

    def do_POST(self):
        size = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(size).decode("utf-8")
        data = urllib.parse.parse_qs(raw)

        job_text = data.get("job_text", [""])[0].strip()
        output_dir = data.get("output_dir", ["applications/generated"])[0].strip() or "applications/generated"
        profile_name = data.get("profile_name", ["autopilot_custom"])[0].strip() or "autopilot_custom"
        update_tracker = "update_tracker" in data

        if not job_text:
            self._send_html(
                render_form("Please provide a job posting.", True, job_text, output_dir, profile_name, update_tracker),
                HTTPStatus.BAD_REQUEST,
            )
            return

        try:
            result = run_autopilot(job_text, output_dir, profile_name, update_tracker)
            message = (
                f"<strong>Success.</strong> {html.escape(result['company'])} | Match {result['match_score']}% | "
                f"CV {html.escape(result['cv_variant'])} | Letter {html.escape(result['letter_template'])}<br/>"
                f"Saved: <code>{html.escape(result['output_file'])}</code>"
            )
            self._send_html(render_form(message, False, job_text, output_dir, profile_name, update_tracker))
        except Exception as exc:  # pragma: no cover
            self._send_html(
                render_form(f"Generation failed: {html.escape(str(exc))}", True, job_text, output_dir, profile_name, update_tracker),
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )


def main():
    parser = argparse.ArgumentParser(description="Run a local UI for application autopilot")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Autopilot UI running at http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
