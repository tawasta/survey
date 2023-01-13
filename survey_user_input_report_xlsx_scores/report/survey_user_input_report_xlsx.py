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

import logging

# 2. Known third party imports:
# 3. Odoo imports (openerp):
from odoo import _, models
from odoo.tools import format_date, format_datetime

# 1. Standard library imports:


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


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

    def generate_xlsx_report(self, workbook, data, survey_user_inputs):  # noqa: C901
        res = super(SurveyUserInputXlsx, self).generate_xlsx_report(
            workbook, data, survey_user_inputs
        )
        row = 0
        col = 0

        # New sheet for score answers
        sheet = workbook.add_worksheet(_("Survey Answer Scores"))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)

        user_input_fnames = self._get_user_input_fnames()
        surveys = self.env["survey.survey"].search(
            [["user_input_ids", "in", survey_user_inputs.ids]]
        )
        # Write user input field titles
        _logger.debug("Writing title columns for static fields: %s", user_input_fnames)
        for fname in user_input_fnames:
            sheet.write(row, col, fname, workbook.add_format({"bold": True}))
            col += 1
        # Write survey question titles
        for survey in surveys:
            _logger.debug(
                "Writing title columns for survey %s questions: %s",
                (survey, survey.question_ids),
            )
            for question in survey.question_ids:
                if question.question_type == "matrix":
                    for matrix_row in question.matrix_row_ids:
                        sheet.write(
                            row,
                            col,
                            matrix_row.value,
                            workbook.add_format({"bold": True}),
                        )
                        col += 1
                else:
                    sheet.write(
                        row, col, question.title, workbook.add_format({"bold": True})
                    )
                    col += 1
        row += 1
        col = 0
        # Write a row for each user input
        for user_input in survey_user_inputs:
            _logger.debug("Writing a row for user input: %s", user_input)
            # Write user input field values
            for fname in user_input_fnames:
                sheet.write(
                    row,
                    col,
                    self._get_user_input_fname_value(
                        user_input, user_input_fnames[fname]
                    ),
                )
                col += 1
            # Write each question answer
            for survey in surveys:
                for question in survey.question_ids:
                    if question.question_type == "matrix":
                        for matrix_row in question.matrix_row_ids:
                            answer_score = 0.0
                            for user_input_line in user_input.user_input_line_ids:
                                if (
                                    user_input_line.question_id == question
                                    and user_input_line.matrix_row_id == matrix_row
                                ):
                                    answer_score += user_input_line.answer_score
                            sheet.write(row, col, answer_score)
                            col += 1
                    else:
                        answer_score = 0.0
                        for user_input_line in user_input.user_input_line_ids:
                            if user_input_line.question_id == question:
                                if question.suggested_answer_ids:
                                    answer_score += user_input_line.answer_score
                        sheet.write(row, col, answer_score)
                        col += 1
            row += 1
            col = 0

        # Scored answers table at the end of sheet
        row += 3
        scored_questions = self.env["survey.question"].search(
            [
                ("survey_id", "in", surveys.ids),
                "|",
                ("is_scored_question", "=", True),
                ("question_type", "=", "matrix"),
            ]
        )
        for question in scored_questions:
            row = self._write_scored_answers(workbook, sheet, question, row)
        return res
