from odoo import models, fields


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    company_id = fields.Many2one(
        'res.company',
        related='survey_id.company_id',
        store=True,
        readonly=True,
    )


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    company_id = fields.Many2one(
        'res.company',
        related='survey_id.company_id',
        store=True,
        readonly=True,
    )


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'

    company_id = fields.Many2one(
        'res.company',
        related='user_input_id.survey_id.company_id',
        store=True,
        readonly=True,
    )
