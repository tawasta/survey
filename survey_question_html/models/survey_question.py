##############################################################################
#
#    Author: Futural Oy
#    Copyright 2022- Futural Oy (https://futural.fi)
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
import base64
import re

# 3. Odoo imports (openerp):
from odoo import _, fields, models
from odoo.tools import html2plaintext

# 4. Imports from Odoo modules:
from odoo.tools.mimetypes import guess_mimetype

# 2. Known third party imports:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SurveyQuestion(models.Model):
    # 1. Private attributes
    _inherit = "survey.question"

    # New question type
    question_type = fields.Selection(
        selection_add=[("html", "HTML field")],
    )

    def validate_question(self, answer, comment=None):
        """Validate HTML question when mandatory and optional word limit."""
        self.ensure_one()
        if self.question_type == "html":
            if self.constr_mandatory:
                content = (answer or {}).get("value") if isinstance(answer, dict) else answer
                if not content or not html2plaintext(content or "").strip():
                    return {self.id: self.constr_error_msg or _("This field is required.")}
            return {}
        return super().validate_question(answer, comment)

    # 8. Business methods
