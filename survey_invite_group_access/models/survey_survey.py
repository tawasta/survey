from odoo import fields, models

READER_GROUP = "survey_invite_group_access.group_survey_invite_reader"


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    # Only the groups are changed, the other attributes come from the core field
    user_input_ids = fields.One2many(
        groups=f"survey.group_survey_user,{READER_GROUP}",
    )

    def _check_answer_creation(
        self,
        user,
        partner,
        email,
        test_entry=False,
        check_attempts=True,
        invite_token=False,
    ):
        # The only check of a test answer in core is the Surveys / User group
        if test_entry and user.has_group(READER_GROUP):
            return None
        return super()._check_answer_creation(
            user, partner, email, test_entry, check_attempts, invite_token
        )
