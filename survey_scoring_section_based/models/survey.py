from odoo import fields, models


class Survey(models.Model):

    _inherit = "survey.survey"

    scoring_based_on_pages = fields.Boolean(
        string="Use Section-specific Score Limits",
        description="Enables setting the amount of points required "
        "for each section, in order to pass.",
    )
