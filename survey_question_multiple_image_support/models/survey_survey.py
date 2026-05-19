from odoo import models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    def action_open_print_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Print Survey",
            "res_model": "survey.print.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_survey_id": self.id,
            },
        }
