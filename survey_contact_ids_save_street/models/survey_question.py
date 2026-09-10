from odoo import api, fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    save_as_partner_street = fields.Boolean(
        compute="_compute_save_as_partner_street",
        readonly=False,
        store=True,
        copy=True,
        help="If checked, this option will save the user's answer as its partner "
        "street.",
    )

    save_as_contact_street = fields.Boolean(
        compute="_compute_save_as_contact_street",
        readonly=False,
        store=True,
        copy=True,
        help="If checked, this option will save the user's answer as its contact "
        "street.",
    )

    @api.depends("question_type")
    def _compute_save_as_contact_street(self):
        for question in self:
            if question.question_type != "char_box":
                question.save_as_contact_street = False

    @api.depends("question_type")
    def _compute_save_as_partner_street(self):
        for question in self:
            if question.question_type != "char_box":
                question.save_as_partner_street = False
