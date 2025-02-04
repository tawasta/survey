from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    notification_recipients = fields.Many2many(
        'res.users',
        string="Survey Notification Recipients",
        help="Users who will receive notifications for survey responses that trigger alerts."
    )

    enable_response_notifications = fields.Boolean(
        string="Enable Response Notifications",
        default=True,
        help="Send notifications when a survey response meets the alert criteria."
    )

class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    min_acceptable_value = fields.Float(
        string="Minimum Acceptable Value",
        help="If a response falls below this value, a notification will be triggered."
    )

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def _mark_done(self):
        """Override to send notification when a response is marked as done and meets criteria."""
        super(SurveyUserInput, self)._mark_done()
        self._check_and_notify_low_responses()

    def _check_and_notify_low_responses(self):
        """Check if any response is below the minimum acceptable value and notify users."""
        survey = self.survey_id
        if not survey.enable_response_notifications:
            return  # Exit if notifications are not enabled

        notification_users = survey.notification_recipients
        email_template = self.env.ref('survey_grade_notification.mail_template_survey_response_alert', raise_if_not_found=False).sudo()
        email_from = self.env.company.email
        
        low_responses = []
        for user_input_line in self.user_input_line_ids:
            question = user_input_line.question_id
            if question.min_acceptable_value and user_input_line.value_numerical_box < question.min_acceptable_value:
                low_responses.append((question, user_input_line.value_numerical_box))

        if low_responses and email_template:
            for user in notification_users:
                email_template.send_mail(
                    self.id,
                    email_values={
                        'email_to': user.partner_id.email,
                        'email_from': email_from,
                        'body_html': self._generate_low_response_email_body(low_responses)
                    },
                    notif_layout='mail.mail_notification_light'
                )

    def _generate_low_response_email_body(self, low_responses):
        """Generate an email body with details about the low responses."""
        message = "<p>The following survey responses were below the acceptable minimum:</p><ul>"
        for question, response_value in low_responses:
            message += f"<li><b>{question.title}</b>: {response_value} (Minimum: {question.min_acceptable_value})</li>"
        message += "</ul><p>Please review the responses.</p>"
        return message
