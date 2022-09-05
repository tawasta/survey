from odoo import api, fields, models


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
    answer_char_box_similarity = fields.Float(
        "Answer similarity %",
        help="How similar the answer must be. \n"
        "This can be used to compensate misspelling etc. \n"
        "A similarity of at least 80% is recommended.\n\n"
        "For example: \n"
        "'receive' and 'recieve' are 85% similiar\n"
        "'definitely' and 'definately' are 90% similiar",
        default="100.0",
    )

    @api.depends("answer_char_box")
    def _compute_is_scored_question_char_box(self):
        for question in self:
            if question.question_type == "char_box":
                if question.answer_char_box:
                    question.is_scored_question = True
                else:
                    question.is_scored_question = False
