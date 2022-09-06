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
import base64
import re

# 3. Odoo imports (openerp):
from odoo import _, fields, models

# 4. Imports from Odoo modules:
from odoo.tools.mimetypes import guess_mimetype

# 2. Known third party imports:


# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SurveyQuestion(models.Model):
    # 1. Private attributes
    _inherit = "survey.question"

    # 2. Fields declaration
    question_type = fields.Selection(selection_add=[("attachment", "Attachment")])
    validation_max_attachment_filesize = fields.Integer(
        "Maximum filesize (MB)",
        default=20,
        help="The maximum filesize for the attachment answer in Megabytes",
    )
    is_multiple_attachments = fields.Boolean("Allow Multiple Attachments")
    validation_attachment_file_type = fields.Selection(
        [("pdf", "PDF"), ("image", "Image")],
        string="Limit Attachment File Type",
        help="This field limits the accepted file type for attachments.",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def validate_question(self, answer, comment=None):
        if self.constr_mandatory and self.question_type == "attachment":
            if "values" in answer:
                if (
                    self.validation_attachment_file_type
                    and self.validation_attachment_file_type == "pdf"
                ):
                    for answer_data in answer.get("values"):
                        mimetype = guess_mimetype(
                            base64.b64decode(answer_data.get("data"))
                        )
                        if mimetype != "application/pdf":
                            return {self.id: _("Files must be PDFs.")}
                elif (
                    self.validation_attachment_file_type
                    and self.validation_attachment_file_type == "image"
                ):
                    for answer_data in answer.get("values"):
                        mimetype = guess_mimetype(
                            base64.b64decode(answer_data.get("data"))
                        )
                        if not re.search("^image/", mimetype):
                            return {self.id: _("Files must be images.")}
                return {}
            else:
                return {self.id: self.constr_error_msg}
        return super(SurveyQuestion, self).validate_question(answer, comment)

    # 8. Business methods
