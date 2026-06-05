# -*- coding: utf-8 -*-

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _save_lines(self, question, answer, comment=None, overwrite_existing=True):
        if question.question_type == "model_select":
            old_answers = self.env["survey.user_input.line"].search(
                [
                    ("user_input_id", "=", self.id),
                    ("question_id", "=", question.id),
                ]
            )
            return self._save_line_model_select(question, old_answers, answer, comment)

        return super()._save_lines(
            question,
            answer,
            comment=comment,
            overwrite_existing=overwrite_existing,
        )

    def _save_line_model_select(self, question, old_answers, answer, comment=None):
        if isinstance(answer, dict):
            answer = (
                answer.get("value")
                or answer.get("suggested_answer_id")
                or answer.get("model_select_answer_id")
            )

        return self._save_line_choice(question, old_answers, answer, comment)