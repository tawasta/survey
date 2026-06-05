import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _save_lines(self, question, answer, comment=None, overwrite_existing=True):
        _logger.info(
            "[model_select] _save_lines: user_input_id=%s question_id=%s "
            "question_type=%s answer=%r",
            self.id,
            question.id,
            question.question_type,
            answer,
        )

        if question.question_type == "model_select":
            old_answers = self.env["survey.user_input.line"].search(
                [
                    ("user_input_id", "=", self.id),
                    ("question_id", "=", question.id),
                ]
            )

            _logger.info(
                "[model_select] old_answers: user_input_id=%s question_id=%s "
                "old_answer_ids=%s",
                self.id,
                question.id,
                old_answers.ids,
            )

            return self._save_line_model_select(question, old_answers, answer, comment)

        return super()._save_lines(
            question,
            answer,
            comment=comment,
            overwrite_existing=overwrite_existing,
        )

    def _save_line_model_select(self, question, old_answers, answer, comment=None):
        _logger.info(
            "[model_select] _save_line_model_select before extract: "
            "question_id=%s answer=%r",
            question.id,
            answer,
        )

        if isinstance(answer, dict):
            answer = (
                answer.get("value")
                or answer.get("suggested_answer_id")
                or answer.get("model_select_answer_id")
            )

        _logger.info(
            "[model_select] _save_line_model_select after extract: "
            "question_id=%s answer=%r",
            question.id,
            answer,
        )

        _logger.info(
            "[model_select] calling _save_line_choice: "
            "user_input_id=%s question_id=%s answer=%r old_answer_ids=%s",
            self.id,
            question.id,
            answer,
            old_answers.ids,
        )

        result = self._save_line_choice(question, old_answers, answer, comment)

        _logger.info(
            "[model_select] _save_line_choice result: "
            "user_input_id=%s question_id=%s result=%s result_ids=%s "
            "answer_type=%s suggested_answer_ids=%s skipped=%s",
            self.id,
            question.id,
            result,
            result.ids if result else False,
            result.mapped("answer_type") if result else False,
            result.mapped("suggested_answer_id").ids if result else False,
            result.mapped("skipped") if result else False,
        )

        return result
