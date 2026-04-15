"""interview-svc: send interview reminders.

Runs daily at 09:00 UTC and emails a reminder 24h before each scheduled interview.
Known issue (HIRE-221): if an interview is rescheduled within the 24h window, both
the old and new slot can trigger a reminder. Workaround: dedupe by
(candidate_id, interview_date) before sending.
"""

from datetime import datetime, timedelta

REMINDER_LEAD = timedelta(hours=24)


def send_due_reminders(repo, mailer, now=None):
    now = now or datetime.utcnow()
    window_start = now + REMINDER_LEAD
    for interview in repo.interviews_scheduled_around(window_start):
        mailer.send_reminder(interview.candidate_id, interview.slot)
