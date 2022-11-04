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
import logging

# 3. Odoo imports (openerp):
from odoo import api, fields, models

# 2. Known third party imports:


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    # 1. Private attributes
    _inherit = "survey.user_input"

    # 2. Fields declaration
    contact_ids = fields.Many2many(
        "res.partner", string="Contact Persons", tracking=True
    )
    invite_ids = fields.One2many(
        comodel_name="survey.user.invite",
        inverse_name="survey_user_input_id",
        string="Invites",
        help="Invites for other users to participate on this survey",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods
    @api.model
    def create(self, vals):
        if vals.get("partner_id"):
            vals["contact_ids"] = [(4, vals.get("partner_id"), 0)]
        return super(SurveyUserInput, self).create(vals)

    # 7. Action methods
    def _create_new_contact(self, vals_list):
        """Create a new contact

        This function creates a new contact for survey answer from dictionary of values.
        :param Dictionary vals_list: Values to create a new contact
        :returns: res.partner: Newly created partner
        """
        contact = self.env["res.partner"].sudo().create(vals_list)
        self.write({"contact_ids": [(4, contact.id, 0)]})
        _logger.debug("Created a new contact %s." % contact)
        return contact

    def _save_contact_field(self, question, answer, field):
        contacts = self.contact_ids.filtered(
            lambda r: r.survey_contact_number == question.contact_number
        )
        if contacts:
            for contact in contacts:
                contact.write({field: answer})
                _logger.debug(
                    "Wrote new partner %s %s for contact %s." % (field, answer, contact)
                )
        else:
            self._create_new_contact(
                {
                    field: answer,
                    "survey_contact_number": question.contact_number,
                    "type": "invoice",
                    "company_type": "person",
                }
            )

    def save_lines(self, question, answer, comment=None):
        """Save answers to questions, depending on question type
        If an answer already exists for question and user_input_id, it will be
        overwritten (or deleted for 'choice' questions) (in order to maintain data consistency).
        """
        res = super(SurveyUserInput, self).save_lines(question, answer, comment)
        if (
            question.question_type == "char_box"
            and question.save_as_contact_name
            and answer
        ):
            self._save_contact_field(question, answer, "name")
        if (
            question.question_type == "char_box"
            and question.save_as_contact_phone
            and answer
        ):
            self._save_contact_field(question, answer, "phone")
        if (
            question.question_type == "char_box"
            and question.save_as_contact_email
            and answer
        ):
            self._save_contact_field(question, answer, "email")
        return res

    # 8. Business methods
