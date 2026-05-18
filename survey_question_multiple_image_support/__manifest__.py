##############################################################################
#
#    Author: Futural Oy
#    Copyright 2026 Futural Oy (www.futural.fi)
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
    "name": "Survey Question Multiple Images Support",
    "version": "14.0.1.2.0",
    "category": "Marketing/Surveys",
    "summary": "Survey question with multiple images",
    "website": "https://gitlab.com/tawasta/odoo/survey",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["survey"],
    "data": [
        "security/ir.model.access.csv",
        "views/survey_templates_print_inherit.xml",
        "views/survey_question_views.xml",
        "views/survey_language_views.xml",
        "views/res_partner_views.xml",
        "views/survey_print_button_views.xml",
        "wizard/survey_wizard_views.xml",
    ],
}
