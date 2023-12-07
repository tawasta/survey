from odoo import fields, models


class SurveyUserInput(models.Model):

    _inherit = "survey.user_input"

    active = fields.Boolean(
        default=True,
    )
