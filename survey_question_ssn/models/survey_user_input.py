from odoo import models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _save_lines(self, question, answer, comment=None, overwrite_existing=False):
        old_answers = self.env["survey.user_input.line"].search(
            [
                ("user_input_id", "=", self.id),
                ("question_id", "=", question.id),
            ]
        )
        if question.question_type == "ssn":
            res = self._save_line_ssn_answer(question, old_answers, answer)
        else:
            res = super()._save_lines(question, answer, comment, overwrite_existing)
        return res

    def _save_line_ssn_answer(self, question, old_answers, answer):
        vals = {
            "user_input_id": self.id,
            "question_id": question.id,
            "skipped": not answer,
            "answer_type": "ssn",
            "value_ssn": answer,
        }

        if old_answers:
            old_answers.write(vals)
            return old_answers
        else:
            new_answer = self.env["survey.user_input.line"].create(vals)
            new_answer.user_input_id.partner_id.sudo().write(
                {"social_security_number": answer}
            )

            return new_answer
