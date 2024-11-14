from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re

class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    # Lisää SSN-kysymystyyppi valintoihin
    question_type = fields.Selection(
        selection_add=[('ssn', 'SSN')],
        help="Select SSN type to allow Social Security Number input."
    )

    def validate_question(self, answer, comment=None):
        self.ensure_one()

        # Tarkista, onko SSN-kysymys
        if self.question_type == 'ssn':
            return self._validate_ssn(answer)

        return super(SurveyQuestion, self).validate_question(answer, comment)

    def _validate_ssn(self, answer):

        # Tarkistetaan pakollisuus
        if self.constr_mandatory and not answer:
            return {self.id: self.constr_error_msg or _('This question requires an SSN entry.')}

        # Tarkistetaan SSN:n muoto
        ssn_pattern = r'^\d{6}[+-A]\d{3}[A-Z0-9]$'
        if answer and not re.match(ssn_pattern, answer):
            return {self.id: self.validation_error_msg or _('The SSN format is invalid. It should be in the format DDMMYY-XXXC.')}

        return {}
