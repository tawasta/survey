from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    min_acceptable_value = fields.Float(
        string="Minimum Acceptable Value",
        help="If a response falls below this value, a notification will be triggered."
    )

    notification_recipients = fields.Many2many(
        'res.users',
        string="Survey Notification Recipients",
        help="Users who will receive notifications when a response to this question triggers an alert."
    )

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def _mark_done(self):
        """Override to send notification when a response is marked as done and meets criteria."""
        super(SurveyUserInput, self)._mark_done()
        self._check_and_notify_low_responses()

    def _check_and_notify_low_responses(self):
        """Check if any response is below the minimum acceptable value and notify users."""
        email_template = self.env.ref('survey_grade_notification.mail_template_survey_response_alert', raise_if_not_found=False).sudo()
        email_from = self.env.company.email
        
        low_responses = []
        notifications = {}
        
        for user_input_line in self.user_input_line_ids:
            question = user_input_line.question_id
            if question.min_acceptable_value and user_input_line.answer_score < question.min_acceptable_value:
                low_responses.append((question, user_input_line.answer_score))
                for user in question.notification_recipients:
                    if user not in notifications:
                        notifications[user] = []
                    notifications[user].append((question, user_input_line.answer_score))
        
        for user, questions in notifications.items():
            logging.info(user);
            if email_template:
                email_template.send_mail(
                    self.id,
                    email_values={
                        'email_to': user.partner_id.email,
                        'email_from': email_from,
                        'body_html': self._generate_low_response_email_body(questions)
                    },
                    notif_layout='mail.mail_notification_light'
                )

    def _generate_low_response_email_body(self, low_responses):
        """Generate an email body with details about the low responses."""
        message = _("<p><b>Low feedback score given.</b></p>")
        message += _(f"<p><b>Time:</b> {self.create_date.strftime('%d.%m.%Y %H:%M')}</p>")
        if self.event_id:
            message += _(f"<p><b>Event:</b> {self.event_id.name if self.event_id else 'Not available'}</p>")
        message += _(f"<p><b>Survey:</b> {self.survey_id.title}</p>")
        message += "<ul>"
        
        for question, response_value in low_responses:
            message += _(f"<li><b>Question:</b> {question.title} - {response_value} (Minimum: {question.min_acceptable_value})</li>")
        
        message += "</ul>"
        return message
