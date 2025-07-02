import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    parent_survey_user_input_id = fields.Many2one(
        "survey.user_input",
        string="Origin Survey Response",
        help="The parent survey participation",
    )

    child_survey_user_input_ids = fields.One2many(
        "survey.user_input",
        "parent_survey_user_input_id",
        string="Follow-Up Survey Responses",
        help="The child survey participations",
    )

    child_survey_user_input_line_ids = fields.One2many(
        comodel_name="survey.user_input.line",
        inverse_name="user_input_id",
        string="Follow-up's Survey Response Lines",
        compute="_compute_child_survey_user_input_line_ids",
        store=False,
    )

    @api.depends(
        "child_survey_user_input_ids", "child_survey_user_input_ids.user_input_line_ids"
    )
    def _compute_child_survey_user_input_line_ids(self):
        # Get all the answers of the follow-up record so they can be shown on the
        # parent's form
        for record in self:
            child_lines = self.env["survey.user_input.line"]
            for child in record.child_survey_user_input_ids:
                child_lines |= child.user_input_line_ids
            record.child_survey_user_input_line_ids = child_lines
