# ruff: noqa
from odoo import http
from odoo.http import request

from odoo.addons.survey.controllers.main import Survey
import logging

_logger = logging.getLogger(__name__)


class SurveyFileDelete(Survey):
    @http.route()
    def survey_submit(self, survey_token, answer_token, **post):
        """
        Override the survey_submit to handle file deletion of attachments
        after standard survey processing.
        """
        # Suorita ensin normaali vastausten tallennus
        response = super().survey_submit(survey_token, answer_token, **post)

        # Tämän jälkeen poista merkityt liitteet
        delete_ids = [
            int(k.replace("delete_attachment_", ""))
            for k in post
            if k.startswith("delete_attachment_")
        ]
        if delete_ids:
            attachments = request.env["ir.attachment"].sudo().browse(delete_ids)
            _logger.info("Deleting attachments with IDs: %s", delete_ids)
            attachments.unlink()

        return response
