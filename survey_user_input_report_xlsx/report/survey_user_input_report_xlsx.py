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

import logging
from datetime import datetime

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SurveyUserInputXlsx(models.AbstractModel):
    _name = "report.survey_user_input_report_xlsx.user_input_report_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Survey User Input Report XLSX"

    def _get_user_input_fnames(self):
        """Returns a dictionary of static fields for report with title and field name"""
        user_input_fnames = {
            self.env._("Survey"): "survey_id",
            self.env._("Partner"): "partner_id",
            self.env._("Created on"): "create_date",
        }
        return user_input_fnames

    def _get_user_input_fname_value(self, user_input, fname):
        """Returns a string value for a corresponding field"""
        value = ""
        if fname == "survey_id":
            value = user_input.survey_id.display_name or ""
        if fname == "partner_id":
            value = user_input.partner_id.name or ""
        if fname == "create_date":
            value = (
                datetime.strftime(
                    fields.Datetime.context_timestamp(self, user_input.create_date),
                    "%-d.%-m.%-Y %-H.%M",
                )
                or ""
            )
        return value

    def generate_xlsx_report(self, workbook, data, survey_user_inputs):
        row = 0
        col = 0
        # Create a sheet and apply formatting
        sheet = workbook.add_worksheet(self.env._("Survey Answers"))
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
                            answer_list = []
                            for user_input_line in user_input.user_input_line_ids:
                                if (
                                    user_input_line.question_id == question
                                    and user_input_line.matrix_row_id == matrix_row
                                ):
                                    answer_list.append(
                                        user_input_line.string_answer or ""
                                    )
                            sheet.write(row, col, ", ".join(answer_list))
                            col += 1
                    else:
                        answer_list = []
                        for user_input_line in user_input.user_input_line_ids:
                            if user_input_line.question_id == question:
                                answer_list.append(user_input_line.string_answer or "")
                        sheet.write(row, col, ", ".join(answer_list))
                        col += 1
            row += 1
            col = 0
