from odoo import fields, models


class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    survey_question_ids = fields.Many2many(
        comodel_name="survey.question",
        relation="survey_question_event_ticket_rel",
        column1="ticket_id",
        column2="question_id",
        string="Questions Specific to this Event Ticket",
        help="Questions that have been configured to be asked when "
        "event registrant is buying this ticket",
    )
