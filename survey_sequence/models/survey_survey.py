from odoo import fields, models


class Survey(models.Model):
    _inherit = "survey.survey"
    _order = "sequence, id"

    sequence = fields.Integer(
        "Sequence", default=1, help="Gives the sequence order for Surveys"
    )
