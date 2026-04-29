import tempfile
import unittest
from pathlib import Path

from scripts.discover_jobs import JobPosting
from scripts.prepare_applications import (
    ApplicationPackage,
    draft_cover_letter_typ,
    load_ranked_jobs,
    package_slug,
    select_application_jobs,
    write_application_package,
)


class PrepareApplicationsTests(unittest.TestCase):
    def test_load_ranked_jobs_reads_jsonl_and_sorts_by_score(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "jobs.jsonl"
            path.write_text(
                "\n".join(
                    [
                        '{"title":"Project Manager","company":"B","location":"Seattle, WA","url":"https://example.com/b","source":"fixture","score":12}',
                        '{"title":"Senior Project Manager","company":"A","location":"Seattle, WA","url":"https://example.com/a","source":"fixture","score":40}',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            jobs = load_ranked_jobs(path)

        self.assertEqual([job.company for job in jobs], ["A", "B"])

    def test_select_application_jobs_filters_noise_and_limits_results(self):
        jobs = [
            JobPosting(
                title="Senior Project Manager",
                company="Builder",
                location="Seattle, WA",
                url="https://example.com/good",
                source="fixture",
                score=40,
            ),
            JobPosting(
                title="Rail Project Manager",
                company="Transit",
                location="Seattle, WA",
                url="https://example.com/rail",
                source="fixture",
                score=40,
            ),
            JobPosting(
                title=".serp-page-1fhg8gh{inline-size:1.5rem;}assistant project manager construction",
                company="Multiple employers",
                location="Seattle, WA",
                url="https://example.com/css",
                source="fixture",
                score=40,
            ),
            JobPosting(
                title="Electrical Estimator/Project Manager",
                company="Electrical",
                location="Seattle, WA",
                url="https://example.com/electrical",
                source="fixture",
                score=36,
            ),
            JobPosting(
                title="Project Coordinator",
                company="Builder",
                location="Seattle, WA",
                url="https://example.com/low",
                source="fixture",
                score=5,
            ),
        ]

        selected = select_application_jobs(jobs, limit=2, min_score=25)

        self.assertEqual([job.url for job in selected], ["https://example.com/good"])

    def test_package_slug_is_stable_and_readable(self):
        job = JobPosting(
            title="Senior Project Manager - Commercial Interiors",
            company="Skyline Construction",
            location="Seattle, WA",
            url="https://example.com/job",
            source="fixture",
        )

        self.assertEqual(package_slug(job), "skyline-construction-senior-project-manager-commercial-interiors")

    def test_draft_cover_letter_typ_replaces_company_and_role(self):
        job = JobPosting(
            title="Senior Project Manager",
            company="Acme Builders",
            location="Seattle, WA",
            url="https://example.com/job",
            source="fixture",
            description="Lead multifamily construction with Procore and Bluebeam.",
        )

        letter = draft_cover_letter_typ(job, letter_template="senior_pm", repo_root=Path("/repo"))

        self.assertIn('recipientName: "Acme Builders"', letter)
        self.assertIn('subject: "Re: Senior Project Manager Position"', letter)
        self.assertIn("Dear Hiring Manager,", letter)
        self.assertIn("multifamily", letter.lower())
        self.assertIn("#let metadata = toml(\"/repo/metadata.toml\")", letter)

    def test_write_application_package_creates_expected_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = ApplicationPackage(
                job=JobPosting(
                    title="Senior Project Manager",
                    company="Acme Builders",
                    location="Seattle, WA",
                    url="https://example.com/job",
                    source="fixture",
                    description="Lead multifamily construction.",
                    score=40,
                    score_reasons=["matched: project manager"],
                ),
                cv_variant="cv_senior_pm",
                letter_template="senior_pm",
                match_score=80.0,
                output_dir=Path(tmp) / "acme-senior-project-manager",
            )

            write_application_package(package, repo_root=Path("/repo"), compile_outputs=False)

            self.assertTrue((package.output_dir / "job_posting.txt").exists())
            self.assertTrue((package.output_dir / "cover_letter.typ").exists())
            self.assertTrue((package.output_dir / "application.md").exists())
            self.assertIn("CV Variant", (package.output_dir / "application.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
