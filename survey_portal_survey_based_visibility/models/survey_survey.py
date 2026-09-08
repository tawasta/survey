from odoo import fields, models


class Survey(models.Model):
    _inherit = "survey.survey"

    hide_survey_result_in_portal = fields.Boolean(
        string="Hide Survey Result in Portal",
        default=False,
        help="Hide the answers of this survey from the portal survey answers "
        "list. If checked, portal users cannot see or open their answers "
        "of this survey.",
    )
