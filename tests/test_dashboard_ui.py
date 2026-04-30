import tempfile
import unittest
from pathlib import Path

from scripts.dashboard_ui import (
    DashboardPaths,
    load_dashboard_state,
    parse_tracker_rows,
    update_tracker_status,
    upsert_tracker_row,
)


class DashboardUiTests(unittest.TestCase):
    def test_parse_tracker_rows_reads_active_application_rows(self):
        content = """
# Job Application Tracker

## Active Applications

| Date | Company | Position | CV Variant | Letter | Status | Next Step | Notes |
|------|---------|----------|------------|--------|--------|-----------|-------|
| 2026-04-19 | Sellen Construction | Senior PM | cv | senior_pm | Prepared | Follow up 2026-04-26 | Package: applications/packages/2026-04-19/sellen |
|  |  |  |  |  |  |  |  |

## Interview Pipeline
""".strip()

        rows = parse_tracker_rows(content)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].company, "Sellen Construction")
        self.assertEqual(rows[0].status, "Prepared")
        self.assertEqual(rows[0].package_path, "applications/packages/2026-04-19/sellen")

    def test_update_tracker_status_changes_matching_package_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            tracker = Path(tmp) / "tracker.md"
            tracker.write_text(
                "\n".join(
                    [
                        "| Date | Company | Position | CV Variant | Letter | Status | Next Step | Notes |",
                        "|------|---------|----------|------------|--------|--------|-----------|-------|",
                        "| 2026-04-19 | DPR Construction | Project Manager | cv_senior_pm | senior_pm | Prepared | Follow up 2026-04-26 | Package: applications/packages/2026-04-19/dpr |",
                        "|  |  |  |  |  |  |  |  |",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            changed = update_tracker_status(tracker, "applications/packages/2026-04-19/dpr", "Applied")

            self.assertTrue(changed)
            self.assertIn("| Applied |", tracker.read_text(encoding="utf-8"))

    def test_upsert_tracker_row_replaces_only_matching_package_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            tracker = Path(tmp) / "tracker.md"
            tracker.write_text(
                "\n".join(
                    [
                        "| Date | Company | Position | CV Variant | Letter | Status | Next Step | Notes |",
                        "|------|---------|----------|------------|--------|--------|-----------|-------|",
                        "| 2026-04-19 | DPR Construction | Project Manager | cv_senior_pm | senior_pm | Prepared | Follow up 2026-04-26 | Package: applications/packages/2026-04-19/dpr |",
                        "| 2026-04-19 | Sellen | Senior PM | cv | senior_pm | Prepared | Follow up 2026-04-26 | Package: applications/packages/2026-04-19/sellen |",
                        "|  |  |  |  |  |  |  |  |",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            upsert_tracker_row(
                tracker,
                "| 2026-04-19 | DPR Construction | Project Manager | cv | senior_pm | Prepared | Follow up 2026-04-26 | Package: applications/packages/2026-04-19/dpr |",
            )

            content = tracker.read_text(encoding="utf-8")
            self.assertEqual(content.count("Package: applications/packages/2026-04-19/dpr"), 1)
            self.assertIn("Package: applications/packages/2026-04-19/sellen", content)

    def test_load_dashboard_state_combines_discovery_packages_and_tracker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            jobs = root / "jobs.jsonl"
            jobs.write_text(
                '{"title":"Senior Project Manager","company":"Builder","location":"Seattle, WA","url":"https://example.com/job","source":"fixture","score":40,"score_reasons":["matched"]}\n',
                encoding="utf-8",
            )
            package_dir = root / "packages" / "2026-04-19" / "builder-senior"
            package_dir.mkdir(parents=True)
            (package_dir / "application.md").write_text(
                "\n".join(
                    [
                        "# Builder - Senior Project Manager",
                        "",
                        "**Job URL**: https://example.com/job",
                        "**Discovery Score**: 40.0",
                        "**ATS Match Score**: 80.0%",
                        "**CV Variant**: `cv_senior_pm`",
                        "**Cover Letter Template**: `senior_pm`",
                    ]
                ),
                encoding="utf-8",
            )
            (package_dir / "cv.pdf").write_bytes(b"%PDF")
            (package_dir / "cover_letter.pdf").write_bytes(b"%PDF")
            tracker = root / "tracker.md"
            tracker.write_text(
                "| Date | Company | Position | CV Variant | Letter | Status | Next Step | Notes |\n"
                "|------|---------|----------|------------|--------|--------|-----------|-------|\n"
                "| 2026-04-19 | Builder | Senior Project Manager | cv_senior_pm | senior_pm | Prepared | Follow up 2026-04-26 | Package: packages/2026-04-19/builder-senior |\n",
                encoding="utf-8",
            )

            state = load_dashboard_state(
                DashboardPaths(
                    jobs_path=jobs,
                    packages_root=root / "packages",
                    tracker_path=tracker,
                    repo_root=root,
                )
            )

        self.assertEqual(state.stats.discovered_count, 1)
        self.assertEqual(state.stats.prepared_count, 1)
        self.assertEqual(state.stats.tracker_count, 1)
        self.assertEqual(state.packages[0].status, "Prepared")


if __name__ == "__main__":
    unittest.main()
