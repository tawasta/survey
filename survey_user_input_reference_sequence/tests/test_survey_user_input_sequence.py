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
import odoo.tests.common as common
from odoo.tests import tagged

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


@tagged("standard", "at_install", "sequence")
class TestSurveyUserInputSequence(common.TransactionCase):
    def setUp(self):
        super(TestSurveyUserInputSequence, self).setUp()

        self.res_partner = self.env["res.partner"]
        self.partner = self.res_partner.create(
            {"name": "test1", "email": "test@test.com"}
        )
        self.survey_survey = self.env["survey.survey"]
        self.survey_user_input = self.env["survey.user_input"]
        self.survey = self.survey_survey.create({"title": "test1"})
        self.user_input = self.survey_user_input.create(
            {"survey_id": self.survey.id, "partner_id": self.partner.id}
        )

    def test_ref_sequence_on_user_input(self):
        """Test sequence on creating user input and copying it"""
        self.assertTrue(self.user_input.ref, "A user input always has a ref.")

        copy = self.partner.copy()
        self.assertTrue(
            copy.ref, "A user input with ref created by copy has a ref by default."
        )

    def test_unique_ref_on_write(self):
        """Assert that on create or on write, a different ref is assigned"""
        vals = [
            {"survey_id": self.survey.id, "partner_id": self.partner.id},
            {"survey_id": self.survey.id, "partner_id": self.partner.id},
        ]
        user_inputs = self.env["survey.user_input"].create(vals)
        self.assertFalse(user_inputs[0].ref == user_inputs[1].ref)
        user_inputs.write({"ref": False})
        self.assertFalse(user_inputs[0].ref)
        user_inputs.write({})
        self.assertFalse(user_inputs[0].ref == user_inputs[1].ref)
