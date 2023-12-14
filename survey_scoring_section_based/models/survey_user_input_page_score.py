from odoo import api, fields, models


class SurveyUserInputPageScore(models.Model):

    _name = "survey.user_input_page_score"

    # if participation gets deleted, delete also the page score
    survey_user_input_id = fields.Many2one(
        string="Participation", comodel_name="survey.user_input", ondelete="cascade"
    )

    page_id = fields.Many2one(string="Section", comodel_name="survey.question")

    page_minimum_required_score = fields.Float(
        string="Section Minimum Score", related="page_id.page_minimum_required_score"
    )

    page_achieved_score = fields.Float(
        string="Section Achieved Score",
        compute="_compute_page_achieved_score",
        store=True,
    )

    page_minimum_score_passed = fields.Boolean(
        string="Section Minimum Score Passed",
        compute="_compute_page_minimum_score_passed",
        store=True,
    )

    @api.depends(
        "page_minimum_required_score",
        "survey_user_input_id",
        "survey_user_input_id.user_input_line_ids",
        "survey_user_input_id.user_input_line_ids.answer_score",
    )
    def _compute_page_achieved_score(self):
        """
        Compute the total score of all the questions that are children of the
        section
        """
        for record in self:

            user_input_lines = self.env["survey.user_input.line"].search(
                [
                    ("user_input_id", "=", record.survey_user_input_id.id),
                    ("question_id.page_id", "=", record.page_id.id),
                ]
            )

            record.page_achieved_score = sum(
                [uil.answer_score for uil in user_input_lines]
            )

    @api.depends("page_minimum_required_score", "page_achieved_score")
    def _compute_page_minimum_score_passed(self):
        # Check if the section's minimum score requirement was met
        for record in self:
            record.page_minimum_score_passed = (
                record.page_achieved_score >= record.page_minimum_required_score
            )
