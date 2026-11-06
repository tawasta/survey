from markupsafe import Markup

from odoo import _, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _timed_cleanup_message_body(self, questions):
        """Build the retention cleanup note, naming questions but never answers."""

        self.ensure_one()
        items = Markup("").join(
            Markup("<li>%s</li>") % question.display_name for question in questions
        )
        return Markup("<p>%s</p><ul>%s</ul>") % (
            _(
                "Answers to the following questions were deleted because their "
                "data retention period has ended:"
            ),
            items,
        )
