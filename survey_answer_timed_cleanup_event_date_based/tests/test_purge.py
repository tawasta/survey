from datetime import timedelta

from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged("at_install")
class TestAnswerPurgeEventDate(TransactionCase):
    """Test purging event survey answers aged against the event dates."""

    def setUp(self):
        super().setUp()

        self.question_model = self.env["survey.question"]
        self.survey = self.env["survey.survey"].create({"title": "Event survey"})
        self.question = self.env["survey.question"].create(
            {
                "survey_id": self.survey.id,
                "title": "Text question",
                "question_type": "text_box",
            }
        )

    def _create_event(self, begin_days_ago=0, end_days_ago=None):
        """Create an event whose dates are the given days in the past."""

        now = fields.Datetime.now()
        date_begin = now - timedelta(days=begin_days_ago)
        if end_days_ago is None:
            date_end = date_begin + timedelta(hours=1)
        else:
            date_end = now - timedelta(days=end_days_ago)
        return self.env["event.event"].create(
            {
                "name": "Test event",
                "date_begin": date_begin,
                "date_end": date_end,
            }
        )

    def _create_answer_line(self, event=False, age_days=0):
        """Create an answer line, optionally linked to an event and backdated."""

        user_input = self.env["survey.user_input"].create(
            {
                "survey_id": self.survey.id,
                "event_id": event.id if event else False,
            }
        )
        line = self.env["survey.user_input.line"].create(
            {
                "user_input_id": user_input.id,
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

    def test_retention_date_field_mapping(self):
        """Each retention basis maps to the expected date field."""

        self.assertEqual(self.question._get_retention_date_field(), "create_date")
        self.question.answer_retention_date_basis = "start"
        self.assertEqual(
            self.question._get_retention_date_field(), "event_id.date_begin"
        )
        self.question.answer_retention_date_basis = "end"
        self.assertEqual(self.question._get_retention_date_field(), "event_id.date_end")
        # Questions created before this module have an empty basis.
        self.question.answer_retention_date_basis = False
        self.assertEqual(self.question._get_retention_date_field(), "create_date")

    def test_purge_by_event_start_date(self):
        """Answers of past events are purged, upcoming and eventless kept."""

        self.question.answer_retention_days = 10
        self.question.answer_retention_date_basis = "start"
        expired = self._create_answer_line(self._create_event(begin_days_ago=20))
        recent = self._create_answer_line(self._create_event(begin_days_ago=-5))
        without_event = self._create_answer_line()

        self.question_model._cron_purge_expired_answers()

        self.assertFalse(expired.exists(), "Answer of a past event must be purged.")
        self.assertTrue(recent.exists(), "Answer of an upcoming event must be kept.")
        self.assertTrue(without_event.exists(), "Answer without an event must be kept.")

    def test_purge_by_event_end_date(self):
        """Only the event end date governs the retention with the end basis."""

        self.question.answer_retention_days = 10
        self.question.answer_retention_date_basis = "end"
        expired = self._create_answer_line(
            self._create_event(begin_days_ago=20, end_days_ago=20)
        )
        kept = self._create_answer_line(
            self._create_event(begin_days_ago=20, end_days_ago=5)
        )

        self.question_model._cron_purge_expired_answers()

        self.assertFalse(expired.exists(), "Answer of a past event must be purged.")
        self.assertTrue(kept.exists(), "Answer of a recent event must be kept.")

    def test_event_basis_not_purged_by_answer_date(self):
        """An old create_date must not purge answers of an event-basis question."""

        self.question.answer_retention_days = 10
        self.question.answer_retention_date_basis = "start"
        # An answer recorded long ago for an event that has not started yet.
        line = self._create_answer_line(
            self._create_event(begin_days_ago=-5), age_days=20
        )

        self.question_model._cron_purge_expired_answers()

        self.assertTrue(line.exists(), "Upcoming event's answer must be kept.")

    def test_purge_all_includes_event_basis(self):
        """The purge-all action covers event-date-based questions too."""

        self.question.answer_retention_days = 10
        self.question.answer_retention_date_basis = "start"
        line = self._create_answer_line(self._create_event(begin_days_ago=-5))

        self.question_model._cron_purge_all_answers()

        self.assertFalse(line.exists(), "Answer must be purged by the purge-all run.")
