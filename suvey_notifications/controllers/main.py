from odoo import http
from odoo.http import request, _
import logging
# 4. Imports from Odoo modules:
from odoo.addons.survey_contact_ids.controllers.main import SurveyContacts

# 2. Known third party imports:


# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SurveyFile(SurveyContacts):
    @http.route('/survey/submit/<string:survey_token>/<string:answer_token>', type='json', auth='public', website=True)
    def survey_submit(self, survey_token, answer_token, **post):
        """
        Override the survey_submit to handle file upload notifications for specific changes.
        """
        # Call the original survey_submit to handle core logic
        original_response = super(SurveyFile, self).survey_submit(survey_token, answer_token, **post)
        access_data = self._get_access_data(survey_token, answer_token, ensure_token=True)

        survey_sudo, answer_sudo = access_data['survey_sudo'], access_data['answer_sudo']
        # Process file upload notifications for this session
        self._notify_specific_file_uploads(answer_sudo, post)

        return original_response

    def _notify_specific_file_uploads(self, answer_sudo, post):
        """
        Notify administrators about uploaded files specific to this save action.
        """
        survey = answer_sudo.survey_id
        if not survey.notify_file_upload:
            return  # Skip if notifications are disabled

        # Collect attachment-related questions from the current save action
        uploaded_files = []
        for line in answer_sudo.user_input_line_ids.filtered(lambda l: l.answer_type == 'attachment' and l.value_attachment_ids):
            for attachment in line.value_attachment_ids:
                uploaded_files.append({
                    'question': line.question_id.title,
                    'file_name': attachment.name,
                })

        if not uploaded_files:
            return  # No files uploaded, skip notifications

        # Create email body
        email_body = _("Attachment(s) added to the survey responses:") + "<br><ul>"
        for file_info in uploaded_files:
            email_body += f"<li><b>{_('Question')}:</b> {file_info['question']} - <b>{_('File')}:</b> {file_info['file_name']}</li>"
        email_body += "</ul>"

        # Send notification emails
        email_template = request.env.ref(
            'suvey_notifications.mail_template_survey_file_upload',
            raise_if_not_found=False
        ).sudo()
        email_from = request.env.company.email
        if email_template:
            for user in survey.notification_user_ids:
                email_template.send_mail(
                    answer_sudo.id,
                    email_values={
                        'email_to': user.partner_id.email,
                        'email_from': email_from,
                        'body_html': email_body,
                    },
                    notif_layout='mail.mail_notification_light'
                )
