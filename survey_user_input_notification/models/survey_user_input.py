##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2019- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
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
import logging

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import models, _


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):

    # 1. Private attributes
    _inherit = "survey.user_input"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods
    def _mark_done(self):
        """ Check if notifications are enabled and create if they are present """
        res = super()._mark_done()
        notif_partners = self.survey_id.notify_partner_ids
        if notif_partners:
            lead = self.env["crm.lead"].sudo().create({
                "name": _("New lead from survey %s", self.survey_id.title),
                "partner_id": self.partner_id,
            })
            # Send notifications to partners
            lead.message_subscribe(notif_partners.ids)
            body = _("This lead was created automatically from survey answer:\n\n")
            body += "<a href='/web?#id={}&model=survey.user_input&view_type=form'>".format(self.id)
            body += _("Link to survey answer</a>")
            lead.message_post(
                subject=_("New lead from survey"),
                body=body,
                partner_ids=notif_partners.ids,
            )

        return res

    # 7. Action methods

    # 8. Business methods
