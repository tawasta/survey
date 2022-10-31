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
from uuid import uuid4

# 3. Odoo imports (openerp):
from odoo import _, api, fields, models

# 2. Known third party imports:


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SurveyUserInvite(models.Model):

    # 1. Private attributes
    _name = "survey.user.invite"
    _description = "Unique invites to survey"
    _rec_name = "email"
    _order = "id DESC"
    _sql_constraints = [
        (
            "code_unique",
            "unique(code)",
            _("Code has to be unique for every invite!"),
        )
    ]

    # 2. Fields declaration
    survey_user_input_id = fields.Many2one(
        comodel_name="survey.user_input",
        string="Survey answer",
        help="Survey answer this invite belongs to",
        required=True,
    )
    code = fields.Char(
        string="Code",
        help="Unique invite code for intitee",
        default=lambda self: uuid4(),
        required=True,
    )
    email = fields.Char(
        string="Email",
        help="Where was invite sent",
        required=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Used by",
        help="User who accepted the invitation",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods
    @api.model
    def create(self, vals):
        """Send email to receiver"""
        res = super().create(vals)
        template_id = self.env.ref(
            "survey_contact_ids.mail_template_survey_invite",
            raise_if_not_found=False,
        ).id
        email_values = {
            "email_from": self.env.ref("base.main_company").email_formatted,
        }
        self.env["mail.template"].browse(template_id).sudo().send_mail(
            res.id, email_values=email_values, force_send=True
        )
        return res

    # 7. Action methods

    # 8. Business methods
