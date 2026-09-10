from odoo import models


class Survey(models.Model):
    _inherit = "survey.survey"

    def _create_answer(
        self,
        user=False,
        partner=False,
        email=False,
        test_entry=False,
        check_attempts=True,
        **additional_vals,
    ):
        """Saves partner street from answer"""
        res = super()._create_answer(
            user, partner, email, test_entry, check_attempts, **additional_vals
        )
        for question in self.mapped("question_ids").filtered(
            lambda q: q.question_type == "char_box" and q.save_as_partner_street
        ):
            for user_input in res:
                if question.save_as_partner_street and user_input.partner_street:
                    user_input._save_lines(question, user_input.partner_street)
        return res
