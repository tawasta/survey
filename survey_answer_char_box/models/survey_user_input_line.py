from odoo import api
from odoo import fields
from odoo import models
from odoo import _


class SurveyUserInputLine(models.Model):

    _inherit = "survey.user_input.line"

    @api.model
    def _get_answer_score_values(self, vals, compute_speed_score=True):
        user_input_id = vals.get("user_input_id")
        answer_type = vals.get("answer_type")
        question_id = vals.get("question_id")
        if not question_id:
            raise ValueError(_("Computing score requires a question in arguments."))
        question = self.env["survey.question"].browse(int(question_id))

        if answer_type != "char_box":
            return super()._get_answer_score_values(vals, compute_speed_score)

        # default and non-scored questions
        answer_is_correct = False
        answer_score = 0

        if question.is_scored_question:
            answer = vals.get("value_%s" % answer_type)
            if answer_type == "char_box":
                answer = answer

            correct_answer = question["answer_char_box"]
            if answer and question.answer_char_box_case_sensitive:
                answer_is_correct = answer == correct_answer
            else:
                answer_is_correct = answer.lower() == correct_answer.lower()
            if answer_is_correct:
                answer_score = question.answer_score

        if compute_speed_score and answer_score > 0:
            user_input = self.env["survey.user_input"].browse(user_input_id)
            session_speed_rating = (
                user_input.exists()
                and user_input.is_session_answer
                and user_input.survey_id.session_speed_rating
            )
            if session_speed_rating:
                max_score_delay = 2
                time_limit = question.time_limit
                now = fields.Datetime.now()
                seconds_to_answer = (
                    now - user_input.survey_id.session_question_start_time
                ).total_seconds()
                question_remaining_time = time_limit - seconds_to_answer
                # if answered within the max_score_delay => leave score as is
                if question_remaining_time < 0:  # if no time left
                    answer_score /= 2
                elif seconds_to_answer > max_score_delay:
                    time_limit -= max_score_delay  # we remove the max_score_delay to have all possible values
                    score_proportion = (time_limit - seconds_to_answer) / time_limit
                    answer_score = (answer_score / 2) * (1 + score_proportion)

        return {"answer_is_correct": answer_is_correct, "answer_score": answer_score}
