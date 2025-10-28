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
import logging

# 2. Known third party imports:
# 3. Odoo imports (openerp):
from odoo import _, api, fields, models
from odoo.tools import html2plaintext

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class SurveyUserInputLine(models.Model):
    # 1. Private attributes
    _inherit = "survey.user_input.line"

    answer_type = fields.Selection(selection_add=[("html", "HTML")])
    value_html = fields.Html(string="HTML Answer")

    @api.depends(
        "answer_type",
        "value_html",
        "value_text_box",
        "value_char_box",
        "value_numerical_box",
        "value_date",
        "value_datetime",
    )
    def _compute_string_answer(self):
        res = super()._compute_string_answer()
        for line in self:
            if line.answer_type == "html" and line.value_html:
                line.string_answer = html2plaintext(line.value_html)[:200]
        return res

    @api.depends(
        "answer_type",
        "value_html",
        "value_text_box",
        "value_char_box",
        "value_numerical_box",
        "value_date",
        "value_datetime",
    )
    def _compute_display_name(self):
        res = super()._compute_display_name()
        for line in self:
            if line.answer_type == "html":
                line.display_name = _("HTML")
        return res

    @api.constrains("skipped", "answer_type")
    def _check_answer_type_skipped(self):
        for line in self:
            if line.answer_type != "html":
                return super(SurveyUserInputLine, line)._check_answer_type_skipped()

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
