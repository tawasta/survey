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
        self.question = self._create_question("Text question")
        self.user_input = self.env["survey.user_input"].create(
            {"survey_id": self.survey.id}
        )

    def _create_question(self, title):
        """Create another question on the test survey."""

        return self.env["survey.question"].create(
            {
                "survey_id": self.survey.id,
                "title": title,
                "question_type": "text_box",
            }
        )

    def _enable_retention(self, days, question=None):
        """Arm the cleanup on a question the way the form does: switch and period."""

        (question or self.question).write(
            {"answer_retention_enabled": True, "answer_retention_days": days}
        )

    def _create_answer_line(self, age_days=0, question=None):
        """Create an answer line, optionally backdated by the given days."""

        line = self.env["survey.user_input.line"].create(
            {
                "user_input_id": self.user_input.id,
                "question_id": (question or self.question).id,
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

    def _run_cleanup(self):
        """Run the cleanup cron and return only the notes it posted."""

        # Creating a response already logs a "created" message in the chatter,
        # so measure the delta of one run instead of counting the whole chatter.
        baseline = self.user_input.message_ids.ids
        self.question_model._cron_purge_expired_answers()
        # Force a fresh read: the notes come from a batch insert that leaves
        # this record's cache the way message_post would not.
        self.user_input.invalidate_recordset(["message_ids"])
        return self.user_input.message_ids.filtered(
            lambda message: message.id not in baseline
        )

    def test_purge_expired_by_answer_date(self):
        """Answers older than the question's retention period are deleted."""

        self._enable_retention(10)
        expired = self._create_answer_line(age_days=20)
        recent = self._create_answer_line(age_days=5)

        self.question_model._cron_purge_expired_answers()

        self.assertFalse(expired.exists(), "Expired answer must be purged.")
        self.assertTrue(recent.exists(), "Recent answer must be kept.")

    def test_zero_retention_days_keeps_answers(self):
        """Answers are never deleted while the retention period is zero."""

        self._enable_retention(0)
        old = self._create_answer_line(age_days=400)

        self.question_model._cron_purge_expired_answers()

        self.assertTrue(old.exists(), "A zero retention period must never purge.")

    def test_disabled_toggle_keeps_answers(self):
        """Answers are never deleted while the cleanup is switched off."""

        # The form's onchange zeroes the retention period when the box is
        # unchecked, so an off cleanup with a retention period only comes from
        # imports or other modules writing the fields directly.
        self.question.answer_retention_enabled = False
        self.question.answer_retention_days = 10
        kept = self._create_answer_line(age_days=400)

        self.question_model._cron_purge_expired_answers()
        self.assertTrue(kept.exists(), "A switched-off cleanup must never purge.")

        # Positive control: the very same answer is purged once the cleanup is
        # armed, so this test cannot pass by the cron being broken altogether.
        self._enable_retention(10)
        self.question_model._cron_purge_expired_answers()
        self.assertFalse(kept.exists(), "Sanity check: the armed cleanup purges.")

    def test_purge_requires_both_toggle_and_days(self):
        """Only a switched-on cleanup with a retention period purges."""

        # The cron gate is the AND of the two fields, so every corner of the
        # table is checked in one place. Each case gets its own question,
        # because the armed corner would otherwise purge another case's answer.
        table = [
            ("switch off, no period", False, 0),
            ("switch off, period slipped in", False, 10),
            ("switch on, no period", True, 0),
            ("switch on, period set", True, 10),
        ]
        for title, enabled, days in table:
            with self.subTest(case=title):
                question = self._create_question(title)
                question.write(
                    {
                        "answer_retention_enabled": enabled,
                        "answer_retention_days": days,
                    }
                )
                answer = self._create_answer_line(age_days=400, question=question)
                cleanup_is_armed = enabled and days > 0

                self.question_model._cron_purge_expired_answers()

                self.assertEqual(
                    bool(answer.exists()),
                    not cleanup_is_armed,
                    "An expired answer must survive unless the cleanup is armed.",
                )

    def test_answer_retention_active(self):
        """The list view flag needs both the toggle and a retention period."""

        self.assertFalse(self.question.answer_retention_active)

        self.question.answer_retention_enabled = True
        self.assertFalse(
            self.question.answer_retention_active,
            "No retention period set yet, so nothing is ever purged.",
        )

        self.question.answer_retention_days = 10
        self.assertTrue(self.question.answer_retention_active)

        self.question.answer_retention_days = 0
        self.assertFalse(
            self.question.answer_retention_active,
            "A zero retention period keeps answers indefinitely.",
        )

    def test_purge_logs_question_not_answer(self):
        """The cleanup note names the question and never the answer itself."""

        self._enable_retention(10)
        self._create_answer_line(age_days=20)

        messages = self._run_cleanup()

        self.assertEqual(len(messages), 1, "One cleanup run leaves one note.")
        self.assertIn(
            self.question.display_name,
            messages.body,
            "The note must say which question was purged.",
        )
        self.assertNotIn(
            "an answer",
            messages.body,
            "Purged answer content must stay out of the chatter.",
        )
        self.assertFalse(
            messages.notification_ids,
            "A cleanup note must not notify anybody.",
        )

    def test_purge_message_escapes_question_title(self):
        """A question title is logged as text, never as markup."""

        self._enable_retention(10)
        self.question.title = "Which <b>vendor</b> do you prefer?"
        self._create_answer_line(age_days=20)

        body = self._run_cleanup().body

        self.assertIn("&lt;b&gt;vendor&lt;/b&gt;", body)
        self.assertNotIn("<b>vendor</b>", body)

    def test_purge_one_message_per_response(self):
        """All questions purged from one response are listed in a single note."""

        other = self._create_question("Second question")
        for question in self.question | other:
            self._enable_retention(10, question)
            self._create_answer_line(age_days=20, question=question)

        notes = self._run_cleanup()

        self.assertEqual(len(notes), 1)
        body = notes.body
        self.assertIn("Text question", body)
        self.assertIn("Second question", body)
        self.assertEqual(
            body.count("Second question"),
            1,
            "Each purged question is named exactly once.",
        )

    def test_purge_names_question_once(self):
        """Several answers to one question are still one line in the note."""

        self._enable_retention(10)
        # Matrix questions store one answer line per row.
        self._create_answer_line(age_days=20)
        self._create_answer_line(age_days=20)

        body = self._run_cleanup().body

        self.assertEqual(body.count("Text question"), 1)

    def test_no_purge_logs_nothing(self):
        """An armed cleanup with nothing expired writes nothing to the chatter."""

        self._enable_retention(10)
        self._create_answer_line(age_days=5)

        self.assertFalse(self._run_cleanup())
