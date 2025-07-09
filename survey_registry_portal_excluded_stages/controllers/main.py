import logging

from odoo.http import request

from odoo.addons.survey_registry_portal.controllers.main import SurveyRegistryPortal

_logger = logging.getLogger(__name__)


class SurveyRegistryExludedStagesPortal(SurveyRegistryPortal):
    def _get_survey_registry_domain(self):
        return [
            ("show_in_registry", "=", True),
            ("stage_id.survey_registry_entries_always_hidden", "=", False),
        ]

    def portal_survey_registry_detail(self, input_id, **kw):
        # Deny access based on the stage
        survey_input = request.env["survey.user_input"].sudo().browse(input_id)
        if (
            not survey_input.exists()
            or survey_input.stage_id.survey_registry_entries_always_hidden
        ):
            return request.render("website.page_404")

        return super().portal_survey_registry_detail(input_id, **kw)
