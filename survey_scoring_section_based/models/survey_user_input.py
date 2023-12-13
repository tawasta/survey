from odoo import api, fields, models


class SurveyUserInput(models.Model):

    _inherit = "survey.user_input"

    @api.depends("survey_id.question_and_page_ids")
    def _compute_user_input_page_scores(self):
        # Compute on the fly all the section-specific scores
        for record in self:
            if record.survey_id.scoring_based_on_pages:

                # Iterate through all the sections fo the parent survey
                related_pages = self.env["survey.question"].search(
                    [("is_page", "=", True), ("survey_id", "=", record.survey_id.id)]
                )

                new_user_input_page_score_ids = []

                # Create new records for each section
                for page in related_pages:
                    new_user_input_page_score = self.env[
                        "survey.user_input_page_score"
                    ].create({"page_id": page.id, "survey_user_input_id": record.id})

                    new_user_input_page_score_ids.append(new_user_input_page_score.id)

                # Link the new records to the current participation (and delete any
                # old computations)
                record.user_input_page_score_ids = [
                    (6, 0, new_user_input_page_score_ids)
                ]
            else:
                # No calculation needed if section-specific scoring not in use
                record.user_input_page_score_ids = [(5, 0, 0)]

    user_input_page_score_ids = fields.Many2many(
        comodel_name="survey.user_input_page_score",
        string="Section-specific scores",
        compute="_compute_user_input_page_scores",
    )

    @api.depends(
        "scoring_percentage",
        "user_input_page_score_ids",
        "survey_id",
        "survey_id.scoring_success_min",
        "survey_id.scoring_based_on_pages",
    )
    def _compute_scoring_success(self):

        super()._compute_scoring_success()
        for record in self:
            # Check also the section specific scores when calculating if
            # "Quizz passed" checkbox gets checked
            if record.survey_id.scoring_based_on_pages:

                if any(
                    not user_input_page_score.page_minimum_score_passed
                    for user_input_page_score in record.user_input_page_score_ids
                ):
                    record.scoring_success = False
