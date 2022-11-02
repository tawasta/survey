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

# 2. Known third party imports:
# 3. Odoo imports (openerp):
from odoo import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    # 1. Private attributes
    _inherit = "survey.user_input"

    # 2. Fields declaration
    secondary_contact_name = fields.Char(readonly=True)
    secondary_contact_phone = fields.Char(readonly=True)
    secondary_contact_email = fields.Char(readonly=True)
    secondary_contact_id = fields.Many2one("res.partner", string="Secondary Contact")

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def save_lines(self, question, answer, comment=None):
        """Save answers to questions, depending on question type
        If an answer already exists for question and user_input_id, it will be
        overwritten (or deleted for 'choice' questions) (in order to maintain data consistency).
        """
        res = super(SurveyUserInput, self).save_lines(question, answer, comment)
        if (
            question.question_type == "char_box"
            and question.save_as_secondary_contact_name
            and answer
        ):
            self.write({"secondary_contact_name": answer})
            secondary_contact = self.secondary_contact_id
            if secondary_contact:
                self.secondary_contact_id.write({"name": answer})
                _logger.debug(
                    "Wrote new partner name %s for secondary contact %s."
                    % (answer, self.secondary_contact_id)
                )
            else:
                secondary_contact = self.env["res.partner"].create(
                    {"name": answer, "type": "invoice", "company_type": "person"}
                )
                self.write({"secondary_contact_id": secondary_contact.id})
                _logger.debug("Created a new contact %s." % secondary_contact)

            if self.partner_company_id:
                self.partner_company_id.write(
                    {"contact_ids": [(4, secondary_contact.id, 0)]}
                )
                _logger.debug(
                    "Added a new partner %s for partner company %s."
                    % (secondary_contact, self.partner_company_id)
                )
            else:
                company = self.env["res.partner"].create(
                    {
                        "name": "null",
                        "type": "invoice",
                        "company_type": "company",
                        "contact_ids": [
                            (4, self.partner_id.id, 0),
                            (4, secondary_contact.id, 0),
                        ],
                    }
                )
                _logger.debug("Created a new company %s." % company)
        if (
            question.question_type == "char_box"
            and question.save_as_secondary_contact_phone
            and answer
        ):
            self.write({"secondary_contact_phone": answer})
            secondary_contact = self.secondary_contact_id
            if secondary_contact:
                self.secondary_contact_id.write({"phone": answer})
                _logger.debug(
                    "Wrote new partner phone %s for secondary contact %s."
                    % (answer, self.secondary_contact_id)
                )
            else:
                secondary_contact = self.env["res.partner"].create(
                    {
                        "name": "null",
                        "phone": answer,
                        "type": "invoice",
                        "company_type": "person",
                    }
                )
                self.write({"secondary_contact_id": secondary_contact.id})
                _logger.debug("Created a new contact %s." % secondary_contact)

            if self.partner_company_id:
                self.partner_company_id.write(
                    {"contact_ids": [(4, secondary_contact.id, 0)]}
                )
                _logger.debug(
                    "Added a new partner %s for partner company %s."
                    % (secondary_contact, self.partner_company_id)
                )
            else:
                company = self.env["res.partner"].create(
                    {
                        "name": "null",
                        "type": "invoice",
                        "company_type": "company",
                        "contact_ids": [
                            (4, self.partner_id.id, 0),
                            (4, secondary_contact.id, 0),
                        ],
                    }
                )
                _logger.debug("Created a new company %s." % company)
        if (
            question.question_type == "char_box"
            and question.save_as_secondary_contact_email
            and answer
        ):
            self.write({"secondary_contact_email": answer})
            secondary_contact = self.secondary_contact_id
            if secondary_contact:
                self.secondary_contact_id.write({"email": answer})
                _logger.debug(
                    "Wrote new partner email %s for secondary contact %s."
                    % (answer, self.secondary_contact_id)
                )
            else:
                secondary_contact = self.env["res.partner"].create(
                    {
                        "name": "null",
                        "email": answer,
                        "type": "invoice",
                        "company_type": "person",
                    }
                )
                self.write({"secondary_contact_id": secondary_contact.id})
                _logger.debug("Created a new contact %s." % secondary_contact)

            if self.partner_company_id:
                self.partner_company_id.write(
                    {"contact_ids": [(4, secondary_contact.id, 0)]}
                )
                _logger.debug(
                    "Added a new partner %s for partner company %s."
                    % (secondary_contact, self.partner_company_id)
                )
            else:
                company = self.env["res.partner"].create(
                    {
                        "name": "null",
                        "type": "invoice",
                        "company_type": "company",
                        "contact_ids": [
                            (4, self.partner_id.id, 0),
                        ],
                    }
                )
                _logger.debug("Created a new company %s." % company)
        return res

    # 8. Business methods
