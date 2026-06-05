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

        vals = {
            "user_input_id": self.id,
            "question_id": question.id,
            "answer_type": "suggestion",
            "skipped": True,
            "suggested_answer_id": False,
        }

        if answer:
            answer_id = int(answer)
            suggested_answer = question.suggested_answer_ids.filtered(
                lambda item: item.id == answer_id
            )

            _logger.info(
                "[model_select] resolved suggested_answer: "
                "question_id=%s answer_id=%s suggested_answer_ids=%s",
                question.id,
                answer_id,
                suggested_answer.ids,
            )

            if suggested_answer:
                vals.update(
                    {
                        "skipped": False,
                        "suggested_answer_id": suggested_answer.id,
                    }
                )

        _logger.info(
            "[model_select] writing user_input_line vals: "
            "user_input_id=%s question_id=%s old_answer_ids=%s vals=%r",
            self.id,
            question.id,
            old_answers.ids,
            vals,
        )

        if old_answers:
            old_answers.write(vals)
            result = old_answers
        else:
            result = self.env["survey.user_input.line"].create(vals)

        _logger.info(
            "[model_select] saved result: result_ids=%s answer_type=%s "
            "suggested_answer_ids=%s skipped=%s",
            result.ids,
            result.mapped("answer_type"),
            result.mapped("suggested_answer_id").ids,
            result.mapped("skipped"),
        )

        return result
