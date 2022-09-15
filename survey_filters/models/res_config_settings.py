from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    use_user_filter = fields.Boolean(
        string="Survey: use the user filter in the survey result view",
        config_parameter="survey.filter.user",
    )

    use_date_filter = fields.Boolean(
        string="Survey: use the date filter in the survey result view",
        config_parameter="survey.filter.date",
    )

    module_society_event_core = fields.Boolean(string="Use event")

    use_event_filter = fields.Boolean(
        string="Survey: use the event filter in the survey result view",
        config_parameter="survey.filter.event",
    )
