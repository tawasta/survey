##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:
import logging

# 2. Known third party imports:
# 3. Odoo imports (openerp):
from odoo import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    # 1. Private attributes
    _inherit = "survey.user_input"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def save_lines(self, question, answer, comment=None):
        """Save answers to questions, depending on question type
        If an answer already exists for question and user_input_id, it will be
        overwritten (or deleted for 'choice' questions) (in order to maintain data consistency).
        """
        if question.question_type == "attachment":
            old_answers = self.env["survey.user_input.line"].search(
                [("user_input_id", "=", self.id), ("question_id", "=", question.id)]
            )
            self._save_line_attachment(question, old_answers, answer, comment)
        else:
            return super(SurveyUserInput, self).save_lines(question, answer, comment)

    def _save_line_attachment(self, question, old_answers, answer, comment):
        vals = {
            "user_input_id": self.id,
            "question_id": question.id,
            "answer_type": question.question_type,
            "skipped": True,
        }
        if answer and answer.get("values") and answer.get("is_answer_update"):
            attachment_data_lines = [
                (
                    0,
                    4,
                    {
                        "name": answer_data.get("file_name"),
                        "store_fname": answer_data.get("file_name"),
                        "datas": answer_data.get("data"),
                        "description": "Survey Answer Attachment",
                        "type": "binary",
                        "res_model": "survey.user_input.line",
                    },
                )
                for answer_data in answer.get("values")
            ]
            vals.update({"value_attachment_ids": attachment_data_lines})
            vals.update({"skipped": False})
        if old_answers:
            # If answer is skipped but it wasn't skipped previously mark answer as not skipped
            if vals.get("skipped") and not old_answers.skipped:
                vals.update({"skipped": False})
            old_answers.write(vals)
            _logger.debug(
                "Old answer %s updated with values:\n%s" % (old_answers, vals)
            )
            return old_answers
        else:
            new_answer = self.env["survey.user_input.line"].create(vals)
            _logger.debug("New answer %s created with values:\n%s" % (new_answer, vals))
            return new_answer

    # 8. Business methods


class SurveyUserInputLine(models.Model):
    # 1. Private attributes
    _inherit = "survey.user_input.line"

    # 2. Fields declaration
    answer_type = fields.Selection(selection_add=[("attachment", "Attachment")])
    value_attachment_ids = fields.One2many(
        comodel_name="ir.attachment",
        inverse_name="res_id",
        string="Attachments Answer",
        domain=[("res_model", "=", "survey.user_input.line")],
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.depends(
        "answer_type",
        "value_char_box",
        "value_numerical_box",
        "value_date",
        "value_datetime",
        "value_text_box",
        "value_attachment_ids",
        "suggested_answer_id",
        "matrix_row_id",
    )
    def _compute_string_answer(self):
        res = super(SurveyUserInputLine, self)._compute_string_answer()
        for line in self:
            if line.answer_type == "attachment" and line.value_attachment_ids:
                line.string_answer = ", ".join(
                    str(attachment.name) for attachment in line.value_attachment_ids
                )
        return res

    # 5. Constraints and onchanges
    @api.constrains("skipped", "answer_type")
    def _check_answer_type_skipped(self):
        for line in self:
            if line.answer_type != "attachment":
                return super(SurveyUserInputLine, line)._check_answer_type_skipped()

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
