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
            if self.partner_company_id:
                self.partner_company_id.write({"name": answer})
                _logger.debug(
                    "Wrote new company name %s for partner company %s."
                    % (answer, self.partner_company_id)
                )
            else:
                company = self.env["res.partner"].create(
                    {
                        "name": answer,
                        "type": "invoice",
                        "company_type": "company",
                        "contact_ids": (4, self.partner_id.id, 0),
                    }
                )
                _logger.debug("Created a new company %s." % company)
        if (
            question.question_type == "char_box"
            and question.save_as_company_street
            and answer
        ):
            self.write({"company_street": answer})
            if self.partner_company_id:
                self.partner_company_id.write({"street": answer})
                _logger.debug(
                    "Wrote a new street %s for partner company %s."
                    % (answer, self.partner_company_id)
                )
            else:
                company = self.env["res.partner"].create(
                    {
                        "name": "null",
                        "street": answer,
                        "type": "invoice",
                        "company_type": "company",
                        "contact_ids": (4, self.partner_id.id, 0),
                    }
                )
                _logger.debug("Created a new company %s." % company)
        if (
            question.question_type == "char_box"
            and question.save_as_company_zip
            and answer
        ):
            self.write({"company_zip": answer})
            if self.partner_company_id:
                self.partner_company_id.write({"zip": answer})
                _logger.debug(
                    "Wrote a new zip %s for partner company %s."
                    % (answer, self.partner_company_id)
                )
            else:
                company = self.env["res.partner"].create(
                    {
                        "name": "null",
                        "zip": answer,
                        "type": "invoice",
                        "company_type": "company",
                        "contact_ids": (4, self.partner_id.id, 0),
                    }
                )
                _logger.debug("Created a new company %s." % company)
        if (
            question.question_type == "char_box"
            and question.save_as_company_city
            and answer
        ):
            self.write({"company_city": answer})
            if self.partner_company_id:
                self.partner_company_id.write({"city": answer})
                _logger.debug(
                    "Wrote a new city %s for partner company %s."
                    % (answer, self.partner_company_id)
                )
            else:
                company = self.env["res.partner"].create(
                    {
                        "name": "null",
                        "city": answer,
                        "type": "invoice",
                        "company_type": "company",
                        "contact_ids": (4, self.partner_id.id, 0),
                    }
                )
                _logger.debug("Created a new company %s." % company)
        if (
            question.question_type == "char_box"
            and question.save_as_company_website
            and answer
        ):
            self.write({"company_website": answer})
            if self.partner_company_id:
                self.partner_company_id.write({"website": answer})
                _logger.debug(
                    "Wrote a new website %s for partner company %s."
                    % (answer, self.partner_company_id)
                )
            else:
                company = self.env["res.partner"].create(
                    {
                        "name": "null",
                        "website": answer,
                        "type": "invoice",
                        "company_type": "company",
                        "contact_ids": (4, self.partner_id.id, 0),
                    }
                )
                _logger.debug("Created a new company %s." % company)
        return res

    # 8. Business methods
