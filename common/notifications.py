"""Candidate notifications (assessment invite, advance, reminder).

Every send carries an Idempotency-Key so a retried or duplicate send is a no-op.
This permanently fixes HR-114, where a bulk re-score double-emailed ~200 candidates.
"""


def send(mailer, candidate_id, kind, payload, idempotency_key):
    # A duplicate send with the same key is dropped, not re-sent.
    return mailer.deliver(
        candidate_id=candidate_id,
        kind=kind,
        payload=payload,
        headers={"Idempotency-Key": idempotency_key},
    )
