from odoo import api, fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    save_as_partner_city = fields.Boolean(
        compute="_compute_save_as_partner_city",
        readonly=False,
        store=True,
        copy=True,
        help="If checked, this option will save the user's answer as its partner "
        "city.",
    )

    save_as_contact_city = fields.Boolean(
        compute="_compute_save_as_contact_city",
        readonly=False,
        store=True,
        copy=True,
        help="If checked, this option will save the user's answer as its contact "
        "city.",
    )

    @api.depends("question_type")
    def _compute_save_as_contact_city(self):
        for question in self:
            if question.question_type != "char_box":
                question.save_as_contact_city = False

    @api.depends("question_type")
    def _compute_save_as_partner_city(self):
        for question in self:
            if question.question_type != "char_box":
                question.save_as_partner_city = False
