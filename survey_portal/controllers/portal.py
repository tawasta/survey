##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import _, http
from odoo.http import request

# 4. Imports from Odoo modules:
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class PortalSurveyAnswers(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "survey_answer_count" in counters:
            survey_answer_count = (
                request.env["survey.user_input"]
                .sudo()
                .search_count(self._get_survey_answers_domain())
            )
            values["survey_answer_count"] = survey_answer_count or 0
        return values

    def _survey_answer_get_page_view_values(self, answer, **kwargs):
        values = {
            "page_name": "survey_answer",
            "answer": answer,
        }
        return values

    def _get_survey_answers_domain(self):
        return [
            ("partner_id.id", "=", request.env.user.partner_id.id),
            ("test_entry", "!=", True),
        ]

    def _get_survey_answers_searchbar_sortings(self):
        return {
            "date": {"label": _("Date"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "display_name desc"},
        }

    def _get_survey_answers_searchbar_filters(self):
        return {
            "all": {"label": _("All"), "domain": []},
        }

    @http.route(
        ["/my/surveys", "/my/surveys/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_surveys(
        self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw
    ):
        values = self._prepare_portal_layout_values()
        SurveyUserInput = request.env["survey.user_input"]
        domain = self._get_survey_answers_domain()
        searchbar_sortings = self._get_survey_answers_searchbar_sortings()
        # default sort by
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        searchbar_filters = self._get_survey_answers_searchbar_filters()
        # default filter value
        if not filterby:
            filterby = "all"
        domain += searchbar_filters[filterby]["domain"]
        if date_begin:
            domain += [("create_date", ">", date_begin)]
        # count for pager
        answer_count = SurveyUserInput.sudo().search_count(domain)
        pager = portal_pager(
            url="/my/surveys",
            url_args={"date_begin": date_begin, "sortby": sortby},
            total=answer_count,
            page=page,
            step=self._items_per_page,
        )
        answers = SurveyUserInput.sudo().search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )
        values.update(
            {
                "date": date_begin,
                "survey_answers": answers,
                "page_name": "survey_answer",
                "pager": pager,
                "default_url": "/my/surveys",
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
                "searchbar_filters": searchbar_filters,
                "filterby": filterby,
            }
        )
        return request.render("survey_portal.portal_my_survey_answers", values)

    @http.route(
        ["/my/surveys/<int:user_input_id>"], type="http", auth="user", website=True
    )
    def portal_my_survey_detail(
        self, user_input_id, access_token=None, report_type=None, download=False, **kw
    ):
        domain = self._get_survey_answers_domain() + [("id", "=", user_input_id)]
        answer_sudo = (
            request.env["survey.user_input"]
            .sudo()
            .search(
                domain,
                limit=1,
            )
        )
        if not answer_sudo:
            return request.redirect("/my")
        values = self._survey_answer_get_page_view_values(answer_sudo)
        return request.render("survey_portal.portal_answer_page", values)
