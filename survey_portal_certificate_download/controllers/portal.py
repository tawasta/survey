##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2025- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
from odoo.addons.survey.controllers.main import Survey
from odoo.addons.survey_portal.controllers.portal import PortalSurveyAnswers

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class PortalSurveyCertificate(PortalSurveyAnswers, Survey):
    def _can_download_certification(self, answer):
        """Whether the portal user may download the certificate of an answer"""
        survey = answer.survey_id
        return bool(
            survey.certification
            and survey.certification_downloadable_in_portal
            and answer.scoring_success
        )

    @http.route(
        ["/my/surveys/<int:user_input_id>/certification"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_survey_certification(self, user_input_id, **kw):
        domain = self._get_survey_answers_domain() + [("id", "=", user_input_id)]
        answer_sudo = request.env["survey.user_input"].sudo().search(domain, limit=1)
        if not answer_sudo or not self._can_download_certification(answer_sudo):
            return request.redirect("/my/surveys")
        # Renders survey.certification_report, which picks the styling from
        # the survey's certification_report_layout
        return self._generate_report(answer_sudo, download=True)
