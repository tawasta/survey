from odoo import _, api, fields, models


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

    survey_is_event_survey = fields.Boolean(
        related="survey_id.is_event_survey",
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

    @api.onchange("answer_retention_date_basis")
    def _onchange_answer_retention_date_basis(self):
        """Keep the event bases unreachable for non-event surveys."""

        event_basis = self.answer_retention_date_basis in ("start", "end")
        if event_basis and not self.survey_is_event_survey:
            self.answer_retention_date_basis = "answer_date"
            return {
                "warning": {
                    "title": _("Warning"),
                    "message": _("Survey not linked to any event."),
                    "type": "notification",
                }
            }
