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
    company_name = fields.Char(readonly=True)
    company_street = fields.Char(readonly=True)
    company_zip = fields.Char(readonly=True)
    company_city = fields.Char(readonly=True)
    company_website = fields.Char(readonly=True)
    partner_company_id = fields.Many2one(
        string="Partner's Company", related="partner_id.parent_id"
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def _create_new_company(self, vals_list):
        """Create a new company

        This function creates a new contact for survey answer from dictionary of values.
        :param Dictionary vals_list: Values to create a new contact
        :returns: res.partner company: Created company
        """
        company = self.env["res.partner"].sudo().create(vals_list)
        _logger.debug("Created a new company %s." % company)
        return company

    def _save_company_contact(self, contact):
        if (
            self.partner_company_id
            and contact not in self.partner_company_id.contact_ids
        ):
            self.partner_company_id.write({"contact_ids": [(4, contact.id, 0)]})
            _logger.debug(
                "Added a new partner %s for partner company %s."
                % (contact, self.partner_company_id)
            )
        else:
            self._create_new_company(
                {
                    "name": "null",
                    "type": "invoice",
                    "company_type": "company",
                    "contact_ids": [
                        (4, self.partner_id.id, 0),
                        (4, contact.id, 0),
                    ],
                }
            )

    def _save_contact_field(self, question, answer, field):
        """overried original function from survey_contact_ids"""
        contacts = self.contact_ids.filtered(
            lambda r: r.survey_contact_number == question.contact_number
        )
        if contacts:
            for contact in contacts:
                contact.write({field: answer})
                _logger.debug(
                    "Wrote new partner %s %s for contact %s." % (field, answer, contact)
                )
                self._save_company_contact(contact)
        else:
            contact = self._create_new_contact(
                {
                    field: answer,
                    "survey_contact_number": question.contact_number,
                    "type": "invoice",
                    "company_type": "person",
                }
            )
            self._save_company_contact(contact)

    def _save_company_field(self, answer, field):
        if self.partner_company_id:
            self.partner_company_id.write({field: answer})
            _logger.debug(
                "Wrote new company %s %s for partner company %s."
                % (field, answer, self.partner_company_id)
            )
        else:
            self._create_new_company(
                {
                    field: answer,
                    "type": "invoice",
                    "company_type": "company",
                    "contact_ids": [(4, self.partner_id.id, 0)]
                    + [(4, contact.id, 0) for contact in self.contact_ids],
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
            and question.save_as_company_name
            and answer
        ):
            self.write({"company_name": answer})
            self._save_company_field(answer, "name")
        if (
            question.question_type == "char_box"
            and question.save_as_company_street
            and answer
        ):
            self.write({"company_street": answer})
            self._save_company_field(answer, "street")
        if (
            question.question_type == "char_box"
            and question.save_as_company_zip
            and answer
        ):
            self.write({"company_zip": answer})
            self._save_company_field(answer, "zip")
        if (
            question.question_type == "char_box"
            and question.save_as_company_city
            and answer
        ):
            self.write({"company_city": answer})
            self._save_company_field(answer, "city")
        if (
            question.question_type == "char_box"
            and question.save_as_company_website
            and answer
        ):
            self.write({"company_website": answer})
            self._save_company_field(answer, "website")
        return res

    # 8. Business methods
