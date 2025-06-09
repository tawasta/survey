# models/survey_user_input.py
from odoo import models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _get_default_mail_template(self):
        # Which template to suggest by default
        return self.env.ref(
            "survey_mailing.survey_mailing_template",
            raise_if_not_found=False,
        )

    def action_survey_user_input_email_send(self):
        # Launch the core e-mail composing wizard
        composer_form_view_id = self.env.ref(
            "mail.email_compose_message_wizard_form"
        ).id

        template_id = self._get_default_mail_template().id

        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "view_id": composer_form_view_id,
            "target": "new",
            "context": {
                "default_composition_mode": "mass_mail"
                if len(self.ids) > 1
                else "comment",
                "default_res_ids": self.ids,
                "default_model": "survey.user_input",
                "default_template_id": template_id,
            },
        }
