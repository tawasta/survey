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
from odoo import _, api, fields, models
from odoo.exceptions import UserError

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SurveyMailingWizard(models.TransientModel):
    # 1. Private attributes
    _name = "survey.mailing.wizard"
    _description = "Survey Mailing Wizard"

    @api.model
    def _set_default_template(self):
        msg_template = self.env.ref(
            "survey_mailing.survey_mailing_template",
            raise_if_not_found=False,
        )
        return msg_template

    # 2. Fields declaration
    subject = fields.Char(
        compute="_compute_subject", readonly=False, store=True, required=True
    )
    body = fields.Html(
        "Contents",
        sanitize_style=True,
        compute="_compute_body",
        readonly=False,
        store=True,
        required=True,
    )
    attachment_ids = fields.Many2many("ir.attachment", string="Attachments")
    template_id = fields.Many2one(
        "mail.template",
        "Use template",
        domain="[('model', '=', 'survey.user_input')]",
        default=_set_default_template,
        readonly=True,
    )
    recipients = fields.Many2many(
        "survey.user_input",
        default=lambda self: self.env["survey.user_input"].browse(
            self._context.get("active_ids")
        ),
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.depends("template_id")
    def _compute_subject(self):
        for msg in self:
            if msg.template_id:
                msg.subject = msg.template_id.subject
            else:
                msg.subject = False

    @api.depends("template_id")
    def _compute_body(self):
        for msg in self:
            if msg.template_id:
                msg.body = msg.template_id.body_html
            else:
                msg.body = False

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def _get_message_values(self):
        vals = {
            "email_from": self.env.user.email_formatted,
            "subject": self.subject,
            "body": self.body,
            "notify_by_email": True,
            "attachment_ids": self.attachment_ids.ids,
            "message_type": "comment",
            "subtype_xmlid": "mail.mt_comment",
        }
        return vals

    def action_message(self):
        self.ensure_one()

        if not self.env.user.email:
            raise UserError(
                _(
                    "Unable to post message, please configure the sender's email address."
                )
            )

        for recipient in self.recipients:
            message_vals = self._get_message_values()
            recipient.sudo().message_post(**message_vals)

    # 8. Business methods
