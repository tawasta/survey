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
import math

# 2. Known third party imports:
# 3. Odoo imports (openerp):
from odoo import _, models
from odoo.tools import format_date, format_datetime

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SurveyUserInputXlsx(models.AbstractModel):
    # 1. Private attributes
    _inherit = "report.survey_user_input_report_xlsx.user_input_report_xlsx"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
    def _get_row_question_scores(self, column_questions, user_input):
        """Traverse through each question in column questions and returns a list
        of row question answer scores"""
        row_questions = []
        for column_question in column_questions:
            column_answer = []
            for user_input_line in user_input.user_input_line_ids:
                if column_question == user_input_line.question_id:
                    column_answer.append(user_input_line.answer_score)
            row_questions.append(math.fsum(column_answer))
        return row_questions

    def _write_scored_answers(self, workbook, sheet, question, row):
        """Write a questions title, answer, and score on sheet. Returns the next empty row."""
        col = 0
        sheet.write(row, col, question.title, workbook.add_format({"bold": True}))
        col += 1
        sheet.write(row, col, _("Answer"), workbook.add_format({"bold": True}))
        col += 1
        sheet.write(row, col, _("Score"), workbook.add_format({"bold": True}))
        row += 1
        # simple choice / multiple choice / matrix
        if question.suggested_answer_ids:
            for suggested_answer_id in question.suggested_answer_ids:
                col = 1
                sheet.write(row, col, suggested_answer_id.value)
                col += 1
                sheet.write(row, col, suggested_answer_id.answer_score)
                row += 1
        # date / datetime / other unknown type
        else:
            if question.question_type == "date":
                col = 1
                sheet.write(
                    row,
                    col,
                    str(format_date(self.env, question.answer_date)),
                )
                col += 1
                sheet.write(row, col, question.answer_score)
                row += 1
            if question.question_type == "datetime":
                col = 1
                sheet.write(
                    row,
                    col,
                    str(format_datetime(self.env, question.answer_datetime)),
                )
                col += 1
                sheet.write(row, col, question.answer_score)
                row += 1
        return row

    def generate_xlsx_report(self, workbook, data, survey_user_inputs):
        res = super(SurveyUserInputXlsx, self).generate_xlsx_report(
            workbook, data, survey_user_inputs
        )
        row = 0
        col = 0

        # New sheet for score answers
        sheet = workbook.add_worksheet(_("Survey Answer Scores"))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        column_fields = self._get_column_fields()
        column_questions = self._get_column_questions(survey_user_inputs)

        # Write column titles first
        for column_field in column_fields:
            sheet.write(row, col, column_field, workbook.add_format({"bold": True}))
            col += 1
        for column_question in column_questions:
            sheet.write(
                row, col, column_question.title, workbook.add_format({"bold": True})
            )
            col += 1
        row += 1
        col = 0

        # Write a row for each user input
        for user_input in survey_user_inputs:
            row_fields = self._get_row_fields(user_input)
            row_questions = self._get_row_question_scores(column_questions, user_input)
            for row_field in row_fields:
                sheet.write(row, col, row_field)
                col += 1
            for row_question in row_questions:
                sheet.write(row, col, row_question)
                col += 1
            row += 1
            col = 0
        # Padding after answer rows
        row += 3

        # Scored answers table at the end of sheet
        scored_questions = column_questions.filtered(
            lambda s: s.is_scored_question
            or (
                s.question_type == "matrix"
                and any(
                    question_answer.answer_score
                    for question_answer in s.suggested_answer_ids
                )
            )
        )
        for question in scored_questions:
            row = self._write_scored_answers(workbook, sheet, question, row)
        return res
