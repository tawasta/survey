from odoo import fields, models


class SurveyUserInputTag(models.Model):
    _name = "survey.user_input.tag"

    name = fields.Char(required=True)

    color = fields.Integer(string="Color Index")

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Tag name already exists!"),
    ]
