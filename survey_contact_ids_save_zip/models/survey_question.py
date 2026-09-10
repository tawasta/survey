from odoo import api, fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    save_as_partner_zip = fields.Boolean(
        compute="_compute_save_as_partner_zip",
        readonly=False,
        store=True,
        copy=True,
        help="If checked, this option will save the user's answer as its partner "
        "zip code.",
    )

    save_as_contact_zip = fields.Boolean(
        compute="_compute_save_as_contact_zip",
        readonly=False,
        store=True,
        copy=True,
        help="If checked, this option will save the user's answer as its contact "
        "zip code.",
    )

    @api.depends("question_type")
    def _compute_save_as_contact_zip(self):
        for question in self:
            if question.question_type != "char_box":
                question.save_as_contact_zip = False

    @api.depends("question_type")
    def _compute_save_as_partner_zip(self):
        for question in self:
            if question.question_type != "char_box":
                question.save_as_partner_zip = False
