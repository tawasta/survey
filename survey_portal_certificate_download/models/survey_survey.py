from odoo import fields, models


class Survey(models.Model):
    _inherit = "survey.survey"

    certification_downloadable_in_portal = fields.Boolean(
        string="Certificate Downloadable in Portal",
        default=False,
        help="Allow portal users to download their certificate "
        "from the survey answers list in the portal.",
    )
