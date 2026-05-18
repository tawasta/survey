from odoo import fields, models


class SurveyLanguage(models.Model):
    _name = "survey.language"
    _description = "Survey Language"
    _order = "sequence, id"

    name = fields.Char(string="Name", required=True, translate=True)
    code = fields.Char(string="Code", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    active = fields.Boolean(string="Active", default=True)
