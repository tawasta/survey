##############################################################################
#
#    Author: Futural Oy
#    Copyright 2022- Futural Oy (https://futural.fi)
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

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SurveyUserInput(models.Model):
    # 1. Private attributes
    _inherit = "survey.user_input"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def _save_lines(self, question, answer, comment=None, overwrite_existing=True):
        """Save answers to questions, depending on question type
        If an answer already exists for question and user_input_id, it will be
        overwritten (or deleted for 'choice' questions) (in order to maintain data consistency).
        """
        if question.question_type == "privacy":
            old_answers = self.env["survey.user_input.line"].search(
                [("user_input_id", "=", self.id), ("question_id", "=", question.id)]
            )
            self._save_line_privacy(question, old_answers, answer, comment)
        else:
            return super(SurveyUserInput, self)._save_lines(
                question, answer, comment, overwrite_existing
            )

    def _save_line_privacy(self, question, old_answers, answer, comment):
        vals = {
            "user_input_id": self.id,
            "question_id": question.id,
            "answer_type": question.question_type,
            "skipped": True,
        }
        if answer:
            vals.update({"skipped": False})
            privacy_activity_id, partner_id = answer.split("-", 1)
            privacy_values = {
                "partner_id": int(partner_id),
                "activity_id": int(privacy_activity_id),
                "accepted": True,
                "state": "answered",
            }
            already_privacy_record = (
                self.env["privacy.consent"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", int(partner_id)),
                        ("activity_id", "=", int(privacy_activity_id)),
                    ]
                )
            )
            if already_privacy_record:
                vals.update({"value_privacy_consent": already_privacy_record.id})
                already_privacy_record.sudo().write({"accepted": True})
            else:
                new_privacy_record = (
                    self.env["privacy.consent"].sudo().create(privacy_values)
                )
                vals.update({"value_privacy_consent": new_privacy_record.id})
        if old_answers:
            old_answers.write(vals)
            return old_answers
        else:
            return self.env["survey.user_input.line"].create(vals)

    # 8. Business methods


class SurveyUserInputLine(models.Model):
    # 1. Private attributes
    _inherit = "survey.user_input.line"

    # 2. Fields declaration
    answer_type = fields.Selection(selection_add=[("privacy", "Privacy")])
    value_privacy_consent = fields.Many2one("privacy.consent")

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.depends(
        "answer_type",
        "value_char_box",
        "value_numerical_box",
        "value_date",
        "value_datetime",
        "value_text_box",
        "value_privacy_consent",
        "suggested_answer_id",
        "matrix_row_id",
    )
    def _compute_string_answer(self):
        res = super(SurveyUserInputLine, self)._compute_string_answer()
        for line in self:
            if line.answer_type == "privacy" and line.value_privacy_consent:
                line.string_answer = line.value_privacy_consent.activity_id.name
        return res

    # 5. Constraints and onchanges
    @api.constrains("skipped", "answer_type")
    def _check_answer_type_skipped(self):
        for line in self:
            if line.answer_type != "privacy":
                return super(SurveyUserInputLine, line)._check_answer_type_skipped()

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
