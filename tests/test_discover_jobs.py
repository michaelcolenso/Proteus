import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from scripts.discover_jobs import (
    DiscoveryConfig,
    DiscoveryState,
    JobPosting,
    canonicalize_url,
    count_enabled_sources,
    dedupe_jobs,
    filter_recent_jobs,
    lever_api_url,
    load_fixture_jobs,
    load_config,
    nonnegative_int,
    parse_career_page,
    parse_lever_created_at,
    parse_lever_jobs,
    parse_posted_at,
    resolve_runtime_dir,
    score_jobs,
    render_latest_report,
    write_autopilot_inputs,
)


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

    def test_canonicalize_url_sorts_non_tracking_query_params(self):
        canonical_a = canonicalize_url("https://example.com/job?b=2&a=1&utm_source=x")
        canonical_b = canonicalize_url("https://example.com/job?a=1&b=2&utm_source=x")

        self.assertEqual(canonical_a, "https://example.com/job?a=1&b=2")
        self.assertEqual(canonical_a, canonical_b)

    def test_lever_api_url_maps_public_board_to_json_endpoint(self):
        self.assertEqual(
            lever_api_url("https://jobs.lever.co/skylineconstruction"),
            "https://api.lever.co/v0/postings/skylineconstruction?mode=json",
        )
        self.assertEqual(
            lever_api_url("https://api.lever.co/v0/postings/skylineconstruction?mode=json"),
            "https://api.lever.co/v0/postings/skylineconstruction?mode=json",
        )

    def test_load_config_uses_repo_default_from_scripts_cwd(self):
        repo_root = Path(__file__).resolve().parents[1]
        scripts_dir = repo_root / "scripts"
        original_cwd = Path.cwd()

        try:
            os.chdir(scripts_dir)
            config = load_config()
        finally:
            os.chdir(original_cwd)

        self.assertIsInstance(config, DiscoveryConfig)
        self.assertIn("construction project manager", config.queries)
        self.assertTrue(config.sources)

    def test_count_enabled_sources_ignores_disabled_entries(self):
        config = DiscoveryConfig(
            sources=[
                {"name": "live", "type": "career_page", "enabled": True},
                {"name": "disabled", "type": "lever", "enabled": False},
                {"name": "implicit", "type": "career_page"},
            ]
        )

        self.assertEqual(count_enabled_sources(config), 2)


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

    def test_parse_posted_at_normalizes_common_public_formats(self):
        self.assertEqual(parse_posted_at("2026-04-18"), "2026-04-18T00:00:00+00:00")
        self.assertEqual(parse_posted_at("2026-04-18T12:30:00Z"), "2026-04-18T12:30:00+00:00")
        self.assertIsNotNone(parse_posted_at("2 days ago"))

    def test_parse_posted_at_supports_common_relative_public_formats(self):
        now = datetime.now(timezone.utc)

        today = parse_posted_at("today")
        yesterday = parse_posted_at("yesterday")
        thirty_plus_days_ago = parse_posted_at("30+ days ago")
        two_days_ago = parse_posted_at("2d ago")
        two_weeks_ago = parse_posted_at("2 weeks ago")

        self.assertIsNotNone(today)
        self.assertIsNotNone(yesterday)
        self.assertIsNotNone(thirty_plus_days_ago)
        self.assertIsNotNone(two_days_ago)
        self.assertIsNotNone(two_weeks_ago)

        self.assertEqual(today, now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat())
        self.assertEqual(yesterday, (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat())
        self.assertTrue(parse_posted_at("30+ days ago").startswith((now - timedelta(days=30)).date().isoformat()))
        self.assertTrue(parse_posted_at("2d ago").startswith((now - timedelta(days=2)).date().isoformat()))
        self.assertTrue(parse_posted_at("2 weeks ago").startswith((now - timedelta(days=14)).date().isoformat()))

    def test_discovery_state_filters_duplicates_within_single_batch_and_records_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = DiscoveryState(Path(tmp))
            jobs = [
                JobPosting(
                    title="Project Manager",
                    company="Builder",
                    location="Seattle, WA",
                    url="https://example.com/job",
                    source="fixture",
                ),
                JobPosting(
                    title="Project Manager",
                    company="Builder",
                    location="Seattle, WA",
                    url="https://example.com/job",
                    source="fixture",
                ),
            ]

            fresh = state.filter_new(jobs)
            state.record_jobs(fresh)

            jobs_path = Path(tmp) / "jobs.jsonl"
            seen_path = Path(tmp) / "seen.json"

            self.assertEqual(len(fresh), 1)
            self.assertEqual(jobs_path.read_text(encoding="utf-8").count("\n"), 1)
            self.assertIn("Project Manager", seen_path.read_text(encoding="utf-8"))

    def test_discovery_state_reset_clears_seen_and_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = DiscoveryState(Path(tmp))
            job = JobPosting(
                title="Project Manager",
                company="Builder",
                location="Seattle, WA",
                url="https://example.com/job",
                source="fixture",
            )

            state.record_jobs([job])
            state.reset()

            self.assertFalse((Path(tmp) / "jobs.jsonl").exists())
            self.assertFalse((Path(tmp) / "seen.json").exists())
            self.assertEqual(state.filter_new([job]), [job])

    def test_dedupe_jobs_preserves_first_occurrence(self):
        first = JobPosting(
            title="Project Manager",
            company="Builder",
            location="Seattle, WA",
            url="https://example.com/job?utm_source=x",
            source="first",
        )
        duplicate = JobPosting(
            title="Project Manager",
            company="Builder",
            location="Seattle, WA",
            url="https://example.com/job",
            source="duplicate",
        )

        self.assertEqual(dedupe_jobs([first, duplicate]), [first])


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
        report = render_latest_report([job], ["broken-source: timeout"], limit=10, new_count=1)
        self.assertIn("# Latest Job Discovery", report)
        self.assertIn("New matches: 1", report)
        self.assertIn("Source errors: 1", report)
        self.assertIn("Senior Project Manager", report)
        self.assertIn("broken-source: timeout", report)

    def test_render_latest_report_has_helpful_empty_state(self):
        report = render_latest_report([], [], limit=10, new_count=0)

        self.assertIn("Total matches: 0", report)
        self.assertIn("New matches: 0", report)
        self.assertIn("Enable public sources", report)

    def test_render_latest_report_explains_zero_limit(self):
        job = JobPosting(
            title="Project Manager",
            company="Acme",
            location="Seattle, WA",
            url="https://example.com/job",
            source="fixture",
        )

        report = render_latest_report([job], [], limit=0)

        self.assertIn("Total matches: 1", report)
        self.assertIn("report limit is 0", report)
        self.assertNotIn("### 1. Project Manager", report)

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

    def test_render_latest_report_normalizes_multiline_detail(self):
        job = JobPosting(
            title="Project Manager",
            company="Acme",
            location="Seattle, WA",
            url="https://example.com/job",
            source="fixture",
            description="Lead projects\nacross teams",
            score=10.0,
            score_reasons=["matched: project manager"],
        )
        report = render_latest_report([job], [], limit=10)
        self.assertIn("- Description: Lead projects across teams", report)
        self.assertNotIn("\nacross teams", report)

    def test_write_autopilot_inputs_prunes_old_text_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            stale = output_dir / "stale.txt"
            stale.write_text("stale", encoding="utf-8")
            job = JobPosting(
                title="Project Manager",
                company="Acme",
                location="Seattle, WA",
                url="https://example.com/job",
                source="fixture",
            )

            written = write_autopilot_inputs([job], output_dir)

            self.assertEqual([path.name for path in written], [f"{job.id}.txt"])
            self.assertFalse(stale.exists())
            self.assertEqual(sorted(path.name for path in output_dir.glob("*.txt")), [f"{job.id}.txt"])
            content = written[0].read_text(encoding="utf-8")
            self.assertIn("Source: fixture", content)
            self.assertIn("URL: https://example.com/job", content)

    def test_resolve_runtime_dir_uses_dry_run_subdir_for_fixtures(self):
        self.assertEqual(resolve_runtime_dir(Path("/tmp/example.json")), Path(__file__).resolve().parents[1] / "applications/discovery/dry_run")
        self.assertEqual(resolve_runtime_dir(None), Path(__file__).resolve().parents[1] / "applications/discovery")

    def test_nonnegative_int_rejects_negative_values(self):
        self.assertEqual(nonnegative_int("0"), 0)
        self.assertEqual(nonnegative_int("12"), 12)
        with self.assertRaises(Exception):
            nonnegative_int("-1")


class AdapterTests(unittest.TestCase):
    def test_parse_lever_jobs(self):
        payload = [
            {
                "text": "Senior Project Manager",
                "hostedUrl": "https://jobs.lever.co/acme/123",
                "categories": {"location": "Seattle, WA"},
                "descriptionPlain": "Manage multifamily construction.",
                "createdAt": 1776556800000,
            }
        ]
        jobs = parse_lever_jobs(payload, {"name": "acme", "url": "https://jobs.lever.co/acme"})
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].title, "Senior Project Manager")
        self.assertEqual(jobs[0].company, "acme")
        self.assertEqual(jobs[0].location, "Seattle, WA")
        self.assertEqual(jobs[0].posted_at, "2026-04-19T00:00:00+00:00")

    def test_parse_lever_created_at_ignores_missing_values(self):
        self.assertIsNone(parse_lever_created_at(None))

    def test_parse_generic_career_page_links(self):
        html = """
        <html><body>
          <a href="/careers/senior-project-manager">Senior Project Manager - Seattle</a>
          <a href="/about">About</a>
        </body></html>
        """
        jobs = parse_career_page(html, {"name": "Acme Builders", "url": "https://example.com/careers"})
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].url, "https://example.com/careers/senior-project-manager")
        self.assertEqual(jobs[0].title, "Senior Project Manager - Seattle")

    def test_parse_generic_career_page_links_uses_aria_label_and_title(self):
        html = """
        <html><body>
          <a href="/careers/senior-superintendent" aria-label="Senior Superintendent">View role</a>
          <a href="/careers/project-engineer" title="Project Engineer">View role</a>
          <a href="/about">About</a>
        </body></html>
        """
        jobs = parse_career_page(html, {"name": "Acme Builders", "url": "https://example.com/careers"})
        self.assertEqual(len(jobs), 2)
        self.assertEqual([job.title for job in jobs], ["Senior Superintendent", "Project Engineer"])
        self.assertEqual(jobs[0].url, "https://example.com/careers/senior-superintendent")
        self.assertEqual(jobs[1].url, "https://example.com/careers/project-engineer")
        self.assertTrue(all(job.title != "About" for job in jobs))


if __name__ == "__main__":
    unittest.main()
