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

from odoo import api, fields, models
from odoo.tools import format_date, format_datetime


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    string_answer = fields.Char(
        string="Answer", readonly=True, store=True, compute="_compute_string_answer"
    )

    @api.depends(
        "answer_type",
        "value_char_box",
        "value_numerical_box",
        "value_date",
        "value_datetime",
        "value_text_box",
        "suggested_answer_id",
        "matrix_row_id",
    )
    def _compute_string_answer(self):
        for line in self:
            if line.answer_type == "char_box" and line.value_char_box:
                line.string_answer = line.value_char_box
            if line.answer_type == "text_box" and line.value_text_box:
                line.string_answer = str(line.value_text_box)
            if line.answer_type == "numerical_box" and line.value_numerical_box:
                line.string_answer = str(line.value_numerical_box)
            if line.answer_type == "date" and line.value_date:
                line.string_answer = str(format_date(self.env, line.value_date))
            if line.answer_type == "datetime" and line.value_datetime:
                line.string_answer = str(format_datetime(self.env, line.value_datetime))
            if line.answer_type == "suggestion" and line.suggested_answer_id:
                line.string_answer = str(line.suggested_answer_id.value)
