from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import textwrap


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    value_ssn = fields.Char("SSN answer")

    answer_type = fields.Selection(
        selection_add=[("ssn", "SSN")],
    )

    @api.depends(
        "answer_type",
        "value_text_box",
        "value_numerical_box",
        "value_char_box",
        "value_date",
        "value_datetime",
        "value_ssn",
        "suggested_answer_id.value",
        "matrix_row_id.value",
    )
    def _compute_display_name(self):
        for line in self:
            user_in_group = self.env.user.has_group(
                "survey_question_ssn.group_social_security_number"
            )
            if line.answer_type == "char_box":
                line.display_name = line.value_char_box
            elif line.answer_type == "text_box" and line.value_text_box:
                line.display_name = textwrap.shorten(
                    line.value_text_box, width=50, placeholder=" [...]"
                )
            elif line.answer_type == "numerical_box":
                line.display_name = line.value_numerical_box
            elif line.answer_type == "date":
                line.display_name = fields.Date.to_string(line.value_date)
            elif line.answer_type == "datetime":
                line.display_name = fields.Datetime.to_string(line.value_datetime)
            elif line.answer_type == "suggestion":
                if line.matrix_row_id:
                    line.display_name = (
                        f"{line.suggested_answer_id.value}: {line.matrix_row_id.value}"
                    )
                else:
                    line.display_name = line.suggested_answer_id.value
            elif line.answer_type == "ssn":
                line.display_name = line.value_ssn if user_in_group else ""

            if line.answer_type != "ssn" and not line.display_name:
                line.display_name = _("Skipped")
