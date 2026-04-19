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
    parse_career_page,
    parse_lever_jobs,
    load_config,
    parse_posted_at,
    score_jobs,
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


if __name__ == "__main__":
    unittest.main()
