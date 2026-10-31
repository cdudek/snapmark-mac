---
id: 2026-10-26-adr-private-monorepo-updates-from-gcs
title: 'One private monorepo; installed copies update from a public Cloud Storage bucket'
type: adr
status: accepted
created: 2026-10-26
supersedes: []
superseded_by: []
amended_by: []
tags: [repo, release, updates]
---

# One private monorepo; installed copies update from a public Cloud Storage bucket

## Context

The repo went public on 2026-09-26 only so that electron-updater could read its GitHub releases. The owner wants "a monorepo, that is not public", with `/snapmark-app`, `/snapmark-chrome` and `/snapmark-web` (2026-10-26), and picked Cloud Storage in GCP project `snapmark-ai` for the downloads. Releases of a private repo answer 404 without a token, and a token inside the app would leak.

## Decision

- **Layout:** the Mac app lives in `snapmark-app/`, an npm workspace of a private root package. `snapmark-chrome/` and `snapmark-web/` start as READMEs and join `workspaces` when they get a `package.json`. The SDLC chain, docs, design explorations and CI stay at the root. One lockfile, at the root.
- **Update feed:** `build.publish` is `provider: generic` with `https://storage.googleapis.com/snapmark-updates/mac`. Every installed copy reads `latest-mac.yml` there.
- **Bucket:** `gs://snapmark-updates`, europe-west3, Standard, uniform access. `allUsers` may read objects (`roles/storage.legacyObjectReader`: get, no listing). The release workflow alone may write.
- **Upload:** the release job logs in with Workload Identity Federation (pool `github`, provider `snapmark`, condition `assertion.repository=='cdudek/snapmark' && assertion.ref=='refs/heads/main'`: only the release job on `main`) as `release-uploader@snapmark-ai.iam.gserviceaccount.com`, which holds `roles/storage.objectAdmin` on this bucket only. No key exists. Binaries go up first, `latest-mac.yml` last with `Cache-Control: no-cache`, then every version except the newest 10 is deleted (`snapmark-app/scripts/prune-releases.sh`). The bucket keeps no soft-deleted or noncurrent copies, so a pruned version is gone at once.
- **GitHub releases stay** as the record of each version and its tag; nobody downloads from them once the repo is private.
- **Order:** the first release built this way ships from the still-public repo, so installed copies move to the bucket feed through GitHub one last time. The repo goes private only after the owner's Macs run that release.
- **electron-builder** runs through `snapmark-app/scripts/electron-builder.sh`, which passes the installed Electron version: workspaces hoist `electron` to the root, and electron-builder refuses the `^45.0.0` range otherwise.

## Rejected

- A public releases-only GitHub repo: the owner picked Cloud Storage.
- Cloudflare R2: no download fees, but the owner picked GCS. Revisit at about 500 users, where downloads pass $30 a month.
- A token in the app to read private releases: it would ship to every user.
- A standalone `snapmark-app/` with its own lockfile: the root tooling (prettier, the guardrail test) would need its own dependencies.
- An age-based lifecycle rule for pruning: a quiet quarter would delete the version clients are being sent.

## Costs

Expected, at list prices: storage about $0.13 a month (10 versions, 5.5 GB); downloads about $0.015 per Mac per update (the 124 MB arm64 ZIP at about $0.12/GB); about $1 a month for the owner alone, $6 at 100 users, $60 at 1,000.

## Setup

Run once, as the owner's Google account, after a billing account is linked to `snapmark-ai`:

```bash
gcloud services enable iam.googleapis.com iamcredentials.googleapis.com sts.googleapis.com --project snapmark-ai
gcloud storage buckets create gs://snapmark-updates --project snapmark-ai --location europe-west3 --default-storage-class STANDARD --uniform-bucket-level-access --no-public-access-prevention
gcloud storage buckets update gs://snapmark-updates --clear-soft-delete --no-versioning
gcloud storage buckets add-iam-policy-binding gs://snapmark-updates --member allUsers --role roles/storage.legacyObjectReader
gcloud iam workload-identity-pools create github --project snapmark-ai --location global --display-name "GitHub Actions"
gcloud iam workload-identity-pools providers create-oidc snapmark --project snapmark-ai --location global --workload-identity-pool github --issuer-uri https://token.actions.githubusercontent.com --attribute-mapping google.subject=assertion.sub,attribute.repository=assertion.repository --attribute-condition "assertion.repository=='cdudek/snapmark' && assertion.ref=='refs/heads/main'"
gcloud iam service-accounts create release-uploader --project snapmark-ai --display-name "Snapmark release uploader"
gcloud storage buckets add-iam-policy-binding gs://snapmark-updates --member serviceAccount:release-uploader@snapmark-ai.iam.gserviceaccount.com --role roles/storage.objectAdmin
gcloud iam service-accounts add-iam-policy-binding release-uploader@snapmark-ai.iam.gserviceaccount.com --project snapmark-ai --role roles/iam.workloadIdentityUser --member principalSet://iam.googleapis.com/projects/225569511245/locations/global/workloadIdentityPools/github/attribute.repository/cdudek/snapmark
```

## Milestones

- [2026-10-26-monorepo-private](../../changes/2026-10-26-monorepo-private/milestone.md)
