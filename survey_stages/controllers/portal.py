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
from odoo import http
from odoo.http import request

# 4. Imports from Odoo modules:
from odoo.addons.survey_contact_ids.controllers.portal import (
    PortalSurveyAnswersContacts,
)

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class PortalSurveyAnswersStages(PortalSurveyAnswersContacts):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "survey_answer_count" in counters:
            survey_answer_count = (
                request.env["survey.user_input"]
                .sudo()
                .search_count(
                    [
                        ("contact_ids", "in", request.env.user.partner_id.id),
                        ("test_entry", "!=", True),
                        ("is_hidden", "!=", True),
                    ]
                )
            )
            values["survey_answer_count"] = survey_answer_count or 0
        return values

    @http.route(["/my/surveys"], type="http", auth="user", website=True)
    def portal_my_surveys(self, **kw):
        values = self._prepare_portal_layout_values()
        survey_answers = (
            request.env["survey.user_input"]
            .sudo()
            .search(
                [
                    ("contact_ids", "in", request.env.user.partner_id.id),
                    ("test_entry", "!=", True),
                    ("is_hidden", "!=", True),
                ]
            )
        )
        values.update(
            {
                "survey_answers": survey_answers,
                "page_name": "survey_answer",
                "default_url": "/my/surveys",
            }
        )
        return request.render("survey_stages.portal_my_survey_answers_stages", values)
