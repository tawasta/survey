from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    question_image_ids = fields.One2many(
        "survey.question.image", "question_id", string="Question Images"
    )
