from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    survey_lang_id = fields.Many2one(
        "res.lang",
        string="Survey Language",
        help="Language to use when printing surveys for this contact.",
    )
