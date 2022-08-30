from odoo import fields, models


class SurveySurvey(models.Model):

    _inherit = "survey.survey"

    show_answers = fields.Boolean(
        "Show answers", default=False, help="Show correct answers after the survey"
    )
