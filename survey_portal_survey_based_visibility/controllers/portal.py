from odoo.addons.survey_portal.controllers.portal import PortalSurveyAnswers


class PortalSurveyAnswersVisibility(PortalSurveyAnswers):
    def _get_survey_answers_domain(self):
        domain = super()._get_survey_answers_domain()
        domain += [("survey_id.hide_survey_result_in_portal", "=", False)]
        return domain
