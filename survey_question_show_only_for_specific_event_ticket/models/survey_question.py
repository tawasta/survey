from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    event_ticket_ids = fields.Many2many(
        comodel_name="event.event.ticket",
        relation="survey_question_event_ticket_rel",
        column1="question_id",
        column2="ticket_id",
        string="Show only for Specific Event Tickets",
        help="If set, this question is only shown on event questionnaires "
        "if the event registrant is buying one of these tickets",
    )
