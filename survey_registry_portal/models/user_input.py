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

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.show_answer_in_survey_registry",
        "user_input_line_ids.question_id.use_answer_as_title_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.value_char_box",
    )
    def _compute_title_in_survey_registry(self):
        # Check which user input line contains the survey registry title and store it,
        # to be shown in website and used in backend search
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            title_user_input_lines = survey_user_input_line_obj.sudo().search(
                [
                    ("question_id.show_answer_in_survey_registry", "=", True),
                    ("question_id.use_answer_as_title_in_survey_registry", "=", True),
                    ("question_id.question_type", "=", "char_box"),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if title_user_input_lines:
                user_input.title_in_survey_registry = title_user_input_lines[
                    0
                ].value_char_box
            else:
                user_input.title_in_survey_registry = "-"

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.show_answer_in_survey_registry",
        "user_input_line_ids.question_id.use_answer_as_category_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.value_char_box",
    )
    def _compute_category_in_survey_registry(self):
        # Check which user input line contains the survey registry category and
        # store it, to be shown in website and used in backend search
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            category_user_input_lines = survey_user_input_line_obj.sudo().search(
                [
                    ("question_id.show_answer_in_survey_registry", "=", True),
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
        "user_input_line_ids.question_id.show_answer_in_survey_registry",
        "user_input_line_ids.question_id.use_answer_as_schedule_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.value_char_box",
    )
    def _compute_schedule_in_survey_registry(self):
        # Check which user input line contains the survey registry schedule and
        # store it, to be shown in website and used in backend search
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            schedule_user_input_lines = survey_user_input_line_obj.sudo().search(
                [
                    ("question_id.show_answer_in_survey_registry", "=", True),
                    (
                        "question_id.use_answer_as_schedule_in_survey_registry",
                        "=",
                        True,
                    ),
                    ("question_id.question_type", "=", "char_box"),
                    ("user_input_id", "=", user_input.id),
                ],
                limit=1,
            )

            if schedule_user_input_lines:
                user_input.schedule_in_survey_registry = schedule_user_input_lines[
                    0
                ].value_char_box
            else:
                user_input.schedule_in_survey_registry = "-"

    @api.depends(
        "user_input_line_ids",
        "user_input_line_ids.question_id.show_answer_in_survey_registry",
        "user_input_line_ids.question_id.use_answer_as_primary_implementer_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.value_char_box",
    )
    def _compute_primary_implementer_in_survey_registry(self):
        # Check which user input line contains the survey registry primary implementer
        # and store it, to be shown in website and used in backend search
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            primary_implementer_user_input_lines = survey_user_input_line_obj.sudo().search(  # noqa: E501,B950
                [
                    ("question_id.show_answer_in_survey_registry", "=", True),
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
        "user_input_line_ids.question_id.show_answer_in_survey_registry",
        "user_input_line_ids.question_id.use_answer_as_other_implementers_in_survey_registry",
        "user_input_line_ids.question_id.question_type",
        "user_input_line_ids.value_char_box",
    )
    def _compute_other_implementers_in_survey_registry(self):
        # Check which user input line contains the survey registry other implementers
        # and store it, to be shown in website and used in backend search
        survey_user_input_line_obj = self.env["survey.user_input.line"]

        for user_input in self:
            other_implementers_user_input_lines = survey_user_input_line_obj.sudo().search(  # noqa: E501,B950
                [
                    ("question_id.show_answer_in_survey_registry", "=", True),
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
