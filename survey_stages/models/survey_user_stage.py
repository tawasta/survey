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
from odoo import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SurveyUserInputStage(models.Model):
    # 1. Private attributes
    _name = "survey.user_input.stage"
    _description = "Participation Stage"
    _order = "sequence, id"

    # 2. Fields declaration
    name = fields.Char(string="Stage Name", required=True, translate=True)
    description = fields.Text(string="Stage description", translate=True)
    sequence = fields.Integer(default=1)
    color = fields.Integer()

    mail_template_id = fields.Many2one(
        "mail.template",
        string="Email Template",
        domain=[("model", "=", "survey.user_input")],
        help="If set an email will be sent to the answer followers when the answer "
        "reaches this step.",
    )
    is_sent = fields.Boolean("Sent Stage", help="Answers in this stage are sent.")
    is_accepted = fields.Boolean(
        string="Accepted Stage", help="Answers in this stage are accepted."
    )
    is_cancel = fields.Boolean(
        string="Canceled Stage", help="Answers in this stage are canceled."
    )
    is_editable = fields.Boolean(
        string="Allow Answer Edit", help="Answers in this stage can be edited."
    )
    is_hidden = fields.Boolean(
        string="Hidden stage", help="Answers in this stage will be hidden."
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
