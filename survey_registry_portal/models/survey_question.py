from odoo import api, fields, models


class SurveyQuestion(models.Model):
    # 1. Private attributes
    _inherit = "survey.question"

    # 2. Fields declaration
    save_as_registry_visibility = fields.Boolean(
        string="Save as registry visibility",
        compute="_compute_save_as_registry_visibility",
        readonly=False,
        store=True,
        copy=True,
        help="If checked, saves user's answer as registry visibility status.",
    )

    # 3. Default methods

    # 4. Compute and search fields
    @api.depends("question_type")
    def _compute_save_as_registry_visibility(self):
        for question in self:
            if question.question_type != "simple_choice":
                question.save_as_registry_visibility = False
