import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    partner_city = fields.Char(string="Partner's City")

    def _save_partner_city(self, answer):
        """Saves city to partner"""
        self.write({"partner_city": answer})
        self.partner_id.write({"city": answer})
        _logger.debug("Partner's %s city saved.", self.partner_id)

    def _save_lines(self, question, answer, comment=None, overwrite_existing=True):
        """Save answers to questions, depending on question type
        If an answer already exists for question and user_input_id, it will be
        overwritten (or deleted for 'choice' questions) (in order to maintain
        data consistency).
        """
        res = super()._save_lines(question, answer, comment, overwrite_existing)
        if (
            question.question_type == "char_box"
            and question.save_as_partner_city
            and answer
        ):
            self._save_partner_city(answer)
        if (
            question.question_type == "char_box"
            and question.save_as_contact_city
            and answer
        ):
            self._save_contact_field(question, answer, "city")
        return res

    def write(self, vals):
        # Check if partner was set afterwards
        partner_was_set = "partner_id" in vals and vals["partner_id"]
        res = super().write(vals)
        for rec in self:
            if partner_was_set and rec.partner_id and rec.partner_city:
                rec.partner_id.sudo().write({"city": rec.partner_city})
        return res
