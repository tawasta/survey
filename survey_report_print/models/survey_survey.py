# 1. Standard library imports:
# 2. Known third party imports:
# 3. Odoo imports (openerp):
from odoo import api
from odoo import models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SurveySurvey(models.Model):

    # 1. Private attributes
    _inherit = "survey.survey"

    def action_generate_print(self):
        self.ensure_one()

        return self.env.ref(
            "survey_report_print.print_report_action"
        ).report_action(self)
