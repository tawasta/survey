from odoo import fields, models


class SurveySurvey(models.Model):

    _inherit = "survey.survey"

    show_numeric_score_to_participant = fields.Boolean(
        "Show Numeric Score to Participant",
        help="The participant can see their numeric score on the screen after answering",
    )
