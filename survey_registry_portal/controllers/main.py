import logging

from odoo import _, http
from odoo.http import request
from odoo.osv.expression import OR

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager

_logger = logging.getLogger(__name__)


class SurveyRegistryPortal(CustomerPortal):
    def _get_survey_registry_domain(self):
        return [("show_in_registry", "=", True)]

    def _get_survey_registry_sortings(self):
        return {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "title_in_survey_registry": {
                "label": _("Title"),
                "order": "title_in_survey_registry",
            },
            "name": {"label": _("Respondent"), "order": "partner_id"},
            "survey": {"label": _("Survey"), "order": "survey_id"},
        }

    def _get_survey_registry_inputs(self):
        return {
            "all": {"label": _("Search in All"), "input": "all"},
            "title_in_survey_registry": {
                "label": _("Title"),
                "input": "title_in_survey_registry",
            },
            "name": {"label": _("Respondent"), "input": "name"},
            "survey": {"label": _("Survey"), "input": "survey"},
        }

    def _get_survey_registry_search_domain(self, search_in, search):
        domain = []
        if search_in in ("name", "all"):
            domain.append([("partner_id.name", "ilike", search)])
        if search_in in ("title_in_survey_registry", "all"):
            domain.append([("title_in_survey_registry", "ilike", search)])
        if search_in in ("survey", "all"):
            domain.append([("survey_id.title", "ilike", search)])

        return OR(domain)

    def _prepare_survey_registry_values(
        self, page, search=None, search_in="all", sortby=None, **kwargs
    ):
        SurveyInput = request.env["survey.user_input"].sudo()
        values = self._prepare_portal_layout_values()

        domain = self._get_survey_registry_domain()
        sortings = self._get_survey_registry_sortings()
        inputs = self._get_survey_registry_inputs()

        if not sortby or sortby not in sortings:
            sortby = "date"
        order = sortings[sortby]["order"]

        if search:
            domain = domain + self._get_survey_registry_search_domain(search_in, search)

        total = SurveyInput.search_count(domain)

        pager = portal_pager(
            url="/surveys/registry",
            url_args={"search": search, "search_in": search_in, "sortby": sortby},
            total=total,
            page=page,
            step=30,  # Tässä asetetaan sivutuksen arvoksi kiinteästi 30
        )

        user_inputs = SurveyInput.search(
            domain, order=order, limit=30, offset=pager["offset"]
        )

        values.update(
            {
                "inputs": user_inputs,
                "page_name": "survey_registry",
                "default_url": "/surveys/registry",
                "pager": pager,
                "search": search,
                "search_in": search_in,
                "sortby": sortby,
                "searchbar_sortings": sortings,
                "searchbar_inputs": inputs,
            }
        )
        return values

    @http.route(
        ["/surveys/registry", "/surveys/registry/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_survey_registry(
        self, page=1, search=None, search_in="all", sortby=None, **kw
    ):
        values = self._prepare_survey_registry_values(
            page, search=search, search_in=search_in, sortby=sortby
        )
        return request.render("survey_registry_portal.survey_registry_page", values)

    @http.route(
        ["/surveys/registry/<int:input_id>"], type="http", auth="public", website=True
    )
    def portal_survey_registry_detail(self, input_id, **kw):
        survey_input = request.env["survey.user_input"].sudo().browse(input_id)
        if not survey_input.exists() or not survey_input.show_in_registry:
            return request.render("website.page_404")
        return request.render(
            "survey_registry_portal.survey_registry_detail",
            {
                "input": survey_input,
                "page_name": "survey_registry",
                "title": survey_input.title_in_survey_registry or "-",
            },
        )
