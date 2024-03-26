from odoo.addons.survey.controllers.main import Survey


class Survey(Survey):
    def _prepare_survey_finished_values(self, survey, answer, token=False):
        """
        Calculate the total score, to be shown in the thank you page.
        """

        result = super(Survey, self)._prepare_survey_finished_values(
            survey, answer, token
        )

        if survey.show_numeric_score_to_participant:

            numeric_score = sum(
                user_input_line.answer_score
                for user_input_line in answer.user_input_line_ids
            )

            # Trim trailing .0 from the shown score
            if numeric_score.is_integer():
                result["numeric_score"] = int(numeric_score)
            else:
                result["numeric_score"] = numeric_score

        return result
