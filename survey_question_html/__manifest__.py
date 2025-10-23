##############################################################################
#
#    Author: Futural Oy
#    Copyright 2022- Futural Oy (https://futural.fi)
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
    "name": "Survey: HTML Field Question (CKEditor)",
    "version": "17.0.1.0.0",
    "category": "Marketing/Surveys",
    "summary": "Adds a new Survey question type that uses CKEditor 5 (HTML field)",
    "website": "https://github.com/tawasta/survey",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["survey",],
    "data": [
        "views/survey_user_input_views.xml",
        "views/survey_templates.xml",
    ],
    "assets": {
        "survey.survey_assets": [
            "web/static/src/core/utils/**/*.js",
            "https://cdn.ckeditor.com/ckeditor5/36.0.1/classic/ckeditor.js",
            "https://cdn.ckeditor.com/ckeditor5/43.1.0/ckeditor5.css",
            "survey_question_html/static/src/js/survey.esm.js",
            "survey_question_html/static/src/js/scss/survey_html.scss",
        ],
    },
}
