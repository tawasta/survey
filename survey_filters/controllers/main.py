from odoo import http
from odoo.http import request

from odoo.addons.survey.controllers.main import Survey


class SurveyFilter(Survey):
    @http.route('/survey/results/<model("survey.survey"):survey>/user/<int:user_id>', type='http', auth='user', website=True)
    def survey_report(self, survey, answer_token=None, **post):

        res =  super(SurveyFilter, self).survey_report(
            survey, answer_token,
        )

        # if res.qcontext.get("question_and_page_data"):
        #     print(res.qcontext.get("question_and_page_data"))
        user_input_lines, search_filters = self._extract_filters_data(
            survey, post
        )
        print(user_input_lines)
        user_input_ids = request.env["survey.user_input.line"].sudo().search([
            ('id', 'in', user_input_lines.ids)
        ]).mapped('user_input_id')

        users = request.env["survey.user_input"].sudo().search([
            ('id', 'in', user_input_ids.ids)
        ]).mapped('partner_id')
        print(users)
        res.qcontext.update({"users": users})
        # survey_data = survey._prepare_statistics(user_input_lines)
        # question_and_page_data = survey.question_and_page_ids._prepare_statistics(
        #     user_input_lines
        # )

        # template_values = {
        #     # survey and its statistics
        #     "survey": survey,
        #     "question_and_page_data": question_and_page_data,
        #     "survey_data": survey_data,
        #     # search
        #     "search_filters": search_filters,
        #     "search_finished": post.get("finished") == "true",
        # }

        # if survey.session_show_leaderboard:
        #     template_values["leaderboard"] = survey._prepare_leaderboard_values()

        return res
