from odoo import api, fields, models


class SurveyPrintWizard(models.TransientModel):
    _name = "survey.print.wizard"
    _description = "Survey Print Wizard"

    survey_id = fields.Many2one("survey.survey", required=True)

    partner_id = fields.Many2one("res.partner", string="Contact")

    lang_id = fields.Many2one("survey.language", string="Print Language", required=True)

    @api.model
    def default_get(self, fields_list):
        res = super(SurveyPrintWizard, self).default_get(fields_list)
        survey_id = self.env.context.get("default_survey_id")
        partner_id = self.env.context.get("default_partner_id")

        if partner_id:
            partner = self.env["res.partner"].browse(partner_id)
            if partner.survey_lang_id:
                res["lang_id"] = partner.survey_lang_id.id
            elif survey_id:
                # Fallback to first available survey language
                first_lang = self.env["survey.language"].search(
                    [("active", "=", True)], order="sequence", limit=1
                )
                if first_lang:
                    res["lang_id"] = first_lang.id
        elif survey_id:
            # Fallback to first available survey language
            first_lang = self.env["survey.language"].search(
                [("active", "=", True)], order="sequence", limit=1
            )
            if first_lang:
                res["lang_id"] = first_lang.id

        return res

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        if self.partner_id and self.partner_id.survey_lang_id:
            self.lang_id = self.partner_id.survey_lang_id

    def action_print(self):
        self.ensure_one()
        result = self.survey_id.action_print_survey()
        url = result.get("url", "")
        if url:
            separator = "&" if "?" in url else "?"
            result["url"] = "{}{}survey_lang={}".format(
                url, separator, self.lang_id.code
            )
        return result
