from odoo import api, fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    service_identifier = fields.Char(tracking=True)

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        domain=[("share", "=", False)],
        help="Person internally responsible for this application",
        tracking=True,
    )

    tax_id = fields.Many2one(
        comodel_name="account.tax",
        string="Tax Rate on the Day of Funding Decision",
        tracking=True,
    )

    funding_decision_date = fields.Date(tracking=True)

    funding_decision_amount = fields.Float(
        string="Amount Funded",
        digits="Account",
        tracking=True,
    )

    funding_decision_currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        tracking=True,
        default=lambda self: self.env.company.currency_id.id,
    )

    funding_decision_terms = fields.Text(string="Terms of Funding Decision")

    funding_left_amount = fields.Float(
        digits="Account",
        tracking=True,
        compute="_compute_funding_left_amount",
        help="Calculated by comparing Amount Funded against Payments made.",
        store=True,
    )

    funding_left_currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        tracking=True,
        default=lambda self: self.env.company.currency_id.id,
    )

    # TODO: currently manual date for logging decision. Could maybe also be
    # automatic from when a payment is logged that exceeds original amount funded?
    funding_overspent_date = fields.Date(
        string="Funding Overspending Decision Date",
        tracking=True,
    )

    date_finished = fields.Date(tracking=True)
    date_cancelled = fields.Date(tracking=True)

    @api.depends(
        "funding_decision_amount",
        "payment_ids",
        "payment_ids.amount",
        "payment_ids.state",
    )
    def _compute_funding_left_amount(self):
        # Compare payments against what was the funding decision

        allowed_states = ["posted"]

        # TODO: put behind settings
        include_draft_payments_in_sum = True
        if include_draft_payments_in_sum:
            allowed_states.append("draft")

        for record in self:
            record.funding_left_amount = record.funding_decision_amount - sum(
                record.payment_ids.filtered(
                    lambda payment: payment.state in allowed_states
                ).mapped("amount")
            )
