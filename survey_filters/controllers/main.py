from datetime import datetime

from odoo import http
from odoo.http import request

from odoo.addons.survey.controllers.main import Survey


class SurveyFilter(Survey):
    @http.route(
        '/survey/results/<model("survey.survey"):survey>',
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
        use_event = (
            request.env["res.config.settings"]
            .sudo()
            .search([("module_society_event_core", "=", True)])
        )
        use_event_filter = request.env["ir.config_parameter"].get_param(
            "survey.filter.event"
        )
        if use_event_filter and use_event:
            events = (
                request.env["survey.user_input"]
                .sudo()
                .search([("id", "in", user_input_ids.ids)])
                .mapped("event_id")
            )
            res.qcontext.update({"users": users, "events": events})

        return res

    @http.route(
        [
            """/survey/results/<model("survey.survey"):survey>/user/<int:user_id>""",
            """/survey/results/<model("survey.survey"):survey>/user/<int:user_id>/event/<int:event_id>""",
            """/survey/results/<model("survey.survey"):survey>/user/<int:user_id>/date/<string:select_date>""",
            """/survey/results/<model("survey.survey"):survey>/event/<int:event_id>""",
            """/survey/results/<model("survey.survey"):survey>/event/<int:event_id>/date/<string:select_date>""",
            """/survey/results/<model("survey.survey"):survey>/date/<string:select_date>""",
            """/survey/results/<model("survey.survey"):survey>/date/<string:select_date>/event/<int:event_id>""",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def survey_report_filter(
        self,
        survey,
        user_id=None,
        event_id=None,
        select_date=None,
        answer_token=None,
        **post
    ):

        user_input_lines, search_filters = self._extract_survey_data(
            survey, user_id, event_id, select_date, post
        )
        survey_data = survey._prepare_statistics(user_input_lines)
        question_and_page_data = survey.question_and_page_ids._prepare_statistics(
            user_input_lines
        )

        template_values = {
            # survey and its statistics
            "survey": survey,
            "question_and_page_data": question_and_page_data,
            "survey_data": survey_data,
            # search
            "search_filters": search_filters,
            "search_finished": post.get("finished") == "true",
        }
        user_input_lines, search_filters = self._extract_filters_data(survey, post)
        user_input_ids = (
            request.env["survey.user_input.line"]
            .sudo()
            .search([("id", "in", user_input_lines.ids)])
            .mapped("user_input_id")
        )

        use_event = (
            request.env["res.config.settings"]
            .sudo()
            .search([("module_society_event_core", "=", True)])
        )
        use_event_filter = request.env["ir.config_parameter"].get_param(
            "survey.filter.event"
        )
        if use_event_filter and use_event:
            events = (
                request.env["survey.user_input"]
                .sudo()
                .search([("id", "in", user_input_ids.ids)])
                .mapped("event_id")
            )
            template_values.update({"events": events})

        users = (
            request.env["survey.user_input"]
            .sudo()
            .search([("id", "in", user_input_ids.ids)])
            .mapped("partner_id")
        )
        template_values.update({"users": users})

        if user_id:
            user = request.env["res.partner"].sudo().search([("id", "=", user_id)])
            template_values.update({"current_user": user})

        if event_id:
            event = request.env["event.event"].sudo().search([("id", "=", event_id)])

            template_values.update({"current_event": event})

        if survey.session_show_leaderboard:
            template_values["leaderboard"] = survey._prepare_leaderboard_values()

        return request.render("survey.survey_page_statistics", template_values)

    def _extract_survey_data(self, survey, user_id, event_id, select_date, post):
        search_filters = []
        if event_id:
            line_filter_domain, line_choices = [
                ("user_input_id.event_id", "=", event_id)
            ], []
        if user_id:
            line_filter_domain, line_choices = [
                ("user_input_id.partner_id", "=", user_id)
            ], []

        if select_date:
            select_date_obj = datetime.strptime(select_date, "%d.%m.%Y").date()
            line_filter_domain, line_choices = [
                ("user_input_id.create_date", "=", select_date_obj)
            ], []
        if not user_id and not select_date and not event_id:
            line_filter_domain, line_choices = [], []
        for data in post.get("filters", "").split("|"):
            try:
                row_id, answer_id = (int(item) for item in data.split(","))
            except Exception:
                pass
            else:
                if row_id and answer_id:
                    line_filter_domain = [
                        [
                            "&",
                            ("matrix_row_id", "=", row_id),
                            ("suggested_answer_id", "=", answer_id),
                        ],
                        line_filter_domain,
                    ]
                    answers = request.env["survey.question.answer"].browse(
                        [row_id, answer_id]
                    )
                elif answer_id:
                    line_choices.append(answer_id)
                    answers = request.env["survey.question.answer"].browse([answer_id])
                if answer_id:
                    question_id = (
                        answers[0].matrix_question_id or answers[0].question_id
                    )
                    search_filters.append(
                        {
                            "question": question_id.title,
                            "answers": "%s%s"
                            % (
                                answers[0].value,
                                ": %s" % answers[1].value if len(answers) > 1 else "",
                            ),
                        }
                    )
        if line_choices:
            line_filter_domain = [
                [("suggested_answer_id", "in", line_choices)],
                line_filter_domain,
            ]

        user_input_domain = self._get_user_input_domain(
            survey, line_filter_domain, **post
        )
        user_input_lines = (
            request.env["survey.user_input"]
            .sudo()
            .search(user_input_domain)
            .mapped("user_input_line_ids")
        )

        return user_input_lines, search_filters
