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
import base64
import logging

# 2. Known third party imports:
# 3. Odoo imports (openerp):
from odoo import _, http
from odoo.http import request

# 4. Imports from Odoo modules:
from odoo.addons.survey.controllers.main import Survey

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class SurveyAttachments(Survey):
    def _validate_filesize(self, file_data, max_size):
        if len(file_data) > max_size:
            _logger.warning(
                _("Attachment filesize is too big: %d MB")
                % (len(file_data) / 1024 / 1024)
            )
            return False
        return True

    def _save_line_attachment(self, answer_sudo, file_input):
        question_id = request.env["survey.question"].search(
            [("id", "=", file_input[0])]
        )
        file = file_input[1]
        file_data = file.read()
        max_size = question_id.validation_max_attachment_filesize * 1024 * 1024
        if file.filename and self._validate_filesize(file_data, max_size):
            vals = {
                "user_input_id": answer_sudo.id,
                "question_id": question_id.id,
                "skipped": False,
                "answer_type": question_id.question_type,
                "value_attachment_ids": [
                    (
                        0,
                        4,
                        {
                            "name": file.filename,
                            "store_fname": file.filename,
                            "datas": base64.b64encode(file_data),
                            "description": "Survey Answer Attachment",
                            "type": "binary",
                            "res_model": "survey.user_input.line",
                        },
                    )
                ],
            }
            # _logger.debug(vals)
            answer_line = request.env["survey.user_input.line"].search(
                [
                    ("user_input_id", "=", answer_sudo.id),
                    ("question_id", "=", question_id.id),
                ],
                limit=1,
            )
            answer_line.write(vals)
            _logger.info(
                _("Attachment {file} uploaded for answer line {line}.").format(
                    file=file.filename, line=answer_line
                ),
            )

    @http.route(
        "/survey/attachments/<string:survey_token>/<string:answer_token>",
        type="json",
        auth="public",
        methods=["POST"],
        website=True,
        sitemap=False,
    )
    def survey_attachments(self, survey_token, answer_token, **post):
        """Attachments to survey modal"""
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

        if answer_sudo and request.env.user.partner_id in answer_sudo.contact_ids:
            return (
                request.env["ir.ui.view"]
                .sudo()
                ._render_template(
                    "survey_portal_upload_attachments.survey_attachments_modal",
                    {
                        "answer_token": answer_token,
                        "survey_token": survey_token,
                        "answer": answer_sudo,
                        "survey": answer_sudo.survey_id,
                    },
                )
            )

    @http.route(
        ["""/survey/attachments/<string:survey_token>/<string:answer_token>/post"""],
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def survey_attachments_post(self, survey_token, answer_token, **post):
        """Upload attachments to survey answer"""
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
        if answer_sudo and request.env.user.partner_id in answer_sudo.contact_ids:
            request_files = request.httprequest.files
            for file_input in request_files.items(multi=True):
                self._save_line_attachment(answer_sudo, file_input)
        return request.redirect("/my/surveys")
