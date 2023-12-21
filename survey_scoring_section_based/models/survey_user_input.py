from odoo import api, fields, models


class SurveyUserInput(models.Model):

    _inherit = "survey.user_input"

    user_input_page_score_ids = fields.One2many(
        comodel_name="survey.user_input_page_score",
        inverse_name="survey_user_input_id",
        string="Section-specific scores",
    )

    @api.depends(
        "scoring_percentage",
        "user_input_page_score_ids",
        "user_input_page_score_ids.page_minimum_score_passed",
        "survey_id",
        "survey_id.scoring_success_min",
        "survey_id.scoring_based_on_pages",
    )
    def _compute_scoring_success(self):
        """
        Check also the section specific scores when calculating if
        "Quizz passed" checkbox gets checked
        """
        super()._compute_scoring_success()
        for record in self:

            if record.survey_id.scoring_based_on_pages:

                if any(
                    not user_input_page_score.page_minimum_score_passed
                    for user_input_page_score in record.user_input_page_score_ids
                ):
                    record.scoring_success = False

    def create(self, values):
        """
        When a participation gets created, create section specific score records for it,
        one per section
        """
        res = super().create(values)

        if res.survey_id.scoring_based_on_pages:
            for qp in res.survey_id.question_and_page_ids:
                if qp.is_page:
                    self.env["survey.user_input_page_score"].create(
                        {"survey_user_input_id": res.id, "page_id": qp.id}
                    )

        return res
