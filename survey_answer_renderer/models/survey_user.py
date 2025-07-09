from odoo import fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def render_answers_html(self):
        """Return all questions and answers in HTML format."""
        self.ensure_one()
        return "".join(line.render_display_html() for line in self.user_input_line_ids)


class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    def get_display_answer(self):
        """Return the plain-text answer for this line."""
        self.ensure_one()
        mapping = {
            "char_box": self.value_char_box or "",
            "text_box": self.value_text_box or "",
            "numerical_box": str(self.value_numerical_box)
            if self.value_numerical_box is not None
            else "",
            "date": fields.Date.to_string(self.value_date) if self.value_date else "",
            "datetime": fields.Datetime.to_string(self.value_datetime)
            if self.value_datetime
            else "",
        }
        if self.answer_type in mapping:
            return mapping[self.answer_type]
        elif self.answer_type == "suggestion":
            if self.matrix_row_id:
                return f"{self.suggested_answer_id.value}: {self.matrix_row_id.value}"
            return self.suggested_answer_id.value or ""
        return ""

    def get_display_answer_html(self):
        """Return the HTML-formatted answer for this line."""
        self.ensure_one()
        answer = self.get_display_answer()
        return answer or "<em>–</em>"

    def render_display_html(self):
        """Return HTML representation of the question and answer."""
        self.ensure_one()
        question = self.question_id.display_name or ""
        answer = self.get_display_answer_html()
        return f"<p><strong>{question}</strong><br/>{answer}</p>"
