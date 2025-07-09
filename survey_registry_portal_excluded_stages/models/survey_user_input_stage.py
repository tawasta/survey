from odoo import fields, models


class SurveyUserInputStage(models.Model):
    _inherit = "survey.user_input.stage"

    survey_registry_entries_always_hidden = fields.Boolean(
        string="Survey Registry: Entries Always Hidden",
        help="Responses in this stage are never shown in the survey registry",
    )
