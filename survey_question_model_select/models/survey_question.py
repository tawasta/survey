import ast
import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    question_type = fields.Selection(
        selection_add=[("model_select", "Odoo Model Dropdown")],
        ondelete={"model_select": "set null"},
    )

    model_select_model_id = fields.Many2one(
        comodel_name="ir.model",
        string="Dropdown Model",
        domain=[
            ("transient", "=", False),
            ("model", "not ilike", "ir.%"),
        ],
        help="Select the Odoo model whose records are used to create dropdown answers.",
    )

    model_select_model = fields.Char(
        string="Technical Model",
        related="model_select_model_id.model",
        readonly=True,
    )

    model_select_domain = fields.Char(
        string="Condition Domain",
        default="[]",
        help="Domain used to fetch answer values from the selected model.",
    )

    model_select_limit = fields.Integer(
        string="Maximum Values",
        default=200,
        help="Maximum number of values generated from the selected model.",
    )

    @api.constrains(
        "question_type",
        "model_select_model_id",
        "model_select_domain",
        "model_select_limit",
    )
    def _check_model_select_configuration(self):
        for question in self:
            if question.question_type != "model_select":
                continue

            if not question.model_select_model_id:
                raise ValidationError(_("Please select a dropdown model."))

            if question.model_select_limit <= 0:
                raise ValidationError(_("Maximum Values must be greater than zero."))

            question._get_model_select_domain()

    @api.onchange("model_select_model_id")
    def _onchange_model_select_model_id(self):
        for question in self:
            if question.question_type == "model_select":
                question.model_select_domain = "[]"

    def validate_question(self, answer, comment=None):
        self.ensure_one()

        if self.question_type != "model_select":
            return super().validate_question(answer, comment)

        if isinstance(answer, dict):
            answer = (
                answer.get("value")
                or answer.get("suggested_answer_id")
                or answer.get("model_select_answer_id")
            )

        if isinstance(answer, str):
            answer = answer.strip()

        if self.constr_mandatory and not answer:
            return {
                self.id: self.constr_error_msg or _("This question requires an answer.")
            }

        if not answer:
            return {}

        try:
            answer_id = int(answer)
        except (TypeError, ValueError):
            return {self.id: _("Invalid selected value.")}

        valid_answer = self.suggested_answer_ids.filtered(
            lambda suggested_answer: suggested_answer.id == answer_id
        )

        if not valid_answer:
            return {self.id: _("The selected value is not allowed.")}

        return {}

    def action_refresh_model_select_answers(self):
        for question in self:
            question._refresh_model_select_answers()
        return True

    def _get_model_select_domain(self):
        self.ensure_one()

        domain_text = self.model_select_domain or "[]"

        try:
            domain = ast.literal_eval(domain_text)
        except Exception as error:
            raise ValidationError(_("Invalid condition domain: %s") % error) from error

        try:
            expression.normalize_domain(domain)
        except Exception as error:
            raise ValidationError(_("Invalid condition domain: %s") % error) from error

        return domain

    def _get_model_select_source_records(self):
        self.ensure_one()

        if not self.model_select_model_id:
            return self.env["ir.model"].browse()

        model_name = self.model_select_model_id.model
        domain = self._get_model_select_domain()
        limit = self.model_select_limit or 200

        return (
            self.env[model_name]
            .sudo()
            .search(
                domain,
                limit=limit,
                order="display_name asc",
            )
        )

    def _refresh_model_select_answers(self):
        self.ensure_one()

        if self.question_type != "model_select":
            return

        if not self.model_select_model_id:
            raise ValidationError(_("Please select a dropdown model first."))

        source_records = self._get_model_select_source_records()

        existing_by_key = {
            (answer.model_select_res_model, answer.model_select_res_id): answer
            for answer in self.suggested_answer_ids
            if answer.model_select_res_model and answer.model_select_res_id
        }

        sequence = 10

        for record in source_records:
            key = (record._name, record.id)
            existing_answer = existing_by_key.get(key)

            vals = {
                "question_id": self.id,
                "sequence": sequence,
                "value": record.display_name,
                "model_select_res_model": record._name,
                "model_select_res_id": record.id,
            }

            if existing_answer:
                existing_answer.write(vals)
            else:
                self.env["survey.question.answer"].create(vals)

            sequence += 10
