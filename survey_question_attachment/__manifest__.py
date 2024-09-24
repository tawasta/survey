##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
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
    "name": "Survey: 'Attachment' question type",
    "version": "17.0.1.0.0",
    "category": "Marketing/Surveys",
    "summary": "Adds a new question type 'attachment' to survey",
    "website": "https://gitlab.com/tawasta/odoo/survey",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["survey", "survey_string_answer", "web_content_link_url"],
    "data": [
        "views/survey_question_views.xml",
        "views/survey_user_input_views.xml",
        "views/survey_templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            'survey_question_attachment/static/src/css/survey_result.css"',
        ],
        "survey.survey_assets": [
            "web/static/src/core/utils/**/*.js",
            "survey_question_attachment/static/src/css/survey_result_frontend.css",
            "survey_question_attachment/static/src/js/survey.esm.js",
        ],
    },
}
