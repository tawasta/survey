from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    # Only the groups are changed, the other attributes come from the core field
    user_input_ids = fields.One2many(
        groups="survey.group_survey_user,"
        "survey_invite_group_access.group_survey_invite_reader",
    )
