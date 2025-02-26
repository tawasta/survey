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
from odoo import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SurveyQuestion(models.Model):
    # 1. Private attributes
    _inherit = "survey.question"

    # 2. Fields declaration
    question_type = fields.Selection(selection_add=[("privacy", "Privacy")])
    privacy_activity_id = fields.Many2one("privacy.activity", string="Privacy Activity")

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def validate_question(self, answer, comment=None):
        if self.constr_mandatory and self.question_type == "privacy":
            if not answer:
                return {self.id: self.constr_error_msg}
            return {}
        return super(SurveyQuestion, self).validate_question(answer, comment)

    # 8. Business methods
