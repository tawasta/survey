import json
import logging

from odoo import _, http
from odoo.http import request

from odoo.addons.survey_portal_upload_attachments.controllers.main import (
    SurveyAttachments,
)

_logger = logging.getLogger(__name__)


class SurveyAttachmentsEnhanced(SurveyAttachments):
    @http.route(
        ["/survey/attachments/<string:survey_token>/<string:answer_token>/post"],
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
    )
    def survey_attachments_post(self, survey_token, answer_token, **post):
        """Kutsutaan peruslogiikka ja lisätään tiedoston
        liittämisestä notifikaatiotoiminnallisuus."""

        response = super().survey_attachments_post(survey_token, answer_token, **post)

        # 🔍 Puritaan mahdollinen response.data sisältö JSONiksi
        if hasattr(response, "data"):  # werkzeug Response
            try:
                response_data = json.loads(response.data.decode())
            except Exception as e:
                _logger.warning("Could not decode JSON from Response object: %s", e)
                return response
        elif isinstance(response, str):
            try:
                response_data = json.loads(response)
            except Exception as e:
                _logger.warning("Could not decode JSON from response string: %s", e)
                return response
        elif isinstance(response, dict):
            response_data = response
        else:
            return response  # Tuntematon muoto, palautetaan sellaisenaan

        # ❌ Jos virhe jo olemassa, lopetetaan tähän
        if response_data.get("error"):
            return response

        # ✅ Hae vastaus ja tee varmistukset
        access_data = self._get_access_data(
            survey_token, answer_token, ensure_token=False, check_partner=False
        )

        if access_data["validity_code"] is not True:
            return response

        answer_sudo = access_data["answer_sudo"]
        if (
            not answer_sudo
            or request.env.user.partner_id not in answer_sudo.contact_ids
        ):
            return response

        # 🗂️ Käsittele ladatut tiedostot ja kerää ne ilmoitusta varten
        request_files = request.httprequest.files
        uploaded_files = []
        for file_input in request_files.items(multi=True):
            file_name = file_input[1].filename
            question_id = request.env["survey.question"].browse(int(file_input[0]))
            uploaded_files.append(
                {
                    "question": question_id.title,
                    "file_name": file_name,
                }
            )

        # 📬 Lähetä notifikaatio jos tiedostoja on
        if uploaded_files:
            self._notify_uploaded_files(answer_sudo, uploaded_files)

        return response

    def _notify_uploaded_files(self, answer_sudo, uploaded_files):
        """Lähetä ilmoitus sähköpostitse, kun tiedostoja lisätään."""
        survey = answer_sudo.survey_id
        if not survey.notify_file_upload:
            return

        email_body = (
            _("Attachments have been added to the survey response:")
            + f" {answer_sudo.ref}"
            + "<br><ul>"
        )
        respondent_info = (
            f"{answer_sudo.partner_id.name}" if answer_sudo.partner_id else _("")
        )
        organization_info = (
            f" ({answer_sudo.partner_id.parent_id.name})"
            if answer_sudo.partner_id and answer_sudo.partner_id.parent_id
            else ""
        )
        email_body += _("Respondent:") + f" {respondent_info}{organization_info}<br>"
        for file_info in uploaded_files:
            email_body += f"<li>{file_info['question']} : {file_info['file_name']}</li>"
        email_body += "</ul>"

        email_template = request.env.ref(
            "suvey_notifications.mail_template_survey_file_upload",
            raise_if_not_found=False,
        ).sudo()
        email_from = request.env.company.email

        if email_template:
            for user in survey.notification_user_ids:
                email_template.send_mail(
                    answer_sudo.id,
                    email_values={
                        "email_to": user.partner_id.email,
                        "email_from": email_from,
                        "body_html": email_body,
                    },
                )
