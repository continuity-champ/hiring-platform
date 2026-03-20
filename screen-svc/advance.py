"""screen-svc: advance candidates to the interview stage based on Cognita score.

Policy: candidates scoring >= AUTO_ADVANCE_SCORE are auto-advanced to 'interview'.
Below-threshold candidates are NEVER auto-rejected — they go to human review first.
"""

AUTO_ADVANCE_SCORE = 75


def advance_candidate(candidate, repo):
    if candidate.score >= AUTO_ADVANCE_SCORE:
        candidate.state = "interview"
        repo.save(candidate)
        return "advanced"
    # Below threshold: flag for human review, never auto-reject.
    candidate.state = "human_review"
    repo.save(candidate)
    return "human_review"
