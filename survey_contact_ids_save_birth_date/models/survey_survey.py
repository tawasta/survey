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


class Survey(models.Model):
    # 1. Private attributes
    _inherit = "survey.survey"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def _create_answer(
        self,
        user=False,
        partner=False,
        email=False,
        test_entry=False,
        check_attempts=True,
        **additional_vals
    ):
        """Saves partner birth date from answer"""
        res = super(Survey, self)._create_answer(
            user, partner, email, test_entry, check_attempts, **additional_vals
        )
        for question in self.mapped("question_ids").filtered(
            lambda q: q.question_type == "date" and (q.save_as_partner_birth_date)
        ):
            for user_input in res:
                if (
                    question.save_as_partner_birth_date
                    and user_input.partner_birth_date
                ):
                    user_input.save_lines(question, user_input.partner_birth_date)
        return res

    # 8. Business methods
