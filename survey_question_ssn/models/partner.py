from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    social_security_number = fields.Char(
        "Personal identification number", invisible=True
    )
