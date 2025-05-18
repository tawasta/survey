from odoo import fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    parent_survey_user_input_id = fields.Many2one(
        "survey.user_input",
        string="Origin Survey Response",
        help="The parent survey participation",
    )

    child_survey_user_input_ids = fields.One2many(
        "survey.user_input",
        "parent_survey_user_input_id",
        string="Follow-Up Survey Responses",
        help="The child survey participations",
    )
