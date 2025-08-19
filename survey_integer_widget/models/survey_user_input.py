from odoo import models, fields

class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    question_is_integer = fields.Boolean(
        related="question_id.is_integer_answer",
        store=True,
        readonly=True
    )

    def _compute_display_name(self):
        # ensin ajetaan alkuperäinen logiikka
        super()._compute_display_name()

        # sitten muokataan vain numeriset rivit tarvittaessa
        for line in self:
            if line.answer_type == "numerical_box" and line.question_is_integer:
                if line.value_numerical_box is not None:
                    try:
                        line.display_name = str(int(line.value_numerical_box))
                    except (TypeError, ValueError):
                        line.display_name = str(line.value_numerical_box)