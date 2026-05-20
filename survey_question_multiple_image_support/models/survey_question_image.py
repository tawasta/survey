from odoo import fields, models


class SurveyQuestionImage(models.Model):
    _name = "survey.question.image"
    _description = "Survey Question Image"

    question_id = fields.Many2one("survey.question", required=True, ondelete="cascade")

    image_lang_id = fields.Many2one("res.lang", string="Language", required=True)

    question_image = fields.Image(
        string="Image", max_width=1920, max_height=1920, required=True
    )
