from odoo import http
from odoo.http import request
from odoo.tools import format_date, format_datetime, is_html_empty

from odoo.addons.survey.controllers.main import Survey


class SurveyPrintController(Survey):
    @http.route(
        "/survey/print/<string:survey_token>",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def survey_print(self, survey_token, review=False, answer_token=None, **post):
        access_data = self._get_access_data(
            survey_token, answer_token, ensure_token=False, check_partner=False
        )
        if access_data["validity_code"] is not True and (
            access_data["has_survey_access"]
            or access_data["validity_code"]
            not in ["token_required", "survey_closed", "survey_void"]
        ):
            return self._redirect_with_error(access_data, access_data["validity_code"])

        survey_sudo, answer_sudo = (
            access_data["survey_sudo"],
            access_data["answer_sudo"],
        )

        survey_lang = request.httprequest.args.get("survey_lang")
        if not survey_lang:
            survey_lang = ""

        return request.render(
            "survey.survey_page_print",
            {
                "is_html_empty": is_html_empty,
                "review": review,
                "survey": survey_sudo,
                "answer": answer_sudo
                if survey_sudo.scoring_type != "scoring_without_answers"
                else answer_sudo.browse(),
                "questions_to_display": answer_sudo._get_print_questions(),
                "scoring_display_correction": survey_sudo.scoring_type
                == "scoring_with_answers"
                and answer_sudo,
                "format_datetime": lambda dt: format_datetime(
                    request.env, dt, dt_format=False
                ),
                "format_date": lambda date: format_date(request.env, date),
                "survey_lang_code": survey_lang,
            },
        )
