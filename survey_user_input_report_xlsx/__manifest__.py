##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
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
{
    "name": "Survey User Input Report XLSX",
    "version": "14.0.1.1.0",
    "category": "Marketing/Surveys",
    "summary": "Print an xlsx report from survey user inputs",
    "website": "https://gitlab.com/tawasta/odoo/survey",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": ["xlsxwriter"]},
    "depends": ["survey_string_answer", "report_xlsx"],
    "data": [
        "report/survey_user_input_report_xlsx.xml",
    ],
}
