from odoo import http
from odoo.http import request

from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.survey.controllers.main import Survey


class SurveyLegacy(Survey):
    @http.route(
        "/survey/start/<string:survey_token>", type="http", auth="public", website=True
    )
    def survey_start(self, survey_token, answer_token=None, email=False, **post):
        if not answer_token:
            answer_token = request.httprequest.cookies.get("survey_%s" % survey_token)

        access_data = self._get_access_data(
            survey_token, answer_token, ensure_token=False
        )

        if access_data.get("validity_code") == "survey_wrong":
            # Try to find survey by id
            survey_id = survey_token.split("-")[-1]
            survey_record = (
                request.env["survey.survey"].sudo().search([("id", "=", survey_id)])
            )
            if slug(survey_record) == survey_token:
                # Use access token as survey token, instead of slug
                survey_token = survey_record.access_token

        return super().survey_start(survey_token, answer_token, email, **post)
