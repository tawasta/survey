from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    answer_button_text = fields.Char(
        translate=True,
        help="Enter a custom label for the 'Start Survey'"
        " or 'Start Certification' button. "
        "Leave empty to use the default text.",
    )
