##############################################################################
#
#    Author: Futural Oy
#    Copyright 2026 Futural Oy (https://futural.fi)
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
    "name": "Survey Answer Timed Cleanup",
    "summary": "Delete survey answers after a per-question or survey-wide "
    "retention period",
    "version": "17.0.1.2.0",
    "category": "Survey",
    "website": "https://github.com/tawasta/survey",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "survey",
    ],
    "data": [
        "data/ir_config_parameter.xml",
        "data/ir_cron.xml",
        "views/survey_question_views.xml",
        "views/survey_survey_views.xml",
    ],
}
