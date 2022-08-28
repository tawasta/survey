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
    def generate_xlsx_report(self, workbook, data, survey_user_inputs):
        row = 0
        col = 0
        sheet = workbook.add_worksheet("Survey Answers")
        for user_input in survey_user_inputs:
            sheet.write(row, col, user_input.survey_id.title)
            sheet.write(
                row,
                col + 1,
                ", ".join(partner.name for partner in user_input.contact_ids),
            )
            row += 1
