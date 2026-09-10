from odoo import _, models
from odoo.tools import format_date, format_datetime


class SurveyUserInputXlsx(models.AbstractModel):
    _inherit = "report.survey_user_input_report_xlsx.user_input_report_xlsx"

    def _write_scored_answers(self, workbook, sheet, question, row):
        """Write a question's title, answer, and score on sheet. Returns the
        next empty row."""
        col = 0
        sheet.write(row, col, question.title, workbook.add_format({"bold": True}))
        col += 1
        sheet.write(row, col, _("Answer"), workbook.add_format({"bold": True}))
        col += 1
        sheet.write(row, col, _("Score"), workbook.add_format({"bold": True}))
        row += 1
        # simple choice / multiple choice / matrix
        if question.suggested_answer_ids:
            for suggested_answer_id in question.suggested_answer_ids:
                col = 1
                sheet.write(row, col, suggested_answer_id.value)
                col += 1
                sheet.write(row, col, suggested_answer_id.answer_score)
                row += 1
        # date / datetime / other unknown type
        elif question.question_type == "date":
            col = 1
            sheet.write(row, col, str(format_date(self.env, question.answer_date)))
            col += 1
            sheet.write(row, col, question.answer_score)
            row += 1
        elif question.question_type == "datetime":
            col = 1
            sheet.write(
                row, col, str(format_datetime(self.env, question.answer_datetime))
            )
            col += 1
            sheet.write(row, col, question.answer_score)
            row += 1
        return row

    def generate_xlsx_report(self, workbook, data, survey_user_inputs):
        res = super().generate_xlsx_report(workbook, data, survey_user_inputs)
        row = 0
        col = 0

        # New sheet for score answers
        sheet = workbook.add_worksheet(_("Survey Answer Scores"))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)

        user_input_fnames = self._get_user_input_fnames()
        surveys = self.env["survey.survey"].search(
            [["user_input_ids", "in", survey_user_inputs.ids]]
        )
        # Write user input field titles
        for fname in user_input_fnames:
            sheet.write(row, col, fname, workbook.add_format({"bold": True}))
            col += 1
        # Write survey question titles
        for survey in surveys:
            for question in survey.question_ids:
                if question.question_type == "matrix":
                    for matrix_row in question.matrix_row_ids:
                        sheet.write(
                            row,
                            col,
                            matrix_row.value,
                            workbook.add_format({"bold": True}),
                        )
                        col += 1
                else:
                    sheet.write(
                        row, col, question.title, workbook.add_format({"bold": True})
                    )
                    col += 1
        row += 1
        col = 0
        # Write a row for each user input
        for user_input in survey_user_inputs:
            # Write user input field values
            for fname in user_input_fnames:
                sheet.write(
                    row,
                    col,
                    self._get_user_input_fname_value(
                        user_input, user_input_fnames[fname]
                    ),
                )
                col += 1
            # Write each question answer score
            for survey in surveys:
                for question in survey.question_ids:
                    if question.question_type == "matrix":
                        for matrix_row in question.matrix_row_ids:
                            answer_list = [
                                str(user_input_line.answer_score)
                                for user_input_line in user_input.user_input_line_ids
                                if user_input_line.question_id == question
                                and user_input_line.matrix_row_id == matrix_row
                            ]
                            sheet.write(row, col, ", ".join(answer_list))
                            col += 1
                    else:
                        answer_list = [
                            str(user_input_line.answer_score)
                            for user_input_line in user_input.user_input_line_ids
                            if user_input_line.question_id == question
                            and question.suggested_answer_ids
                        ]
                        sheet.write(row, col, ", ".join(answer_list))
                        col += 1
            row += 1
            col = 0

        # Scored answers table at the end of sheet
        row += 3
        scored_questions = self.env["survey.question"].search(
            [
                ("survey_id", "in", surveys.ids),
                "|",
                ("is_scored_question", "=", True),
                ("question_type", "=", "matrix"),
            ]
        )
        for question in scored_questions:
            row = self._write_scored_answers(workbook, sheet, question, row)
        return res
