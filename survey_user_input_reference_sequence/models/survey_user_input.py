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


class SurveyUserInput(models.Model):
    # 1. Private attributes
    _inherit = "survey.user_input"

    # 2. Fields declaration
    ref = fields.Char(string="Reference", index=True, readonly=True)

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods
    @api.model
    def create(self, vals):
        if not vals.get("ref"):
            vals["ref"] = self._get_next_ref(vals=vals)
        return super(SurveyUserInput, self).create(vals)

    def copy(self, default=None):
        default = default or {}
        default["ref"] = self._get_next_ref()
        return super(SurveyUserInput, self).copy(default=default)

    def write(self, vals):
        for user_input in self:
            user_input_vals = vals.copy()
            if not user_input_vals.get("ref") and not user_input.ref:
                user_input_vals["ref"] = user_input._get_next_ref(vals=user_input_vals)
            super(SurveyUserInput, user_input).write(user_input_vals)
        return True

    # 7. Action methods
    def _get_next_ref(self, vals=None):
        return self.env["ir.sequence"].next_by_code("survey.user_input")

    # 8. Business methods
