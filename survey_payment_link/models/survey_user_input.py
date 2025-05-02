from odoo import models, fields


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    payment_ids = fields.One2many(
        "account.payment",
        "survey_user_input_id",
        string="Payments",
        help="Payments linked to this survey input (project/grant/etc).",
    )

    def action_create_payment(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Create Payment",
            "res_model": "account.payment",
            "view_mode": "form",
            "context": {
                "default_survey_user_input_id": self.id,
                "default_partner_id": self.partner_id.id if self.partner_id else False,
                "default_payment_type": "outbound",
                "default_partner_type": "supplier",
            },
            "target": "current",
        }
