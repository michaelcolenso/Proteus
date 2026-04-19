import os
import tempfile
import unittest
from pathlib import Path

from scripts.discover_jobs import DiscoveryConfig, JobPosting, canonicalize_url, load_config


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


if __name__ == "__main__":
    unittest.main()
