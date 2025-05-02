from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    show_in_registry = fields.Boolean(
        string="Show in Registry",
        default=False,
        help="Indicates whether this survey response can be shown in the public registry.",
    )

    def _save_line_choice(self, question, old_answers, answers, comment):
        # Ota raakavastaus talteen ennen kuin super() muokkaa sitä
        raw_answer = None
        if (
            question.question_type == "simple_choice"
            and question.save_as_registry_visibility
        ):
            raw_answer = self.env["survey.question.answer"].browse(int(answers))
        # Kutsu super-metodi
        result = super()._save_line_choice(question, old_answers, answers, comment)

        # Aseta näkyvyystieto superin jälkeen
        if raw_answer:
            normalized = raw_answer.value.strip().lower()
            visibility = normalized in ("kyllä", "yes", "true", "1")
            self.write({"show_in_registry": visibility})

        return result
