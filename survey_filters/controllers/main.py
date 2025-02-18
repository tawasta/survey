import logging
from datetime import datetime, timedelta

from odoo import http
from odoo.http import request
from odoo.osv import expression

from odoo.addons.survey.controllers.main import Survey

_logger = logging.getLogger(__name__)


class SurveyFilter(Survey):
    # flake8: noqa: C901
    @http.route(
        '/survey/results/<model("survey.survey"):survey>',
        type="http",
        auth="user",
        website=True,
    )
    def survey_report(
        self,
        survey,
        search="",
        selected_courses=None,
        selected_events=None,
        select_date=None,
        date_end=None,
        answer_token=None,
        **post,
    ):
        logging.info("====VAI TAMAKO?????????")
        res = super(SurveyFilter, self).survey_report(
            survey,
            answer_token,
        )
        user_input_lines, search_filters = self._extract_survey_data(
            survey,
            selected_courses,
            selected_events,
            select_date,
            date_end,
            search,
            post,
        )
        survey_data = survey._prepare_statistics(user_input_lines)
        question_and_page_data = survey.question_and_page_ids._prepare_statistics(
            user_input_lines
        )
        res.qcontext.update(
            {
                "question_and_page_data": question_and_page_data,
                "survey_data": survey_data,
                "search_filters": search_filters,
            }
        )
        user_input_ids = (
            request.env["survey.user_input.line"]
            .sudo()
            .search([("id", "in", user_input_lines.ids)])
            .mapped("user_input_id")
        )
        get_events = (
            request.env["survey.user_input"]
            .sudo()
            .search([("id", "in", user_input_ids.ids)])
            .mapped("event_id")
        )
        courses = (
            request.env["event.event"]
            .sudo()
            .search([("id", "in", get_events.ids)])
            .mapped("course_id")
        )
        res.qcontext.update(
            {
                "courses": courses,
            }
        )
        events = (
            request.env["survey.user_input"]
            .sudo()
            .search([("id", "in", user_input_ids.ids)])
            .mapped("event_id")
        )
        res.qcontext.update({"events": events})

        return res

    # flake8: noqa: C901
    @http.route(
        '/survey/results/<model("survey.survey"):survey>/<path:extrafilters>',
        type="http",
        auth="user",
        website=True,
    )
    def survey_report_filter(self, survey, extrafilters=None, **post):

        # Alustetaan suodattimien muuttujat oletusarvoilla
        selected_courses, selected_events, select_date, date_end = (
            None,
            None,
            None,
            None,
        )

        # Parsitaan extrafilters-parametri
        if extrafilters:
            filter_list = extrafilters.split("/")
            for filter_item in filter_list:
                if "=" in filter_item:
                    filter_name, filter_value = filter_item.split("=", 1)
                    if filter_name == "course":
                        selected_courses = filter_value  # Kurssit pilkulla eroteltuna
                    elif filter_name == "event":
                        selected_events = filter_value  # Tapahtumat pilkulla eroteltuna
                    elif filter_name == "date_start":
                        select_date = filter_value  # Aloituspäivämäärä
                    elif filter_name == "date_end":
                        date_end = filter_value  # Loppupäivämäärä

        if isinstance(selected_events, str):
            selected_events = selected_events.split(",")
        elif not selected_events:
            selected_events = []

        select_events = (
            request.env["event.event"]
            .sudo()
            .search([("id", "in", list(map(int, selected_events)))])
            if selected_events
            else request.env["event.event"]
        )

        if isinstance(selected_courses, str):
            selected_courses = selected_courses.split(",")
        elif not selected_courses:
            selected_courses = []

        select_courses = (
            request.env["op.course"]
            .sudo()
            .search([("id", "in", list(map(int, selected_courses)))])
            if selected_courses
            else request.env["op.course"]
        )

        # Haetaan alkuperäiset vastaukset ilman filttereitä
        all_user_input_lines = (
            request.env["survey.user_input.line"]
            .sudo()
            .search([("survey_id", "=", survey.id)])
        )
        all_user_input_ids = all_user_input_lines.mapped("user_input_id")

        # Haetaan alkuperäiset kurssit ja tapahtumat
        all_events = (
            request.env["survey.user_input"]
            .sudo()
            .search([("id", "in", all_user_input_ids.ids)])
            .mapped("event_id")
        )
        all_courses = (
            request.env["event.event"]
            .sudo()
            .search([("id", "in", all_events.ids)])
            .mapped("course_id")
        )

        # Suodata data _extract_survey_data-metodilla
        user_input_lines, search_filters = self._extract_survey_data(
            survey,
            selected_courses,
            selected_events,
            select_date,
            date_end,
            "",
            post,
        )

        # Luo kyselyt ja sivustonäkymän tiedot
        survey_data = survey._prepare_statistics(user_input_lines)
        question_and_page_data = survey.question_and_page_ids._prepare_statistics(
            user_input_lines
        )

        # Päivitetään templateen välitettävät tiedot, mukaan lukien suodattimien arvot
        template_values = {
            "survey": survey,
            "question_and_page_data": question_and_page_data,
            "survey_data": survey_data,
            "search_filters": search_filters,
            "selected_courses": select_courses,
            "selected_events": select_events,
            "select_date": select_date,
            "date_end": date_end,
            "courses": all_courses,  # Alkuperäiset kurssit
            "events": all_events,  # Alkuperäiset tapahtumat
        }

        # Palautetaan suodatettu näkymä
        return request.render("survey.survey_page_statistics", template_values)

    def _get_user_input_domain(self, survey, line_filter_domain, **post):
        user_input_domain = [
            "&",
            ("test_entry", "=", False),
            ("survey_id", "=", survey.id),
        ]
        if line_filter_domain:
            matching_line_ids = (
                request.env["survey.user_input.line"]
                .sudo()
                .search(line_filter_domain)
                .ids
            )
            logging.info(matching_line_ids)
            user_input_domain = expression.AND(
                [[("user_input_line_ids", "in", matching_line_ids)], user_input_domain]
            )
        if post.get("finished"):
            user_input_domain = expression.AND(
                [[("state", "=", "done")], user_input_domain]
            )
        else:
            user_input_domain = expression.AND(
                [[("state", "!=", "new")], user_input_domain]
            )
        return user_input_domain

    # flake8: noqa: C901
    def _extract_survey_data(
        self,
        survey,
        selected_courses,
        selected_events,
        select_date,
        date_end,
        search,
        post,
    ):
        logging.info("=========== EXTRACTING SURVEY DATA ===========")

        search_filters = []
        line_filter_domain = [("test_entry", "=", False), ("survey_id", "=", survey.id)]
        line_choices = []

        # Parsitaan suodattimet POST-data
        filters = post.get("filters", "")
        for data in filters.split("|"):
            try:
                row_id, answer_id = (int(item) for item in data.split(","))
            except ValueError:
                continue

            if row_id and answer_id:
                line_filter_domain += [
                    "&",
                    ("user_input_line_ids.matrix_row_id", "=", row_id),
                    ("user_input_line_ids.suggested_answer_id", "=", answer_id),
                ]
                answers = (
                    request.env["survey.question.answer"]
                    .sudo()
                    .browse([row_id, answer_id])
                )
                logging.debug(
                    "Adding matrix filter for row: %s, answer: %s", row_id, answer_id
                )
            elif answer_id:
                line_choices.append(answer_id)
                answers = (
                    request.env["survey.question.answer"].sudo().browse([answer_id])
                )

            if answer_id:
                question_id = answers[0].matrix_question_id or answers[0].question_id
                search_filters.append(
                    {
                        "question": question_id.title,
                        "answers": f"{answers[0].value}{': ' + answers[1].value if len(answers) > 1 else ''}",
                    }
                )

        if line_choices:
            line_filter_domain.append(
                ("user_input_line_ids.suggested_answer_id", "in", line_choices)
            )

        # Tila-suodatus
        if post.get("finished"):
            line_filter_domain.append(("state", "=", "done"))
        else:
            line_filter_domain.append(("state", "!=", "new"))

        # Kurssi- ja tapahtumasuodatus yhdistetään yhteen tietokantakyselyyn
        course_ids, event_ids = [], []
        if selected_courses:
            courses = (
                request.env["op.course"].sudo().search([("id", "in", selected_courses)])
            )
            line_filter_domain.append(("event_id.course_id", "in", courses.ids))

        if selected_events:
            events = (
                request.env["event.event"]
                .sudo()
                .search([("id", "in", selected_events)])
            )
            line_filter_domain.append(("event_id", "in", events.ids))

        # Hakusuodatus
        if search:
            line_filter_domain.append(("event_id.name", "ilike", search))

        # Päivämäärärajaukset
        if select_date:
            select_date_obj = datetime.strptime(select_date, "%d.%m.%Y")
            if date_end:
                date_end_obj = datetime.strptime(date_end, "%d.%m.%Y") + timedelta(
                    hours=23, minutes=59, seconds=59
                )
                line_filter_domain += [
                    ("create_date", ">=", select_date_obj),
                    ("create_date", "<=", date_end_obj),
                ]
            else:
                line_filter_domain.append(("create_date", ">=", select_date_obj))

        # Debug-logit
        logging.info("Filter domain: %s", line_filter_domain)
        logging.info("Search filters: %s", search_filters)

        # Haetaan käyttäjän vastaukset yhdellä kyselyllä
        user_input_lines = (
            request.env["survey.user_input"]
            .sudo()
            .search(line_filter_domain)
            .mapped("user_input_line_ids")
        )
        logging.info("User input lines: %s", user_input_lines)

        return user_input_lines, search_filters

    # def _extract_survey_data(
    #     self,
    #     survey,
    #     selected_courses,
    #     selected_events,
    #     select_date,
    #     date_end,
    #     search,
    #     post,
    # ):
    #     logging.info(
    #         "==================FILTTERI EXTRACT SURVEY DATA========================"
    #     )
    #     search_filters = []
    #     line_filter_domain, line_choices = [], []
    #     logging.info(post)
    #     for data in post.get("filters", "").split("|"):
    #         try:
    #             row_id, answer_id = (int(item) for item in data.split(","))
    #         except:
    #             pass
    #         else:
    #             if row_id and answer_id:
    #                 line_filter_domain = expression.AND(
    #                     [
    #                         [
    #                             "&",
    #                             ("user_input_line_ids.matrix_row_id", "=", row_id),
    #                             (
    #                                 "user_input_line_ids.suggested_answer_id",
    #                                 "=",
    #                                 answer_id,
    #                             ),
    #                         ],
    #                         line_filter_domain,
    #                     ]
    #                 )
    #                 logging.info("=============FILTER LINE FILER DOMAIN==========")
    #                 logging.info(line_filter_domain)
    #                 answers = request.env["survey.question.answer"].browse(
    #                     [row_id, answer_id]
    #                 )
    #             elif answer_id:
    #                 logging.info("====MENEEKO TANNE KUN FILTER VALITTU======")
    #                 line_choices.append(answer_id)
    #                 answers = request.env["survey.question.answer"].browse([answer_id])
    #             if answer_id:
    #                 question_id = (
    #                     answers[0].matrix_question_id or answers[0].question_id
    #                 )
    #                 search_filters.append(
    #                     {
    #                         "question": question_id.title,
    #                         "answers": "%s%s"
    #                         % (
    #                             answers[0].value,
    #                             ": %s" % answers[1].value if len(answers) > 1 else "",
    #                         ),
    #                     }
    #                 )
    #     if line_choices:
    #         logging.info("=======LINE CHOICES=================")
    #         logging.info(line_choices)
    #         # line_filter_domain = expression.AND([[('suggested_answer_id', '=', line_choices)], line_filter_domain])
    #         for lc in line_choices:
    #             line_filter_domain += [
    #                 ("user_input_line_ids.suggested_answer_id", "=", lc)
    #             ]
    #     line_filter_domain += [("test_entry", "=", False)]
    #     line_filter_domain += [("survey_id", "=", survey.id)]
    #     if post.get("finished"):
    #         line_filter_domain += [("state", "=", "done")]
    #     else:
    #         line_filter_domain += [("state", "!=", "new")]

    #     if selected_courses:
    #         select_courses = (
    #             request.env["op.course"]
    #             .sudo()
    #             .search([("id", "in", list(map(int, selected_courses.split(","))))])
    #         )
    #         line_filter_domain += [("event_id.course_id", "in", select_courses.ids)]
    #     if search:
    #         line_filter_domain += [("event_id.name", "ilike", search)]
    #     if selected_events:
    #         select_events = (
    #             request.env["event.event"]
    #             .sudo()
    #             .search([("id", "in", list(map(int, selected_events.split(","))))])
    #         )
    #         line_filter_domain += [("event_id", "in", select_events.ids)]
    #     # if user_id:
    #     #     line_filter_domain += [("partner_id", "=", user_id)]

    #     if select_date and not date_end:
    #         select_date_obj = datetime.strptime(select_date, "%d.%m.%Y")
    #         select_date_end_obj = select_date_obj + timedelta(
    #             hours=23, minutes=59, seconds=59
    #         )
    #         line_filter_domain += [
    #             ("create_date", ">=", select_date_obj),
    #             ("create_date", "<=", select_date_end_obj),
    #         ]
    #     if select_date and date_end:
    #         select_date_start_obj = datetime.strptime(select_date, "%d.%m.%Y")
    #         select_date_end_obj = datetime.strptime(date_end, "%d.%m.%Y")
    #         date_end_obj = select_date_end_obj + timedelta(
    #             hours=23, minutes=59, seconds=59
    #         )
    #         line_filter_domain += [
    #             ("create_date", ">=", select_date_start_obj),
    #             ("create_date", "<=", date_end_obj),
    #         ]
    #     logging.info(line_filter_domain)
    #     logging.info(search_filters)

    #     user_input_lines = (
    #         request.env["survey.user_input"]
    #         .sudo()
    #         .search(line_filter_domain)
    #         .mapped("user_input_line_ids")
    #     )
    #     logging.info(user_input_lines)
    #     # user_input_domain = self._get_user_input_domain(survey, line_filter_domain, **post)

    #     # user_input_lines = request.env['survey.user_input'].sudo().search(user_input_domain).mapped('user_input_line_ids')
    #     logging.info(search_filters)
    #     return user_input_lines, search_filters

    # def _extract_survey_data(
    #     self, survey, user_id, event_id, select_date, date_end, search, post
    # ):
    #     search_filters = []
    #     line_filter_domain = []
    #     line_choices = []
    #     if search:
    #         line_filter_domain += [("user_input_id.event_id.name", "ilike", search)]
    #     if event_id:
    #         line_filter_domain += [("user_input_id.event_id", "=", event_id)]
    #     if user_id:
    #         line_filter_domain += [("user_input_id.partner_id", "=", user_id)]

    #     if select_date and not date_end:
    #         select_date_obj = datetime.strptime(select_date, "%d.%m.%Y")
    #         select_date_end_obj = select_date_obj + timedelta(
    #             hours=23, minutes=59, seconds=59
    #         )
    #         line_filter_domain += [
    #             ("user_input_id.create_date", ">=", select_date_obj),
    #             ("user_input_id.create_date", "<=", select_date_end_obj),
    #         ]
    #     if select_date and date_end:
    #         select_date_start_obj = datetime.strptime(select_date, "%d.%m.%Y")
    #         select_date_end_obj = datetime.strptime(date_end, "%d.%m.%Y")
    #         date_end_obj = select_date_end_obj + timedelta(
    #             hours=23, minutes=59, seconds=59
    #         )
    #         line_filter_domain += [
    #             ("user_input_id.create_date", ">=", select_date_start_obj),
    #             ("user_input_id.create_date", "<=", date_end_obj),
    #         ]
    #     if (
    #         not user_id
    #         and not select_date
    #         and not event_id
    #         and not search
    #         and not date_end
    #     ):
    #         line_filter_domain, line_choices = [], []
    #     for data in post.get("filters", "").split("|"):
    #         try:
    #             row_id, answer_id = (int(item) for item in data.split(","))
    #         except Exception:
    #             pass
    #         else:
    #             if row_id and answer_id:
    #                 line_filter_domain = expression.AND(
    #                     [
    #                         [
    #                             "&",
    #                             ("matrix_row_id", "=", row_id),
    #                             ("suggested_answer_id", "=", answer_id),
    #                         ],
    #                         line_filter_domain,
    #                     ]
    #                 )
    #                 answers = request.env["survey.question.answer"].browse(
    #                     [row_id, answer_id]
    #                 )
    #             elif answer_id:
    #                 line_choices.append(answer_id)
    #                 answers = request.env["survey.question.answer"].browse([answer_id])
    #             if answer_id:
    #                 question_id = (
    #                     answers[0].matrix_question_id or answers[0].question_id
    #                 )
    #                 search_filters.append(
    #                     {
    #                         "question": question_id.title,
    #                         "answers": "%s%s"
    #                         % (
    #                             answers[0].value,
    #                             ": %s" % answers[1].value if len(answers) > 1 else "",
    #                         ),
    #                     }
    #                 )
    #     if line_choices:
    #         line_filter_domain = expression.AND(
    #             [[("suggested_answer_id", "in", line_choices)], line_filter_domain]
    #         )

    #     user_input_domain = self._get_user_input_domain(
    #         survey, line_filter_domain, **post
    #     )
    #     user_input_lines = (
    #         request.env["survey.user_input"]
    #         .sudo()
    #         .search(user_input_domain)
    #         .mapped("user_input_line_ids")
    #     )

    #     return user_input_lines, search_filters
