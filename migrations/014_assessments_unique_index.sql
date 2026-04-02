-- ats_prod: candidates + assessments tables, with a dedup guarantee
CREATE TABLE IF NOT EXISTS candidates (
    id          BIGSERIAL PRIMARY KEY,
    full_name   TEXT NOT NULL,
    email       TEXT NOT NULL,
    state       TEXT NOT NULL DEFAULT 'screening',
    score       INTEGER,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS assessments (
    id            BIGSERIAL PRIMARY KEY,
    candidate_id  BIGINT NOT NULL REFERENCES candidates(id),
    assessment_id BIGINT NOT NULL,
    score         INTEGER,
    scored_at     TIMESTAMPTZ
);

-- One result per (candidate, assessment): dedupes Cognita re-scores
CREATE UNIQUE INDEX idx_assessments_candidate_assessment
    ON assessments (candidate_id, assessment_id);
