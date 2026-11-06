from odoo import models


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    def _timed_cleanup_log_purged(self):
        """Tell each response which questions the retention cleanup purged."""

        questions_by_input = {}

        for line in self:
            questions_by_input.setdefault(
                line.user_input_id, self.env["survey.question"]
            )
            questions_by_input[line.user_input_id] |= line.question_id
        user_inputs = self.env["survey.user_input"]
        bodies = {}

        for user_input, questions in questions_by_input.items():
            user_inputs |= user_input
            bodies[user_input.id] = user_input._timed_cleanup_message_body(questions)
        user_inputs._message_log_batch(bodies)
