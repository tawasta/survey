import logging

from dateutil.relativedelta import relativedelta

from odoo import fields, models

_logger = logging.getLogger(__name__)

RETENTION_DAYS_PARAM = "survey_answer_timed_cleanup.retention_days"


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    answer_retention_days = fields.Integer(
        string="Answer Data Retention (days)",
        help="Number of days an answer to this question is kept before it is "
        "deleted by the scheduled cleanup action, counted from when the answer "
        "was recorded. Applies to every response, including unfinished ones. "
        "Takes precedence over the survey-level automatic retention. Leave "
        "empty or zero to fall back on the survey-level retention, or to keep "
        "the answers indefinitely when that is not enabled.",
    )

    def _cron_purge_expired_answers(self):
        # Delete answers older than each question's retention period.

        retention_questions = self._get_retention_questions()
        if not retention_questions:
            return

        now = fields.Datetime.now()
        answer_lines = self.env["survey.user_input.line"]
        deleted = self.env["survey.user_input.line"]
        # Group questions by their retention period and date field so each
        # group only needs one search for expired answers.
        questions_by_key = {}
        for question in retention_questions:
            questions_by_key.setdefault(
                (
                    question._get_effective_retention_days(),
                    question._get_retention_date_field(),
                ),
                [],
            ).append(question.id)
        for (retention_days, date_field), question_ids in questions_by_key.items():
            cutoff = now - relativedelta(days=retention_days)
            expired_lines = answer_lines.search(
                [
                    ("question_id", "in", question_ids),
                    (date_field, "<", cutoff),
                ]
            )
            deleted |= expired_lines
        if deleted:
            deleted.unlink()

    def _cron_purge_all_answers(self):
        # Delete every answer of questions that are under a retention policy.

        retention_questions = self._get_retention_questions()
        if not retention_questions:
            return

        answer_lines = self.env["survey.user_input.line"]
        deleted = answer_lines.search([("question_id", "in", retention_questions.ids)])
        if deleted:
            deleted.unlink()

    def _get_retention_questions(self):
        # Return questions whose answers must be purged by the cleanup.
        candidates = self.search(
            [
                "|",
                ("answer_retention_days", ">", 0),
                ("survey_id.answer_retention_auto", "=", True),
            ]
        )
        retention_questions = self.browse()
        for question in candidates:
            if question._get_effective_retention_days() > 0:
                retention_questions += question
        return retention_questions

    def _get_effective_retention_days(self):
        # Return the retention period applied to this question's answers.

        self.ensure_one()
        if self.answer_retention_days > 0:
            return self.answer_retention_days
        if self.survey_id.answer_retention_auto:
            # Reading system parameters requires superuser rights.
            parameter = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param(RETENTION_DAYS_PARAM, "0")
            )
            try:
                return max(int(parameter), 0)
            except ValueError:
                _logger.warning(
                    "Survey answer cleanup: system parameter %s has value %r "
                    "which is not an integer; survey-level retention is skipped.",
                    RETENTION_DAYS_PARAM,
                    parameter,
                )

        return 0

    def _get_retention_date_field(self):
        """Return the date field this question's answers are aged against."""

        self.ensure_one()
        return "create_date"
