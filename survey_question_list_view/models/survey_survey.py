from odoo import fields, models


class SurveySurvey(models.Model):

    _inherit = "survey.survey"

    question_count = fields.Integer(
        "Question count",
        compute="_compute_question_count",
    )

    def _compute_question_count(self):
        for record in self:
            record.question_count = len(record.question_ids)

    def action_survey_questions(self):
        action = self.env['ir.actions.act_window']._for_xml_id('survey_question_list_view.survey_question_action')
        ctx = dict(self.env.context)
        ctx.update({'search_default_survey_id': self.ids[0]})
        action['context'] = ctx
        return action
