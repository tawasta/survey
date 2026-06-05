from odoo import fields, models


class SurveyQuestionAnswer(models.Model):
    _inherit = "survey.question.answer"

    model_select_res_model = fields.Char(
        string="Source Model",
        readonly=True,
        copy=True,
    )

    model_select_res_id = fields.Integer(
        string="Source Record ID",
        readonly=True,
        copy=True,
    )
