from odoo import fields, models


class Survey(models.Model):
    _inherit = "survey.survey"

    answer_retention_auto = fields.Boolean(
        string="Automatic Answer Retention",
        help="Apply the retention period from the system parameter "
        "survey_answer_timed_cleanup.retention_days to every question of "
        "this survey, including questions added later. A retention period "
        "set on an individual question always takes precedence.",
    )
