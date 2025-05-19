from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    notification_user_ids = fields.Many2many(
        "res.users",
        string="Notified Users",
        help="Users who will receive notifications for this survey.",
    )

    notify_file_upload = fields.Boolean(
        string="Notify on File Upload",
        default=True,
        help="Send notifications to users when a file is uploaded to a question.",
    )

    notify_response_submission = fields.Boolean(
        string="Notify on Response Submission",
        default=True,
        help="Send notifications to users when a survey response is submitted.",
    )
