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

from odoo.tests import TransactionCase, tagged


@tagged("at_install")
class TestAnswerPurge(TransactionCase):
    """Test the scheduled cleanup of expired survey answers."""

    def setUp(self):
        super().setUp()

        self.question_model = self.env["survey.question"]
        self.survey = self.env["survey.survey"].create({"title": "Retention test"})
        self.question = self.env["survey.question"].create(
            {
                "survey_id": self.survey.id,
                "title": "Text question",
                "question_type": "text_box",
            }
        )
        self.user_input = self.env["survey.user_input"].create(
            {"survey_id": self.survey.id}
        )

    def _create_answer_line(self, age_days=0):
        """Create an answer line, optionally backdated by the given days."""

        line = self.env["survey.user_input.line"].create(
            {
                "user_input_id": self.user_input.id,
                "question_id": self.question.id,
                "answer_type": "text_box",
                "value_text_box": "an answer",
            }
        )
        if age_days:
            # create_date is set from the database clock, so backdate it there.
            self.env.cr.execute(
                "UPDATE survey_user_input_line"
                " SET create_date = now() - %s * interval '1 day'"
                " WHERE id = %s",
                (age_days, line.id),
            )
            line.invalidate_recordset(["create_date"])
        return line

    def test_purge_expired_by_answer_date(self):
        """Answers older than the question's retention period are deleted."""

        self.question.answer_retention_days = 10
        expired = self._create_answer_line(age_days=20)
        recent = self._create_answer_line(age_days=5)

        self.question_model._cron_purge_expired_answers()

        self.assertFalse(expired.exists(), "Expired answer must be purged.")
        self.assertTrue(recent.exists(), "Recent answer must be kept.")

    def test_no_retention_keeps_answers(self):
        """Answers of questions without a retention period are never purged."""

        old = self._create_answer_line(age_days=400)

        self.question_model._cron_purge_expired_answers()

        self.assertTrue(old.exists(), "Answer without retention period must be kept.")

    def test_retention_days_decide_not_the_toggle(self):
        """The retention period governs the purge, the enable field is a UI switch."""

        # A retention period can be set without the form onchange running, e.g.
        # by an import or by another module writing the field.
        self.question.answer_retention_enabled = False
        self.question.answer_retention_days = 10
        expired = self._create_answer_line(age_days=20)

        self.question_model._cron_purge_expired_answers()

        self.assertFalse(expired.exists(), "Expired answer must be purged.")
