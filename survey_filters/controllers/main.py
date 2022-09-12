from odoo import http
from odoo.http import request

from odoo.addons.survey.controllers.main import Survey


class SurveyFilter(Survey):
    @http.route(
        '/survey/results/<model("survey.survey"):survey>/user/<int:user_id>',
        type="http",
        auth="user",
        website=True,
    )
    def survey_report(self, survey, answer_token=None, **post):

        res = super(SurveyFilter, self).survey_report(
            survey,
            answer_token,
        )

        user_input_lines, search_filters = self._extract_filters_data(survey, post)
        user_input_ids = (
            request.env["survey.user_input.line"]
            .sudo()
            .search([("id", "in", user_input_lines.ids)])
            .mapped("user_input_id")
        )

        users = (
            request.env["survey.user_input"]
            .sudo()
            .search([("id", "in", user_input_ids.ids)])
            .mapped("partner_id")
        )
        res.qcontext.update({"users": users})

        return res
