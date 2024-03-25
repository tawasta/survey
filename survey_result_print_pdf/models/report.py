from odoo import api, models

class SurveyPrintReport(models.AbstractModel):
    _name = 'report.survey_result_print_pdf.survey_page_print'
    _description = 'Survey Print Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['survey.survey'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'survey.survey',
            'docs': docs,
        }
