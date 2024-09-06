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

GENDER_OPTS = {
    "m": ["male", "man", "boy", "mies", "poika", "miespuolinen"],
    "f": ["female", "woman", "girl", "nainen", "naispuolinen", "tyttö"],
    "o": ["other", "muu"],
}


class SurveyUserInput(models.Model):
    # 1. Private attributes
    _inherit = "survey.user_input"

    # 2. Fields declaration
    partner_gender = fields.Selection(
        [("m", "Male"), ("f", "Female"), ("o", "Other")], string="Partner's Gender"
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def _get_partner_gender(self, answer_id):
        answer_value = (
            self.env["survey.question.answer"]
            .sudo()
            .search([("id", "=", answer_id)], limit=1)
            .value
        )
        if answer_value:
            # Question answers can be anything so we need to hard-code some string comparisons.
            # If no match is found don't save gender. (But still save the answer)
            for gender_opt, gender in GENDER_OPTS.items():
                if answer_value.casefold() in gender:
                    return gender_opt
            _logger.warning(
                "Gender %s answer does not match known gender options in %s. "
                % (answer_value.casefold(), GENDER_OPTS)
            )
        return False

    def _save_partner_gender(self, gender):
        """Saves gender to partner"""
        self.write({"partner_gender": gender})

        # Map gender with OCA's gender selection on partner
        gender_map = {"m": "male", "f": "female", "o": "other"}
        gender = gender_map.get(gender) or gender

        self.partner_id.write({"gender": gender})
        _logger.debug("Partner's %s gender saved." % self.partner_id)

    def save_lines(self, question, answer, comment=None):
        """Save answers to questions, depending on question type
        If an answer already exists for question and user_input_id, it will be
        overwritten (or deleted for 'choice' questions) (in order to maintain data consistency).
        """
        res = super(SurveyUserInput, self).save_lines(question, answer, comment)
        if (
            question.question_type == "simple_choice"
            and question.save_as_partner_gender
            and answer
            and not question.comment_count_as_answer
        ):
            gender_opt = self._get_partner_gender(answer)
            if gender_opt:
                self._save_partner_gender(gender_opt)
        if (
            question.question_type == "simple_choice"
            and question.save_as_contact_gender
            and answer
            and not question.comment_count_as_answer
        ):
            gender_opt = self._get_partner_gender(answer)

            gender_map = {"m": "male", "f": "female", "o": "other"}
            gender_opt = gender_map.get(gender_opt) or gender_opt

            if gender_opt:
                self._save_contact_field(question, gender_opt, "gender")
        return res

    # 8. Business methods
