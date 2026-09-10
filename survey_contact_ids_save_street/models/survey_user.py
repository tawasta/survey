import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    partner_street = fields.Char(string="Partner's Street")

    def _save_partner_street(self, answer):
        """Saves street to partner"""
        self.write({"partner_street": answer})
        self.partner_id.write({"street": answer})
        _logger.debug("Partner's %s street saved.", self.partner_id)

    def _save_lines(self, question, answer, comment=None, overwrite_existing=True):
        """Save answers to questions, depending on question type
        If an answer already exists for question and user_input_id, it will be
        overwritten (or deleted for 'choice' questions) (in order to maintain
        data consistency).
        """
        res = super()._save_lines(question, answer, comment, overwrite_existing)
        if (
            question.question_type == "char_box"
            and question.save_as_partner_street
            and answer
        ):
            self._save_partner_street(answer)
        if (
            question.question_type == "char_box"
            and question.save_as_contact_street
            and answer
        ):
            self._save_contact_field(question, answer, "street")
        return res

    def write(self, vals):
        # Check if partner was set afterwards
        partner_was_set = "partner_id" in vals and vals["partner_id"]
        res = super().write(vals)
        for rec in self:
            if partner_was_set and rec.partner_id and rec.partner_street:
                rec.partner_id.sudo().write({"street": rec.partner_street})
        return res
