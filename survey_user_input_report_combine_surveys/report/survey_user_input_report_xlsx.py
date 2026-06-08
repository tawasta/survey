import logging
from datetime import datetime

from odoo import _, fields, models

_logger = logging.getLogger(__name__)


class CombineSurveyUserInputXlsx(models.AbstractModel):
    _name = "report.survey_user_input_report_xlsx.user_input_report_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Combine Survey User Input Rows on Report XLSX"

    def _get_user_input_fnames(self):
        """Returns a dictionary of static fields for report with title and field name"""
        user_input_fnames = {
            _("Survey"): "survey_id",
            _("Partner"): "partner_id",
            _("Created on"): "create_date",
        }
        return user_input_fnames

    def _get_user_input_fname_value(self, user_input, fname):
        """Returns a string value for a corresponding field"""
        value = ""
        if fname == "survey_id":
            value = user_input.survey_id.display_name or ""
        if fname == "partner_id":
            value = user_input.partner_id.name or ""
        if fname == "create_date":
            value = (
                datetime.strftime(
                    fields.Datetime.context_timestamp(self, user_input.create_date),
                    "%-d.%-m.%-Y %-H.%M",
                )
                or ""
            )
        return value

    def generate_xlsx_report(self, workbook, data, survey_user_inputs):
        survey_user_inputs = survey_user_inputs.sorted(
            key=lambda r: r.registration_id.id or r.id
        )
        sheet = workbook.add_worksheet(_("Survey Answers"))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)

        user_input_fnames = self._get_user_input_fnames()
        surveys = self.env["survey.survey"].search(
            [["user_input_ids", "in", survey_user_inputs.ids]]
        )
        col_max_widths = {}
        row = 0

        def write_and_track(row_idx, col_idx, value, cell_format=None):
            display_value = value if value not in (None, "", []) else "-"
            sheet.write(row_idx, col_idx, display_value, cell_format)
            length = len(str(display_value)) if display_value else 0
            col_max_widths[col_idx] = max(col_max_widths.get(col_idx, 0), length)

        headers = self._write_headers(
            sheet, workbook, row, user_input_fnames, surveys, write_and_track
        )
        row += 1

        input_values = self._collect_input_values(
            survey_user_inputs, surveys, user_input_fnames
        )
        self._write_data_rows(sheet, headers, input_values, row, write_and_track)
        self._adjust_column_widths(sheet, col_max_widths)

    # Writes the column headers to the xlsx file and tracks the width of these
    def _write_headers(
        self, sheet, workbook, row, user_input_fnames, surveys, write_and_track
    ):
        headers = []
        col = 0
        bold_format = workbook.add_format({"bold": True})

        _logger.debug("Writing title columns for static fields: %s", user_input_fnames)
        for fname in user_input_fnames:
            write_and_track(row, col, fname, bold_format)
            headers.append((fname, col))
            col += 1

        for survey in surveys:
            _logger.debug(
                "Writing title columns for survey %s questions: %s",
                (survey, survey.question_ids),
            )
            for question in survey.question_ids:
                if question.question_type == "matrix":
                    for matrix_row in question.matrix_row_ids:
                        write_and_track(row, col, matrix_row.value, bold_format)
                        headers.append((matrix_row.value, col))
                        col += 1
                else:
                    write_and_track(row, col, question.title, bold_format)
                    headers.append((question.title, col))
                    col += 1
        return headers

    # Collects the survey answers to a dict. If the same
    # user has answered multiple surveys, then combines all
    # the answers into one dict using the registration_id field.
    # If registration_id is missing, uses survey.user_input id instead.
    def _collect_input_values(self, survey_user_inputs, surveys, user_input_fnames):
        input_values = {}
        for user_input in survey_user_inputs:
            reg_id = user_input.registration_id.id or user_input.id

            if reg_id not in input_values:
                input_values[reg_id] = {}

            # Static fields
            for fname in user_input_fnames:
                value = self._get_user_input_fname_value(
                    user_input, user_input_fnames[fname]
                )
                existing_value = input_values[reg_id].get(fname)

                if fname == "Survey":
                    input_values[reg_id][fname] = (
                        f"{existing_value}, {value}" if existing_value else value
                    )
                elif not existing_value:
                    input_values[reg_id][fname] = value

            # Survey answers
            for survey in surveys:
                for question in survey.question_ids:
                    if question.question_type == "matrix":
                        for matrix_row in question.matrix_row_ids:
                            answer_list = [
                                line.string_answer or ""
                                for line in user_input.user_input_line_ids
                                if line.question_id == question
                                and line.matrix_row_id == matrix_row
                            ]
                            value = ", ".join(answer_list)
                            key = matrix_row.value
                            if (
                                key not in input_values[reg_id]
                                or not input_values[reg_id][key]
                            ):
                                input_values[reg_id][key] = value
                    else:
                        answer_list = [
                            line.string_answer or ""
                            for line in user_input.user_input_line_ids
                            if line.question_id == question
                        ]
                        value = ", ".join(answer_list)
                        key = question.title
                        if (
                            key not in input_values[reg_id]
                            or not input_values[reg_id][key]
                        ):
                            input_values[reg_id][key] = value
        return input_values

    # Writes the survey answers, one row per one user
    def _write_data_rows(
        self, sheet, headers, input_values, start_row, write_and_track
    ):
        row = start_row
        for __, answers in input_values.items():
            for header_name, header_col in headers:
                if header_name in answers:
                    write_and_track(row, header_col, answers[header_name])
            row += 1

    # Adjusts the columns to fit the answers/headers,
    # max width set to 50.
    def _adjust_column_widths(self, sheet, col_max_widths):
        for c, width in col_max_widths.items():
            sheet.set_column(c, c, min(width + 2, 50))
