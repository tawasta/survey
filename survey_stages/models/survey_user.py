##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SurveyUserInput(models.Model):
    # 1. Private attributes
    _inherit = "survey.user_input"

    @api.model
    def _get_default_stage_id(self):
        return self.env["survey.user_input.stage"].search([], limit=1).id

    # 2. Fields declaration
    stage_id = fields.Many2one(
        "survey.user_input.stage",
        string="Stage",
        ondelete="restrict",
        index=True,
        copy=False,
        default=_get_default_stage_id,
        group_expand="_read_group_stage_ids",
        required=True,
        tracking=True,
    )
    is_accepted = fields.Boolean(related="stage_id.is_accepted", readonly=True)
    is_cancel = fields.Boolean(related="stage_id.is_cancel", readonly=True)
    is_editable = fields.Boolean(related="stage_id.is_editable", readonly=True)
    is_sent = fields.Boolean(related="stage_id.is_sent", readonly=True)
    is_hidden = fields.Boolean(related="stage_id.is_hidden", readonly=True)

    partner_id = fields.Many2one("res.partner", tracking=True)

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def _track_template(self, changes):
        res = super(SurveyUserInput, self)._track_template(changes)
        answer = self[0]
        if "stage_id" in changes and answer.stage_id.mail_template_id:
            res["stage_id"] = (
                answer.stage_id.mail_template_id,
                {
                    "composition_mode": "comment",
                    "message_type": "comment",
                    #"auto_delete_message": True,
                    "subtype_id": self.env["ir.model.data"]._xmlid_to_res_id(
                        "mail.mt_comment"
                    ),
                    "email_layout_xmlid": "mail.mail_notification_light",
                },
            )
        return res

    # 7. Action methods
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """Always display all stages"""
        return stages.search([], order=order)

    def _save_lines(self, question, answer, comment=None, overwrite_existing=True):
        """Override to allow saving if the answer is editable (draft mode)."""
        old_answers = self.env['survey.user_input.line'].search([
            ('user_input_id', '=', self.id),
            ('question_id', '=', question.id)
        ])

        if old_answers and not overwrite_existing and not self.is_editable:
            raise UserError(_("This answer cannot be overwritten."))

        # Kaikki muu kopioidaan coresta
        if question.question_type in ['char_box', 'text_box', 'numerical_box', 'date', 'datetime']:
            self._save_line_simple_answer(question, old_answers, answer)
            if question.save_as_email and answer:
                self.write({'email': answer})
            if question.save_as_nickname and answer:
                self.write({'nickname': answer})

        elif question.question_type in ['simple_choice', 'multiple_choice']:
            self._save_line_choice(question, old_answers, answer, comment)
        elif question.question_type == 'matrix':
            self._save_line_matrix(question, old_answers, answer, comment)
        else:
            raise AttributeError(question.question_type + ": This type of question has no saving function")

    # 8. Business methods
