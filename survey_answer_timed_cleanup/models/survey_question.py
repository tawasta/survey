from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


def _get_field_value(record, field_path):
    # Return the value of a dotted field path on one record, the way a search
    # domain uses it: "event_id.date_begin" is the event's start date.

    for part in field_path.split("."):
        record = record[part]
    return record


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    answer_retention_enabled = fields.Boolean(
        string="Enable Answer Data Retention",
        help="If enabled, answers to this question are automatically deleted "
        "after a certain number of days.",
    )

    answer_retention_days = fields.Integer(
        string="Answer Data Retention (days)",
        help="Number of days an answer to this question is kept before it is "
        "deleted by the scheduled cleanup action, counted from when the answer "
        "was recorded. Applies to every response, including unfinished ones. "
        "Leave empty or zero to keep the answers indefinitely.",
    )

    survey_scoring_type = fields.Selection(
        related="survey_id.scoring_type",
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

    def _get_retention_questions(self):
        # Return questions whose answers must be purged by the cleanup.
        return self.search([("answer_retention_days", ">", 0)])

    def _get_effective_retention_days(self):
        # Return the retention period applied to this question's answers.

        self.ensure_one()
        return self.answer_retention_days

    # Set answer_retention_days to 0 if user sets answer_retention_enabled to False
    @api.onchange("answer_retention_enabled")
    def _onchange_answer_retention_enabled(self):
        if not self.answer_retention_enabled:
            self.answer_retention_days = 0

    def _get_retention_date_field(self):
        """Return the date field this question's answers are aged against."""

        self.ensure_one()
        return "create_date"
