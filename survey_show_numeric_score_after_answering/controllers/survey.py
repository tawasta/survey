from odoo.addons.survey.controllers.main import Survey


class Survey(Survey):
    def _prepare_survey_finished_values(self, survey, answer, token=False):
        """
        Calculate the total score, to be shown in the thank you page.
        """

        result = super(Survey, self)._prepare_survey_finished_values(
            survey, answer, token
        )

        if (
            survey.scoring_type != "no_scoring"
            and survey.show_numeric_score_to_participant
        ):

            # Trim trailing .0 from the shown score
            if answer.scoring_total.is_integer():
                result["numeric_score"] = int(answer.scoring_total)
            else:
                result["numeric_score"] = answer.scoring_total

        return result
