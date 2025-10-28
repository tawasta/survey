from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    # Defines which fields of a survey.user_input model, i.e. in addition to the
    # actual answers, will be shown in survey registry
    survey_registry_field_line_ids = fields.One2many(
        "survey.registry.field.line",
        "survey_id",
        string="User Input Fields to Show in Survey Registry",
        help="If this survey's answers are shown in the Survey Registry, you can "
        "select what fields (in addition to the actual answers) gets shown there, "
        "e.g. the status of the answer.",
    )
