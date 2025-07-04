from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    answer_button_text = fields.Char(
        string="Answer Button Text", translate=True
    )
