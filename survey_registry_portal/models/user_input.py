import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    show_in_registry = fields.Boolean(
        string="Show Answers in Survey Registry",
        default=False,
        help="Indicates whether this survey response "
        "can be shown in the public registry.",
    )

    # Store answer-related fields at header level so that they can be used in search
    # filters and can be exported to xlsx. name everything "in survey registry" for
    # easier finding, even if not all fields are visible in the frontend registry.

    title_in_survey_registry = fields.Char(
        compute="_compute_title_in_survey_registry",
        store=True,
        copy=False,
        help="Title in survey registry, computed based on survey "
        "question configuration",
    )

    category_in_survey_registry = fields.Char(
        compute="_compute_category_in_survey_registry",
        store=True,
        copy=False,
        help="Category in survey registry, computed based on survey "
        "question configuration",
    )

    schedule_in_survey_registry = fields.Char(
        compute="_compute_schedule_in_survey_registry",
        store=True,
        copy=False,
        help="Schedule in survey registry, computed based on survey "
        "question configuration",
    )

    primary_implementer_in_survey_registry = fields.Char(
        compute="_compute_primary_implementer_in_survey_registry",
        store=True,
        copy=False,
        help="Primary implementer in survey registry, computed based on survey "
        "question configuration",
    )

    other_implementers_in_survey_registry = fields.Char(
        compute="_compute_other_implementers_in_survey_registry",
        store=True,
        copy=False,
        help="Other implementers in survey registry, computed based on survey "
        "question configuration",
    )

    funding_amount_applied_in_survey_registry = fields.Float(
        compute="_compute_funding_amount_applied_in_survey_registry",
        store=True,
        copy=False,
        help="Funding applied for in survey registry, computed based on survey "
        "question configuration",
    )

    funding_amount_total_in_survey_registry = fields.Float(
        compute="_compute_funding_amount_total_in_survey_registry",
        store=True,
        copy=False,
        help="Funding total in survey registry, computed based on survey "
        "question configuration",
    )

    subject_to_vat_in_survey_registry = fields.Char(
        compute="_compute_subject_to_vat_in_survey_registry",
        store=True,
        copy=False,
        help="Subject to VAT in survey registry, computed based on survey "
        "question configuration",
    )

    confirmed_funders_in_survey_registry = fields.Text(
        compute="_compute_confirmed_funders_in_survey_registry",
        store=True,
        copy=False,
        help="Confirmed_funders in survey registry, computed based on survey "
        "question configuration",
    )

    unconfirmed_funders_in_survey_registry = fields.Text(
        compute="_compute_unconfirmed_funders_in_survey_registry",
        store=True,
        copy=False,
        help="Unconfirmed_funders in survey registry, computed based on survey "
        "question configuration",
    )

    goals_in_survey_registry = fields.Text(
        compute="_compute_goals_in_survey_registry",
        store=True,
        copy=False,
        help="Goals in survey registry, computed based on survey "
        "question configuration",
    )

    implementation_in_survey_registry = fields.Text(
        compute="_compute_implementation_in_survey_registry",
        store=True,
        copy=False,
        help="Implementation in survey registry, computed based on survey "
        "question configuration",
    )

    progress_in_survey_registry = fields.Text(
        compute="_compute_progress_in_survey_registry",
        store=True,
        copy=False,
        help="Progress in survey registry, computed based on survey "
        "question configuration",
    )

    results_in_survey_registry = fields.Text(
        compute="_compute_results_in_survey_registry",
        store=True,
        copy=False,
        help="Results in survey registry, computed based on survey "
        "question configuration",
    )

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.use_answer_as_title_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.string_answer",
    )
    def _compute_title_in_survey_registry(self):
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            title_user_input_lines = survey_user_input_line_obj.sudo().search(
                [
                    ("question_id.use_answer_as_title_in_survey_registry", "=", True),
                    ("question_id.question_type", "=", "char_box"),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if title_user_input_lines:
                user_input.title_in_survey_registry = title_user_input_lines[
                    0
                ].string_answer
            else:
                user_input.title_in_survey_registry = "-"

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.use_answer_as_category_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.string_answer",
    )
    def _compute_category_in_survey_registry(self):
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            category_user_input_lines = survey_user_input_line_obj.sudo().search(
                [
                    (
                        "question_id.use_answer_as_category_in_survey_registry",
                        "=",
                        True,
                    ),
                    ("question_id.question_type", "=", "simple_choice"),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if category_user_input_lines:
                user_input.category_in_survey_registry = category_user_input_lines[
                    0
                ].string_answer
            else:
                user_input.category_in_survey_registry = "-"

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.use_answer_as_schedule_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.string_answer",
    )
    def _compute_schedule_in_survey_registry(self):
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            schedule_user_input_lines = survey_user_input_line_obj.sudo().search(
                [
                    (
                        "question_id.use_answer_as_schedule_in_survey_registry",
                        "=",
                        True,
                    ),
                    ("question_id.question_type", "in", ["char_box", "text_box"]),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if schedule_user_input_lines:
                user_input.schedule_in_survey_registry = schedule_user_input_lines[
                    0
                ].string_answer
            else:
                user_input.schedule_in_survey_registry = "-"

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.use_answer_as_primary_implementer_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.string_answer",
    )
    def _compute_primary_implementer_in_survey_registry(self):
        # Check which user input line contains the survey registry primary implementer
        # and store it, to be shown in website and used in backend search
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            primary_implementer_user_input_lines = survey_user_input_line_obj.sudo().search(  # noqa: E501,B950
                [
                    (
                        "question_id.use_answer_as_primary_implementer_in_survey_registry",
                        "=",
                        True,
                    ),
                    ("question_id.question_type", "in", ["char_box", "text_box"]),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if primary_implementer_user_input_lines:
                user_input.primary_implementer_in_survey_registry = (
                    primary_implementer_user_input_lines[0].string_answer
                )
            else:
                user_input.primary_implementer_in_survey_registry = "-"

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.use_answer_as_other_implementers_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.string_answer",
    )
    def _compute_other_implementers_in_survey_registry(self):
        # Check which user input line contains the survey registry other implementers
        # and store it, to be shown in website and used in backend search
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            other_implementers_user_input_lines = survey_user_input_line_obj.sudo().search(  # noqa: E501,B950
                [
                    (
                        "question_id.use_answer_as_other_implementers_in_survey_registry",  # noqa: E501,B950
                        "=",
                        True,
                    ),
                    ("question_id.question_type", "in", ["char_box", "text_box"]),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if other_implementers_user_input_lines:
                user_input.other_implementers_in_survey_registry = (
                    other_implementers_user_input_lines[0].string_answer
                )
            else:
                user_input.other_implementers_in_survey_registry = "-"

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.use_answer_as_funding_amount_applied_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.value_numerical_box",
    )
    def _compute_funding_amount_applied_in_survey_registry(self):
        # Check which user input line contains the funding applied amount
        # and store it
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            funding_amount_applied_user_input_lines = survey_user_input_line_obj.sudo().search(  # noqa: E501,B950
                [
                    (
                        "question_id.use_answer_as_funding_amount_applied_in_survey_registry",  # noqa: E501,B950
                        "=",
                        True,
                    ),
                    ("question_id.question_type", "=", "numerical_box"),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if funding_amount_applied_user_input_lines:
                user_input.funding_amount_applied_in_survey_registry = (
                    funding_amount_applied_user_input_lines[0].value_numerical_box
                )
            else:
                user_input.funding_amount_applied_in_survey_registry = 0

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.use_answer_as_funding_amount_total_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.value_numerical_box",
    )
    def _compute_funding_amount_total_in_survey_registry(self):
        # Check which user input line contains the funding total amount
        # and store it
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            funding_amount_total_user_input_lines = survey_user_input_line_obj.sudo().search(  # noqa: E501,B950
                [
                    (
                        "question_id.use_answer_as_funding_amount_total_in_survey_registry",  # noqa: E501,B950
                        "=",
                        True,
                    ),
                    ("question_id.question_type", "=", "numerical_box"),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if funding_amount_total_user_input_lines:
                user_input.funding_amount_total_in_survey_registry = (
                    funding_amount_total_user_input_lines[0].value_numerical_box
                )
            else:
                user_input.funding_amount_total_in_survey_registry = 0

    # TODO fill in actual calculation

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.use_answer_as_subject_to_vat_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.string_answer",
    )
    def _compute_subject_to_vat_in_survey_registry(self):
        # Check which user input line contains the funding applied amount
        # and store it
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            subject_to_vat_user_input_lines = survey_user_input_line_obj.sudo().search(  # noqa: E501,B950
                [
                    (
                        "question_id.use_answer_as_subject_to_vat_in_survey_registry",
                        "=",
                        True,
                    ),
                    ("question_id.question_type", "=", "simple_choice"),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if subject_to_vat_user_input_lines:
                user_input.subject_to_vat_in_survey_registry = (
                    subject_to_vat_user_input_lines[0].string_answer
                )
            else:
                user_input.subject_to_vat_in_survey_registry = "-"

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.use_answer_as_confirmed_funders_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.string_answer",
    )
    def _compute_confirmed_funders_in_survey_registry(self):
        _logger.info("recalc confirmed funders")
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            confirmed_funders_user_input_lines = survey_user_input_line_obj.sudo().search(  # noqa: E501,B950
                [
                    (
                        "question_id.use_answer_as_confirmed_funders_in_survey_registry",
                        "=",
                        True,
                    ),
                    ("question_id.question_type", "in", ["char_box", "text_box"]),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if confirmed_funders_user_input_lines:
                user_input.confirmed_funders_in_survey_registry = (
                    confirmed_funders_user_input_lines[0].string_answer
                )
            else:
                user_input.confirmed_funders_in_survey_registry = "-"

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.use_answer_as_unconfirmed_funders_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.string_answer",
    )
    def _compute_unconfirmed_funders_in_survey_registry(self):
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            unconfirmed_funders_user_input_lines = survey_user_input_line_obj.sudo().search(  # noqa: E501,B950
                [
                    (
                        "question_id.use_answer_as_unconfirmed_funders_in_survey_registry",
                        "=",
                        True,
                    ),
                    ("question_id.question_type", "in", ["char_box", "text_box"]),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if unconfirmed_funders_user_input_lines:
                user_input.unconfirmed_funders_in_survey_registry = (
                    unconfirmed_funders_user_input_lines[0].string_answer
                )
            else:
                user_input.unconfirmed_funders_in_survey_registry = "-"

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.use_answer_as_goals_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.string_answer",
    )
    def _compute_goals_in_survey_registry(self):
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            goals_user_input_lines = survey_user_input_line_obj.sudo().search(  # noqa: E501,B950
                [
                    (
                        "question_id.use_answer_as_goals_in_survey_registry",
                        "=",
                        True,
                    ),
                    ("question_id.question_type", "in", ["char_box", "text_box"]),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if goals_user_input_lines:
                user_input.goals_in_survey_registry = goals_user_input_lines[
                    0
                ].string_answer
            else:
                user_input.goals_in_survey_registry = "-"

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.use_answer_as_implementation_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.string_answer",
    )
    def _compute_implementation_in_survey_registry(self):
        # Check which user input line contains the funding applied amount
        # and store it
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            implementation_user_input_lines = survey_user_input_line_obj.sudo().search(  # noqa: E501,B950
                [
                    (
                        "question_id.use_answer_as_implementation_in_survey_registry",
                        "=",
                        True,
                    ),
                    ("question_id.question_type", "in", ["char_box", "text_box"]),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if implementation_user_input_lines:
                user_input.implementation_in_survey_registry = (
                    implementation_user_input_lines[0].string_answer
                )
            else:
                user_input.implementation_in_survey_registry = "-"

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.use_answer_as_progress_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.string_answer",
    )
    def _compute_progress_in_survey_registry(self):
        # Check which user input line contains the funding applied amount
        # and store it
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            progress_user_input_lines = survey_user_input_line_obj.sudo().search(  # noqa: E501,B950
                [
                    (
                        "question_id.use_answer_as_progress_in_survey_registry",
                        "=",
                        True,
                    ),
                    ("question_id.question_type", "in", ["char_box", "text_box"]),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if progress_user_input_lines:
                user_input.progress_in_survey_registry = progress_user_input_lines[
                    0
                ].string_answer
            else:
                user_input.progress_in_survey_registry = "-"

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.use_answer_as_results_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.string_answer",
    )
    def _compute_results_in_survey_registry(self):
        # Check which user input line contains the funding applied amount
        # and store it
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            results_user_input_lines = survey_user_input_line_obj.sudo().search(  # noqa: E501,B950
                [
                    (
                        "question_id.use_answer_as_results_in_survey_registry",
                        "=",
                        True,
                    ),
                    ("question_id.question_type", "in", ["char_box", "text_box"]),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if results_user_input_lines:
                user_input.results_in_survey_registry = results_user_input_lines[
                    0
                ].string_answer
            else:
                user_input.results_in_survey_registry = "-"

    def _save_line_choice(self, question, old_answers, answers, comment):
        # Ota raakavastaus talteen ennen kuin super() muokkaa sitä
        raw_answer = None
        if (
            question.question_type == "simple_choice"
            and question.save_as_registry_visibility
        ):
            raw_answer = self.env["survey.question.answer"].browse(int(answers))
        # Kutsu super-metodi
        result = super()._save_line_choice(question, old_answers, answers, comment)

        # Aseta näkyvyystieto superin jälkeen
        if raw_answer:
            normalized = raw_answer.value.strip().lower()
            visibility = normalized in ("kyllä", "yes", "true", "1")
            self.write({"show_in_registry": visibility})

        return result
