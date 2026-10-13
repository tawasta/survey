##############################################################################
#
#    Author: Futural Oy
#    Copyright 2026 Futural Oy (https://futural.fi)
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
from dateutil.relativedelta import relativedelta

# 3. Odoo imports (openerp):
from odoo import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class SurveyQuestion(models.Model):
    # 1. Private attributes
    _inherit = "survey.question"

    # 2. Fields declaration
    answer_retention_days = fields.Integer(
        string="Answer Data Retention (days)",
        help="Number of days an answer to this question is kept before it is "
        "deleted by the scheduled cleanup action, counted from when the answer "
        "was recorded. Applies to every response, including unfinished ones. "
        "Leave empty or zero to keep the answers indefinitely.",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def _cron_purge_expired_answers(self):
        """Delete answers older than each question's retention period.

        Runs across all responses, including in-progress ones, so no personal
        answer data survives past its retention window.
        """
        retention_questions = self.search([("answer_retention_days", ">", 0)])
        if not retention_questions:
            _logger.info(
                "Survey answer cleanup: no questions have a retention period set."
            )
            return

        now = fields.Datetime.now()
        answer_lines = self.env["survey.user_input.line"]
        deleted = self.env["survey.user_input.line"]
        for question in retention_questions:
            cutoff = now - relativedelta(days=question.answer_retention_days)
            expired_lines = answer_lines.search(
                [
                    ("question_id", "=", question.id),
                    ("create_date", "<", cutoff),
                ]
            )
            deleted |= expired_lines
        if deleted:
            deleted.unlink()
        _logger.info(
            "Survey answer cleanup: checked %s question(s), "
            "deleted %s expired answer line(s).",
            len(retention_questions),
            len(deleted),
        )

    def _cron_purge_all_answers(self):
        """Delete every answer of questions that have a retention period set.

        Same scope as the timed cleanup but ignores the date, so it wipes all
        answer data of those questions the moment it is run.
        """
        retention_questions = self.search([("answer_retention_days", ">", 0)])
        if not retention_questions:
            _logger.info(
                "Survey answer cleanup: no questions have a retention period set."
            )
            return

        answer_lines = self.env["survey.user_input.line"]
        deleted = answer_lines.search([("question_id", "in", retention_questions.ids)])
        if deleted:
            deleted.unlink()
        _logger.info(
            "Survey answer cleanup: checked %s question(s), "
            "deleted %s answer line(s) regardless of age.",
            len(retention_questions),
            len(deleted),
        )

    # 8. Business methods
