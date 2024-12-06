from odoo import http
from odoo.http import request
from odoo.addons.survey_portal_upload_attachments.controllers.main import SurveyAttachments
import logging

_logger = logging.getLogger(__name__)

class SurveyAttachmentsEnhanced(SurveyAttachments):

    @http.route(
        ["/survey/attachments/<string:survey_token>/<string:answer_token>/post"],
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def survey_attachments_post(self, survey_token, answer_token, **post):
        """Kutsutaan peruslogiikka ja lisätään tiedoston liittämisestä notifikaatiotoiminnallisuus."""
        # Kutsutaan alkuperäistä funktiota
        response = super(SurveyAttachmentsEnhanced, self).survey_attachments_post(survey_token, answer_token, **post)

        # Haetaan tarvittavat tiedot
        access_data = self._get_access_data(
            survey_token, answer_token, ensure_token=False, check_partner=False
        )

        # Jos pääsyyn liittyvät ongelmat, ohitetaan lisätoiminnot
        if access_data["validity_code"] is not True:
            return response

        answer_sudo = access_data["answer_sudo"]
        if not answer_sudo or request.env.user.partner_id not in answer_sudo.contact_ids:
            return response

        # Liitetiedostojen käsittely
        request_files = request.httprequest.files
        uploaded_files = []
        for file_input in request_files.items(multi=True):
            file_name = file_input[1].filename
            question_id = request.env["survey.question"].browse(int(file_input[0]))
            uploaded_files.append({
                "question": question_id.title,
                "file_name": file_name,
            })

        # Lähetetään notifikaatio, jos liitteitä on lisätty
        if uploaded_files:
            self._notify_uploaded_files(answer_sudo, uploaded_files)

        return response

    def _notify_uploaded_files(self, answer_sudo, uploaded_files):
        """Lähetä ilmoitus sähköpostitse, kun tiedostoja lisätään."""
        survey = answer_sudo.survey_id
        if not survey.notify_file_upload:
            return  # Ei tehdä mitään, jos ilmoitukset on pois päältä

        # Sähköpostin runko
        email_body = "Attachments have been added to the survey response:<br><ul>"
        for file_info in uploaded_files:
            email_body += f"<li><b>Question:</b> {file_info['question']} - <b>File:</b> {file_info['file_name']}</li>"
        email_body += "</ul>"

        # Hae sähköpostipohja
        email_template = request.env.ref(
            'survey_file_upload_notifications.mail_template_survey_file_upload',
            raise_if_not_found=False
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
                    notif_layout="mail.mail_notification_light",
                )
