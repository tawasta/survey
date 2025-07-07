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

# 3. Odoo imports (openerp):
# 2. Known third party imports:
import logging

from odoo import http
from odoo.http import request

# 4. Imports from Odoo modules:
from odoo.addons.survey_contact_ids.controllers.main import SurveyContacts

_logger = logging.getLogger(__name__)

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SurveyStages(SurveyContacts):
    def _get_draft_stage(self, survey_sudo, answer_sudo):
        draft_stage = request.env["survey.user_input.stage"].search(
            [("is_editable", "=", True)], limit=1
        )

        return draft_stage

    def _get_sent_stage(self, survey_sudo, answer_sudo):
        sent_stage = request.env["survey.user_input.stage"].search(
            [("is_sent", "=", True)], limit=1
        )

        return sent_stage

    @http.route(
        "/survey/edit/<string:survey_token>/<string:answer_token>",
        type="http",
        auth="public",
        website=True,
    )
    def survey_edit(self, survey_token, answer_token, email=False, **post):
        """Edit survey"""
        # Get the current answer token from cookie
        answer_from_cookie = False
        if not answer_token:
            answer_token = request.httprequest.cookies.get("survey_%s" % survey_token)
            answer_from_cookie = bool(answer_token)

        access_data = self._get_access_data(
            survey_token, answer_token, ensure_token=False, check_partner=False
        )

        if answer_from_cookie and access_data["validity_code"] in (
            "answer_wrong_user",
            "token_wrong",
        ):
            # If the cookie had been generated for another user or does not correspond
            # to any existing answer object (probably because it has been deleted),
            # ignore it and redo the check. The cookie will be replaced by a legit
            # value when resolving the URL, so we don't clean it further here.
            access_data = self._get_access_data(survey_token, None, ensure_token=False)

        if access_data["validity_code"] is not True:
            return self._redirect_with_error(access_data, access_data["validity_code"])

        answer_sudo = access_data["answer_sudo"]

        if (
            answer_sudo.is_editable
            and request.env.user.partner_id in answer_sudo.contact_ids
        ):
            # Mark answer as in progress and reset last displayed page
            answer_sudo._mark_in_progress()
            answer_sudo.write({"last_displayed_page_id": False})
            # Start survey normally with existing answer
            return self.survey_start(survey_token, answer_token, email, **post)

    @http.route(
        "/survey/submit/<string:survey_token>/<string:answer_token>",
        type="json",
        auth="public",
        website=True,
    )
    def survey_submit(self, survey_token, answer_token, **post):
        access_data = self._get_access_data(
            survey_token, answer_token, ensure_token=True
        )
        if access_data["validity_code"] is not True:
            return {"error": access_data["validity_code"]}

        survey_sudo = access_data["survey_sudo"]
        answer_sudo = access_data["answer_sudo"]

        # Aseta draft-tila ENNEN super(), että save_lines toimii
        if post.get("isFinish") and post.get("isDraft"):
            draft_stage = self._get_draft_stage(survey_sudo, answer_sudo)
            if draft_stage:
                answer_sudo.write({"stage_id": draft_stage.id})

        # Aja core submit
        res = super().survey_submit(survey_token, answer_token, **post)

        # Jos lopullinen lähetys, merkkaa is_editable=False
        if post.get("isFinish") and not post.get("isDraft"):
            sent_stage = self._get_sent_stage(survey_sudo, answer_sudo)
            if sent_stage:
                answer_sudo.write({"stage_id": sent_stage.id, "is_editable": False})

            # Jos palaamme valmisnäkymään, palautetaan se uudelleen käsin
            if answer_sudo.state == "done":
                return {}, self._prepare_question_html(survey_sudo, answer_sudo, **post)

        # Muussa tapauksessa palautetaan core-vastaus
        return res
