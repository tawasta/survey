from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SurveyUserInputLine(models.Model):

    _inherit = "survey.user_input.line"

    answer_type = fields.Selection(
        selection_add=[('ssn', 'SSN')],
    )
