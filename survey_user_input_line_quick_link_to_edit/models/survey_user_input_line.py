from odoo import models


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    def action_open_line_form(self):
        self.ensure_one()

        view = self.env.ref("survey.survey_user_input_line_view_form")

        return {
            "type": "ir.actions.act_window",
            "res_model": "survey.user_input.line",
            "res_id": self.id,
            "view_mode": "form",
            "views": [(view.id, "form")],
            "target": "current",
        }
