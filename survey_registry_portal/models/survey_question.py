from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SurveyQuestion(models.Model):
    # 1. Private attributes
    _inherit = "survey.question"

    # 2. Fields declaration

    save_as_registry_visibility = fields.Boolean(
        string="Answer Controls Registry Visibility",
        compute="_compute_save_as_registry_visibility",
        readonly=False,
        store=True,
        copy=True,
        help="If checked and the question is a simple choice, the answer 'Yes' "
        "will automatically set the participation to be visible in the survey "
        "registry.",
    )

    show_answer_in_survey_registry = fields.Boolean(
        help="If checked, the answer to this question will be shown on the website "
        "in the survey registry."
    )

    format_as_monetary_in_survey_registry = fields.Boolean(
        help="If checked, a numeric amount will be formatted as a monetary amount, "
        "e.g. 12.34 and be suffixed with a currency symbol"
    )

    # TODO: implement multicurrency support if needed. Currently just gets the
    # company currency silently in the background
    survey_registry_currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
    )

    use_answer_as_title_in_survey_registry = fields.Boolean(
        help="If checked, the answer to this question will be used as the title "
        "in the survey registry."
    )

    # 3. Default methods

    # 4. Compute and search fields
    @api.depends("question_type")
    def _compute_save_as_registry_visibility(self):
        for question in self:
            if question.question_type != "simple_choice":
                question.save_as_registry_visibility = False

    @api.constrains("use_answer_as_title_in_survey_registry", "survey_id")
    def _check_unique_registry_name_per_survey(self):
        # Ensure that not more than one question's answer is trying to be used as the
        # title in survey registry
        for question in self:
            if question.use_answer_as_title_in_survey_registry:
                count = self.sudo().search_count(
                    [
                        ("survey_id", "=", question.survey_id.id),
                        ("use_answer_as_title_in_survey_registry", "=", True),
                        ("id", "!=", question.id),
                    ]
                )
                if count:
                    raise ValidationError(
                        _(
                            "Only one question per survey can be marked with "
                            "'Use Answer as Title in Survey Registry'."
                        )
                    )
