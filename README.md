# hiring-platform

AI-assisted hiring and assessment platform. Three services:

- **screen-svc** — screens candidates and auto-advances them to interview.
- **assess-svc** — submits assessments to our scoring provider, **Cognita**.
- **interview-svc** — schedules interviews and sends reminders.

## Data
All hiring data lives in the `ats_prod` Postgres database. Core tables are
`candidates` and `assessments` (unique index on `(candidate_id, assessment_id)`
to dedupe re-scores).

## Scoring
Each candidate is scored by Cognita. assess-svc retries a failed scoring call a
**maximum of 3 times** with backoff, then flags the candidate for manual review.
Candidates scoring **>= 75** are auto-advanced to the interview stage.
Cognita enforces a rate limit of **60 requests per minute** per API key.

## Reminders
interview-svc sends an interview reminder daily at **09:00 UTC**, 24h before each interview.

## Gotcha
**Never** re-score candidates already in the `interview` or `hired` state — re-scoring
can re-trigger candidate emails (this caused incident HR-114). And never auto-reject a
below-threshold candidate on the AI score alone; they always get a human review first.

## Config & secrets
Service config: `/etc/assess-svc/config.yaml`. Cognita credentials load from Vault at
`secret/hiring/cognita` — never in `.env` or the repo.
