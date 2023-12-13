from odoo import fields, models


class SurveyUserInputLine(models.Model):

    _inherit = "survey.user_input.line"

    active = fields.Boolean(
        default=True,
    )
