from odoo import fields, models


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

    funding_underspent_amount = fields.Float(
        string="Funding Amount Underspent",
        digits="Account",
        tracking=True,
    )
    funding_underspent_currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        tracking=True,
        default=lambda self: self.env.company.currency_id.id,
    )

    funding_overspent_amount = fields.Float(
        string="Funding Amount Overspent",
        digits="Account",
        tracking=True,
    )
    funding_overspent_currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        tracking=True,
        default=lambda self: self.env.company.currency_id.id,
    )

    funding_overspent_date = fields.Date(
        string="Funding Overspending Decision Date",
        tracking=True,
    )

    date_finished = fields.Date(tracking=True)
    date_cancelled = fields.Date(tracking=True)
