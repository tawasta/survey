from odoo import fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    tag_ids = fields.Many2many(comodel_name="survey.user_input.tag", string="Tags")
