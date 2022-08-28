from odoo import api
from odoo import fields
from odoo import models


class SurveyQuestion(models.Model):

    _inherit = "survey.question"

    answer_char_box = fields.Char(
        "Correct text answer", help="Correct text answer for this question.", default=""
    )
    answer_char_box_case_sensitive = fields.Boolean(
        "Case sensitive",
        help="Require a case sensitive answer",
        default=False,
    )

    @api.depends("answer_char_box")
    def _compute_is_scored_question_char_box(self):
        for question in self:
            if question.question_type == "char_box":
                if question.answer_char_box:
                    question.is_scored_question = True
                else:
                    question.is_scored_question = False
