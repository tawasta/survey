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


class SurveyUserInput(models.Model):
    # 1. Private attributes
    _name = "survey.user_input"
    _inherit = ["mail.thread", "survey.user_input", "mail.activity.mixin"]

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def action_message_user_input(self):
        self.ensure_one()
        template = self.env.ref(
            "survey_mailing.survey_mailing_template_mail_attendees",
            raise_if_not_found=False,
        )
        local_context = dict(
            self.env.context,
            default_event_id=self.id,
            default_template_id=template and template.id or False,
        )
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "survey.mailling.wizard",
            "target": "new",
            "context": local_context,
        }

    # 8. Business methods
