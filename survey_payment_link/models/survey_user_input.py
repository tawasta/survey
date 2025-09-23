from odoo import fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    payment_ids = fields.One2many(
        "account.payment",
        "survey_user_input_id",
        string="Payments",
        help="Payments linked to this survey input (project/grant/etc).",
    )
