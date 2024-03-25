from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError


class SurveyInvite(models.TransientModel):

    _inherit = "survey.invite"

    @api.depends("template_id")
    def _compute_email_from(self):
        for invite in self:
            if (
                invite.template_id
                and invite.template_id.email_from
                and tools.email_normalize(invite.template_id.email_from)
            ):
                invite.email_from = invite.template_id.email_from
            elif self.env.user.email:
                invite.email_from = self.env.user.email_formatted
            else:
                raise UserError(
                    _(
                        "Unable to post message, please configure the sender's email address."
                    )
                )

    email_from = fields.Char(compute="_compute_email_from")
