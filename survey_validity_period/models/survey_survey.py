from odoo import fields, models


class SurveySurvey(models.Model):

    _inherit = "survey.survey"

    qualification_period = fields.Boolean(
        string="Specify the period of qualification", default=False
    )

    interval_nbr = fields.Integer("Interval", default=1)

    interval_unit = fields.Selection(
        [("days", "Days")],
        string="Unit",
        default="days",
    )
