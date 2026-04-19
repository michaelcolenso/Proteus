# Job Discovery Scraper Design

## Purpose

Add a freshness-first job discovery feature to the existing CV and application workflow. The feature should surface newly posted construction project manager and adjacent roles quickly, normalize them into a consistent local format, rank them by relevance and freshness, and optionally hand top matches into the existing autopilot brief generator.

The first version will use public sources only. It will not use logged-in accounts, captcha solving, private APIs, or techniques that bypass access controls.

## User Goals

- Find relevant construction project manager jobs as soon as possible after posting.
- Cover a broad set of public sources rather than relying on one job board.
- Prioritize newness, then relevance to construction PM, senior PM, superintendent, estimator, multifamily, luxury residential, owner representative, and related roles.
- Produce local files that can be reviewed, versioned, and fed into the current application tools.
- Avoid noisy duplicates and repeated processing of already-seen jobs.

## Command Surface

Add a new `discover` command to `generate.sh`:

```bash
./generate.sh discover
./generate.sh discover --since-hours 24 --limit 25
./generate.sh discover --autopilot-top 5
```

The shell command will delegate to a new Python script:

```bash
python3 scripts/discover_jobs.py [options]
```

Initial options:

- `--since-hours`: Prefer jobs posted or discovered within the provided window.
- `--limit`: Limit the number of jobs shown in the Markdown output.
- `--autopilot-top`: Generate autopilot briefs for the top N ranked jobs.
- `--config`: Override the discovery source config path.
- `--dry-run-fixtures`: Read local fixture files instead of fetching live pages.

## Source Strategy

Discovery will be adapter-based. Each adapter has one job: fetch public data from a source type and return normalized candidate postings.

Initial source types:

- Public ATS boards where pages or JSON are accessible without authentication, such as Greenhouse, Lever, Ashby, SmartRecruiters, and similar systems.
- Public company career pages from a curated seed list of general contractors, construction managers, developers, owner reps, and specialty builders.
- Public search/feed style sources where available and stable enough to parse.
- Configured keyword/watchlist searches where the source exposes public results.

The implementation should favor many small, imperfect adapters over one large scraper. A source failure should be reported but should not fail the full discovery run.

## Configuration

Create a config file at:

```text
applications/discovery/sources.yaml
```

The config will define source entries, query terms, target locations, and scoring preferences. A minimal shape:

```yaml
queries:
  - construction project manager
  - senior project manager construction
  - multifamily project manager
  - construction superintendent
  - construction estimator
  - owner's representative construction

locations:
  - Seattle, WA
  - Bellevue, WA
  - Remote

sources:
  - type: greenhouse
    name: example-builder
    url: https://example.com/careers
  - type: lever
    name: example-developer
    url: https://jobs.lever.co/example
  - type: career_page
    name: example-construction
    url: https://example.com/careers
```

The config should be easy to edit by hand. Missing or failing entries should be skipped with clear warnings.

## Normalized Job Model

Each discovered job will be normalized into a dictionary with these fields:

- `id`: Stable local ID derived from canonical URL and key fields.
- `title`: Job title.
- `company`: Company name.
- `location`: Location text.
- `url`: Canonical public URL.
- `source`: Source adapter name.
- `posted_at`: Parsed posting date when available.
- `discovered_at`: Local timestamp when first seen.
- `description`: Full text when safely available.
- `snippet`: Short description or extracted context.
- `tags`: Matched role, project type, location, and skill tags.
- `score`: Total ranking score.
- `score_reasons`: Short list explaining why the job ranked where it did.

## State And Outputs

Create local discovery state under:

```text
applications/discovery/
```

Primary files:

- `seen.json`: Known job IDs and first-seen timestamps.
- `jobs.jsonl`: Append-only normalized job records.
- `latest.md`: Human-readable ranked report from the most recent run.
- `fixtures/`: Optional saved HTML or JSON fixtures for parser tests and dry runs.

When `--autopilot-top N` is provided, the script will write each selected job description to a temporary text file and call the existing application autopilot flow. Generated briefs remain under the existing `applications/generated/` directory.

## Ranking

The first ranking formula should be simple and inspectable:

- Freshness score: high weight for jobs posted or first discovered recently.
- Role score: project manager, senior project manager, superintendent, estimator, project executive, owner representative, preconstruction.
- Construction score: construction, general contractor, multifamily, luxury residential, high-rise, mixed-use, tenant improvement, renovation.
- Location score: configured preferred locations and remote/hybrid text.
- Seniority score: match seniority signals without over-filtering.
- Exclusion penalties: internships, unpaid roles, unrelated software/product roles, sales-only roles, and stale postings.

The report must show score reasons so a user can understand and tune the system.

## Dedupe

Deduplication will use:

- Canonicalized URL.
- Similarity over title, company, and location.
- Stable local IDs for already-seen jobs.

The script should avoid adding duplicate rows to `jobs.jsonl` during repeated runs. If a known job is seen again with updated details, it may update the latest report but should preserve the original `discovered_at` timestamp.

## Error Handling

- Network requests use short timeouts and a clear user agent.
- Per-source errors are collected and shown in the run summary.
- A broken source does not stop other sources.
- Invalid config entries produce warnings with the source name and field.
- If no jobs are found, the output should distinguish between "no matches" and "all sources failed."

## Testing

Add focused tests for:

- Ranking and score reasons.
- URL canonicalization and dedupe.
- Date parsing and freshness handling.
- Config loading defaults and validation.
- Source parser fixtures for each adapter added in v1.

Live network fetching should not be required for normal tests. Fixtures under `applications/discovery/fixtures/` or test fixtures should cover parsing behavior.

## First Implementation Scope

V1 should include:

- `scripts/discover_jobs.py`.
- `applications/discovery/sources.yaml` with a small starter set of editable public sources and queries.
- `./generate.sh discover` integration.
- Local state and report generation.
- At least two source adapters: one ATS-style adapter and one generic career page adapter.
- Ranking, dedupe, and dry-run fixture support.
- Tests for the non-network core behavior.

V1 should not include:

- Authenticated scraping.
- Browser automation as the default fetch path.
- Automated applications or form submission.
- Captcha solving or access-control bypass.
- A persistent background scheduler. Scheduling can be handled later by cron, launchd, or a separate command once the discovery loop is useful.

## Open Design Decisions

The first implementation should pick conservative defaults:

- Preferred geography defaults to Seattle/Bellevue/remote unless the config says otherwise.
- The tool should collect more candidate jobs than it displays, then show the top ranked subset.
- Source coverage should be expanded incrementally as adapters prove reliable.

These defaults can be changed through `applications/discovery/sources.yaml` without code edits.
