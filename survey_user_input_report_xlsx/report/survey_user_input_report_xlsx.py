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

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SurveyUserInputXlsx(models.AbstractModel):
    # 1. Private attributes
    _name = "report.survey_user_input_report_xlsx.user_input_report_xlsx"
    _inherit = "report.report_xlsx.abstract"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
    def _get_questions(self, survey_user_inputs):
        questions = self.env["survey.question"]
        for user_input in survey_user_inputs:
            for user_input_line in user_input.user_input_line_ids:
                if user_input_line.question_id not in questions:
                    questions += user_input_line.question_id
        print("@@@@@@@@@@@@@@@@@@@@")
        print("@@@@@@@@@@@@@@@@@@@@")
        print("@@@@@@@@@@@@@@@@@@@@")
        print("@@@@@@@@@@@@@@@@@@@@")
        print(questions)
        return questions

    def _get_fields_to_print(self, user_input):
        """Returns a dictionary where key is the xlsx column title and
        value is the column value."""
        fields_to_print = {
            "Survey": user_input.survey_id.title,
            "Partner": user_input.partner_id.name,
            "Created on": user_input.create_date,
        }
        # for input_line in user_input.user_input_line_ids:
        #     fields_to_print[input_line.question_id.title] = input_line.string_answer
        return fields_to_print

    def generate_xlsx_report(self, workbook, data, survey_user_inputs):
        row = 0
        col = 0
        sheet = workbook.add_worksheet("Survey Answers")
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        questions = self._get_questions(survey_user_inputs)
        for user_input in survey_user_inputs:
            fields_to_print = self._get_fields_to_print(user_input)
            if row == 0:
                for field_to_print in fields_to_print:
                    sheet.write(
                        row, col, field_to_print, workbook.add_format({"bold": True})
                    )
                    col += 1
                for question in questions:
                    sheet.write(
                        row, col, question.title, workbook.add_format({"bold": True})
                    )
                    col += 1
                col = 0
                row += 1
            for field_to_print in fields_to_print:
                sheet.write(row, col, fields_to_print[field_to_print])
                col += 1
            matrix_answer = []
            for user_input_line in user_input.user_input_line_ids:
                if user_input_line.question_id in questions:
                    if user_input_line.question_id.question_type == "matrix":
                        matrix_answer.append(user_input_line.string_answer)
                    else:
                        sheet.write(row, col, user_input_line.string_answer)
                col += 1
            col = 0
            row += 1
