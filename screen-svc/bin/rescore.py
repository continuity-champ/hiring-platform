# Re-scores candidates. NEVER re-score candidates already in interview/hired:
# re-scoring can re-trigger candidate emails (caused incident HR-114 on 2026-05-09).
def rescore(candidates, client):
    for c in candidates:
        if c.state != "screening":
            continue  # guard added after HR-114
        client.score(c)  # retries up to 3x (see assess-svc config)
