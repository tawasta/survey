from odoo import models, fields

class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    is_integer_answer = fields.Boolean(
        string="Force Integer Answer",
        help="If set, numerical answers to this question will be displayed as integers."
    )
