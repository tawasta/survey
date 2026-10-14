from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    answer_retention_date_basis = fields.Selection(
        selection=[
            ("answer_date", "Answer Date"),
            ("start", "Event Start Date"),
            ("end", "Event End Date"),
        ],
        string="Answer Data Retention Basis",
        default="answer_date",
        help="Which date the answer retention period of this question is "
        "counted from. Has an effect only when a retention period applies to "
        "the question. The event date options purge only answers linked to "
        "an event.",
    )

    def _get_retention_date_field(self):
        """Map the retention basis to the date field the base cleanup cron
        ages answers against."""

        self.ensure_one()
        if self.answer_retention_date_basis == "start":
            return "event_id.date_begin"
        if self.answer_retention_date_basis == "end":
            return "event_id.date_end"
        return super()._get_retention_date_field()
