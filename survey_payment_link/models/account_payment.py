from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = "account.payment"

    survey_user_input_id = fields.Many2one(
        "survey.user_input",
        string="Related Survey Input",
        help="Link this payment to a survey-based project/hanke.",
        ondelete="restrict",
    )
