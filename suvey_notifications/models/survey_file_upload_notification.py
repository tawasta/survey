from odoo import api, fields, models, _
import logging

class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    notification_user_ids = fields.Many2many(
        'res.users',
        string="Notification Users",
        help="Users who will receive notifications for this survey."
    )

    notify_file_upload = fields.Boolean(
        string="Notify on File Upload",
        default=True,
        help="Send notifications to users when a file is uploaded to a question."
    )

    notify_response_submission = fields.Boolean(
        string="Notify on Response Submission",
        default=True,
        help="Send notifications to users when a survey response is submitted."
    )

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'


    @api.returns("mail.message", lambda value: value.id)
    def message_post(self, *args, **kwargs):
        """
        Override to handle notifications for attachments added via chatter.
        """

        if kwargs.get('attachment_ids'):
            attachment_ids = [
                int(attachment_id) for attachment_id in kwargs['attachment_ids']
                if str(attachment_id).isdigit()
            ]
            for attachment_id in attachment_ids:
                self._notify_file_uploads(attachment_id)
        return super().message_post(
            *args,
            **kwargs,
        )

    def _notify_file_uploads(self, attachment_id):
        """Send notifications when a file is uploaded to the chatter."""
        survey = self.survey_id
        if not survey.notify_file_upload:
            return  # Skip notifications if disabled

        # Fetch the attachment details
        attachment = self.env['ir.attachment'].browse(attachment_id)

        # Create email body
        email_body = _(
            "Attachment added to the application:"
        ) + f"<br><ul><li><b>{_('Answer')}:</b> {self.ref} - <b>{_('File')}:</b> {attachment.name}</li></ul>"


        # Send notification emails
        email_template = self.env.ref(
            'suvey_notifications.mail_template_survey_file_upload',
            raise_if_not_found=False
        ).sudo()
        email_from = self.env.company.email

        if email_template:
            for user in survey.notification_user_ids:
                email_template.send_mail(
                    self.id,
                    email_values={
                        'email_to': user.partner_id.email,
                        'email_from': email_from,
                        'body_html': email_body,
                    },
                    notif_layout='mail.mail_notification_light'
                )


    def _mark_done(self):
        """Override to send notification when a response is marked as done."""
        super(SurveyUserInput, self)._mark_done()
        self._notify_response_submission()

    def _notify_response_submission(self):
        """Send notification when a survey response is submitted."""
        survey = self.survey_id
        if not survey.notify_response_submission:
            return  # Don't send notifications if not enabled

        notification_users = survey.notification_user_ids
        email_template = self.env.ref('suvey_notifications.mail_template_survey_response_submission', raise_if_not_found=False).sudo()
        email_from = self.env.company.email

        if email_template:
            for user in notification_users:
                email_template.send_mail(
                    self.id,
                    email_values={
                        'email_to': user.partner_id.email,
                        'email_from': email_from,
                    },
                    notif_layout='mail.mail_notification_light'
                )






