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
from odoo.http import request

# 4. Imports from Odoo modules:
from odoo.addons.survey_portal.controllers.portal import PortalSurveyAnswers

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class PortalSurveyAnswersContacts(PortalSurveyAnswers):
    def _get_survey_answers_domain(self):
        return [
            ("contact_ids", "in", request.env.user.partner_id.id),
            ("test_entry", "!=", True),
        ]
