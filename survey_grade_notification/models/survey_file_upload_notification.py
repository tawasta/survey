import logging
import pytz

from odoo import _, fields, models

_logger = logging.getLogger(__name__)


class SurveyQuestionAnswer(models.Model):
    _inherit = "survey.question.answer"

    check_min_value = fields.Boolean(
        string="Check minimum value",
        help="If enabled, this matrix row will be checked for minimum acceptable value.",
    )


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    min_acceptable_value = fields.Float(
        string="Minimum Acceptable Value",
        help="If a response falls below this value, a notification will be triggered.",
    )

    notification_recipients = fields.Many2many(
        "res.users",
        string="Survey Notification Recipients",
        help="Users who will receive notifications when a response to "
        "this question triggers an alert.",
    )


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    # ---- TZ helpers ----
    def _user_tz_name(self, user):
        """Return user's timezone name or UTC fallback."""
        tzname = (user.tz or "UTC").strip() or "UTC"
        try:
            pytz.timezone(tzname)
            return tzname
        except Exception:
            return "UTC"

    def _localize_for_user(self, dt, user):
        """Return dt localized to the given user's timezone."""
        if not dt:
            return dt
        tzname = self._user_tz_name(user)
        # context_timestamp käsittelee Odoo-UTC-naive -> local
        return fields.Datetime.context_timestamp(self.with_context(tz=tzname), dt)

    def _mark_done(self):
        super(SurveyUserInput, self)._mark_done()
        self._check_and_notify_low_responses()

    def _check_and_notify_low_responses(self):
        """Check if any response is below the minimum acceptable value and notify users."""
        email_template = self.env.ref(
            "survey_grade_notification.mail_template_survey_response_alert",
            raise_if_not_found=False,
        ).sudo()
        email_from = self.env.company.email

        notifications = {}

        for user_input_line in self.user_input_line_ids:
            question = user_input_line.question_id

            # MATRIX-kysymys: tarkista vain rivit, joissa check_min_value=True
            if (
                question.question_type == "matrix"
                and user_input_line.matrix_row_id.check_min_value
                and question.min_acceptable_value
            ):
                # käytä line.answer_score jos sellainen on, muutoin suggested_answer_id.answer_score
                score = (
                    user_input_line.answer_score
                    if user_input_line.answer_score is not None
                    else getattr(user_input_line.suggested_answer_id, "answer_score", None)
                )
                if score is not None and score < question.min_acceptable_value:
                    for user in question.notification_recipients:
                        notifications.setdefault(user, []).append((question, score))

            # MUUT kysymystyypit
            if question.question_type != "matrix" and question.min_acceptable_value:
                score = user_input_line.answer_score
                if score is not None and score < question.min_acceptable_value:
                    for user in question.notification_recipients:
                        notifications.setdefault(user, []).append((question, score))

        for user, questions in notifications.items():
            if not user or not user.partner_id or not user.partner_id.email:
                continue
            if email_template:
                email_template.send_mail(
                    self.id,
                    email_values={
                        "email_to": user.partner_id.email,
                        "email_from": email_from,
                        # IMPORTANT: generoidaan body vastaanottajan omaan aikavyöhykkeeseen
                        "body_html": self._generate_low_response_email_body(
                            questions, user
                        ),
                    },
                    notif_layout="mail.mail_notification_light",
                )

    # flake8: noqa: C901
    def _generate_low_response_email_body(self, low_responses, recipient_user):
        """Generate an email body with details about the low responses for a given recipient (localized time)."""
        # Localisoi luontiaika vastaanottajan aikavyöhykkeelle
        local_dt = self._localize_for_user(self.create_date, recipient_user)
        # Varmista, että meillä on strftime-kelpoinen arvo
        time_str = local_dt.strftime("%d.%m.%Y %H:%M") if local_dt else "-"

        message = _("<p><b>Low feedback score given.</b></p>")
        message += _(f"<p><b>Time:</b> {time_str}</p>")
        if self.event_id:
            message += _(
                f"<p><b>Event:</b> {self.event_id.name if self.event_id else 'Not available'}</p>"
            )
        message += _(f"<p><b>Survey:</b> {self.survey_id.title}</p>")
        message += "<ul>"

        for question, response_value in low_responses:
            message += _(
                f"<li><b>Question:</b> {question.title} - {response_value} (Minimum: {question.min_acceptable_value})</li>"
            )

        message += "</ul>"
        return message
