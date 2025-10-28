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
from odoo import models

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

    # 7. Action methods
    def _save_lines(self, question, answer, comment=None, overwrite_existing=True):
        if question.question_type == "html":
            old = self.env["survey.user_input.line"].search(
                [
                    ("user_input_id", "=", self.id),
                    ("question_id", "=", question.id),
                ]
            )
            vals = {
                "user_input_id": self.id,
                "question_id": question.id,
                "answer_type": "html",
                "skipped": True,
            }
            if isinstance(answer, dict) and answer.get("value") is not None:
                vals.update({"value_html": answer.get("value"), "skipped": False})
            if old:
                if vals.get("skipped") and not old.skipped:
                    vals.update({"skipped": False})
                old.write(vals)
                return old
            return self.env["survey.user_input.line"].create(vals)
        return super()._save_lines(question, answer, comment, overwrite_existing)

    # 8. Business methods
