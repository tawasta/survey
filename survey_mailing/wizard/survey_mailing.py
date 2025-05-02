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
            "attachment_ids": self.attachment_ids.ids,
            "message_type": "comment",
            "subtype_xmlid": "mail.mt_comment",
        }
        return vals

    def action_message(self):
        self.ensure_one()

        if not self.env.user.email:
            raise UserError(
                _("Please configure your user email address to send messages.")
            )

        if not self.subject or not self.body:
            raise UserError(_("Subject and body are required to send a message."))

        template = self.template_id
        if not template:
            raise UserError(_("Email template not found."))

        for recipient in self.recipients:
            if not recipient.partner_id or not recipient.partner_id.email:
                continue  # skip if no partner or email

            # Create message in chatter
            recipient.message_post(
                body=self.body,
                subject=self.subject,
                message_type="email",
                email_from=self.env.user.email_formatted,
                partner_ids=[recipient.partner_id.id],
                attachment_ids=self.attachment_ids.ids,
                subtype_xmlid="mail.mt_comment",
            )

            # Send email from template to the same partner
            template.with_context(
                default_model="survey.user_input",
                default_res_id=recipient.id,
                default_composition_mode="comment",
                force_send=True,
            ).send_mail(
                recipient.id,
                force_send=True,
                email_values={
                    "email_to": recipient.partner_id.email,
                    "email_from": self.env.user.email_formatted,
                    "body_html": self.body,
                    "subject": self.subject,
                    "attachment_ids": [(6, 0, self.attachment_ids.ids)],
                },
            )

    # 8. Business methods
