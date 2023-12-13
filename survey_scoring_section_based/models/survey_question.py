from odoo import fields, models


class SurveyQuestion(models.Model):

    _inherit = "survey.question"

    scoring_based_on_pages = fields.Boolean(
        related="survey_id.scoring_based_on_pages", store=True
    )

    page_minimum_required_score = fields.Float(
        string="Section Minimum Score",
        help="When the Surveys uses scoring and section-specific score limits, fill "
        "in this field to specify how many points are required in total from this "
        "section's questions in order to pass. ",
    )
