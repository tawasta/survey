from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    parent_survey_id = fields.Many2one(
        "survey.survey",
        string="Origin Survey",
        help="The parent survey",
    )

    child_survey_ids = fields.One2many(
        "survey.survey",
        "parent_survey_id",
        string="Follow-Up Surveys",
        help="The child surveys",
    )
