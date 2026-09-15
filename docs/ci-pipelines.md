# CI pipelines: GitHub Actions (KAN-26)

Investigation and estimate for the project's continuous integration. Decision:
**GitHub Actions, native (no third-party CI)**.

## Core aspects

### Cost

GitHub Free includes **2,000 Actions minutes/month** and **500 MB of artifact
storage** for private repositories. A full CI run for this project
(dependencies cached via `setup-uv`, then ruff + mypy + pytest + a Docker
build) takes roughly 2–4 minutes. Even with every PR re-running CI several
times, the free tier covers this project by an order of magnitude. Public
repositories run entirely free. No paid plan is needed.

### Flexibility

Actions is a generic workflow runner, not just CI: build matrices, environment
secrets, deployment jobs, scheduled tasks and reusable workflows are all
available later without migrating tooling. The marketplace already provides
well-maintained actions used here (`astral-sh/setup-uv`,
`docker/setup-buildx-action`, `docker/build-push-action`). If we ever outgrow
it, the workflow file is plain YAML in the repo and portable in structure.

### Necessity

A PR-gating CI is what makes the acceptance criteria of M0 tickets verifiable
(KAN-6: "a pull request with a deliberate lint error is blocked by CI"). It is
cheap insurance against broken main and is required before any team growth.

## What was set up

* `.github/workflows/ci.yml` with two jobs:
  * `checks` — `ruff check`, `ruff format --check`, `mypy`, `pytest` in a
    single job (single dependency install, fewer billed minutes).
  * `docker` — builds the production image (`api/Dockerfile.prod`) on every
    PR so Dockerfile breakage is caught early. Uses the GitHub Actions cache.
* Concurrency group cancels superseded runs on the same ref.
* The production image is a multi-stage build (builder with `uv sync --no-dev`
  → slim runtime, non-root user); no dev dependencies, tests, build tools or
  caches end up in the final image.

## Deferred

* Publishing images to a registry (GHCR) — not needed until there is a deploy
  target.
* Separate deploy workflows, environment protection rules — later milestones.
