from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models


class SurveyUserInput(models.Model):

    _inherit = "survey.user_input"

    start_date = fields.Date(string="Start Date", readonly=False)

    end_date = fields.Date(string="End Date", readonly=False)

    qualification_period = fields.Boolean(
        string="Specify the period of qualification",
        related="survey_id.qualification_period",
    )

    def write(self, vals):
        res = super(SurveyUserInput, self).write(vals)
        if vals.get("stage_id"):
            stage = (
                self.env["survey.user_input.stage"]
                .sudo()
                .search([("id", "=", vals.get("stage_id"))])
            )
            if stage.is_accepted and self.qualification_period and not self.start_date:
                start_date = fields.Date.today()
                days_val = self.survey_id.interval_nbr
                end_date = start_date + relativedelta(days=days_val)
                self.sudo().write({"start_date": start_date, "end_date": end_date})
                self.message_post(
                    body=(_("%s has accepted qualification") % (self.env.user.name))
                )

        return res

    @api.model
    def _cron_update_user_input_state(self):
        now = fields.Date.today()
        confirm_stage_id = (
            self.env["survey.user_input.stage"]
            .sudo()
            .search([("is_accepted", "=", True)])
        )
        user_input_ids = (
            self.env["survey.user_input"]
            .sudo()
            .search(
                [
                    ("qualification_period", "=", True),
                    ("stage_id", "=", confirm_stage_id.id),
                ]
            )
        )
        ended_stage = (
            self.env["survey.user_input.stage"].sudo().search([("is_end", "=", True)])
        )
        for user_input in user_input_ids:
            if now > user_input.end_date:
                user_input.sudo().write(
                    {
                        "stage_id": ended_stage.id,
                    }
                )
            if now - relativedelta(days=7) == user_input.end_date:
                message_template = self.env.ref(
                    "survey_validity_period.mail_template_data_participation_ending"
                )
                values = {
                    "email_to": user_input.partner_id.email,
                    "email_from": "lorem@lorem.fi",
                }
                message_template.sudo().write(values)
                message_template.sudo().send_mail(user_input.id, force_send=True)
