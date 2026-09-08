from odoo import http
from odoo.http import content_disposition, request

from odoo.addons.survey_portal.controllers.portal import PortalSurveyAnswers


class PortalSurveyCertificate(PortalSurveyAnswers):
    def _generate_certification_report(self, answer):
        report = (
            request.env["ir.actions.report"]
            .sudo()
            ._render_qweb_pdf(
                "survey.certification_report",
                [answer.id],
                data={"report_type": "pdf"},
            )[0]
        )

        return request.make_response(
            report,
            headers=[
                ("Content-Type", "application/pdf"),
                ("Content-Length", len(report)),
                ("Content-Disposition", content_disposition("Certification.pdf")),
            ],
        )

    def _can_download_certification(self, answer):
        """Whether the portal user may download the certificate of an answer"""
        survey = answer.survey_id
        return bool(
            survey.certification
            and survey.certification_downloadable_in_portal
            and answer.scoring_success
        )

    @http.route(
        ["/my/surveys/<int:user_input_id>/certification"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_survey_certification(self, user_input_id, **kw):
        domain = self._get_survey_answers_domain() + [("id", "=", user_input_id)]
        answer_sudo = request.env["survey.user_input"].sudo().search(domain, limit=1)
        if not answer_sudo or not self._can_download_certification(answer_sudo):
            return request.redirect("/my/surveys")

        return self._generate_certification_report(answer_sudo)
