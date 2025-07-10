from odoo import fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    internal_notes = fields.Text()
