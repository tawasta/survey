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
from odoo import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SurveyQuestion(models.Model):
    # 1. Private attributes
    _inherit = "survey.question"

    # 2. Fields declaration
    save_as_partner_birth_date = fields.Boolean(
        compute="_compute_save_as_partner_birth_date",
        readonly=False,
        store=True,
        copy=True,
        help="If checked, this option will save the user's answer as its partner "
        "birth date.",
    )

    save_as_contact_birth_date = fields.Boolean(
        compute="_compute_save_as_contact_birth_date",
        readonly=False,
        store=True,
        copy=True,
        help="If checked, this option will save the user's answer as its contact "
        "birth date.",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.depends("question_type")
    def _compute_save_as_contact_birth_date(self):
        for question in self:
            if question.question_type != "date":
                question.save_as_contact_birth_date = False

    @api.depends("question_type")
    def _compute_save_as_partner_birth_date(self):
        for question in self:
            if question.question_type != "date":
                question.save_as_partner_birth_date = False

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
