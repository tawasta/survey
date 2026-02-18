##############################################################################
#
#    Author: Futural Oy
#    Copyright 2026- Futural Oy (https://futural.fi)
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
    "name": "Survey Question: Show Only for Specific Event Ticket",
    "summary": "Add option for showing question only for event surveys where "
    "participant is buying a specific ticket",
    "version": "17.0.1.0.0",
    "category": "Marketing/Surveys",
    "website": "https://github.com/tawasta/survey",
    "author": "Futural",
    "license": "AGPL-3",
    "depends": [
        "society_event_core",
    ],
    "data": ["views/survey_question_views.xml", "views/event_templates.xml"],
    "application": False,
    "installable": True,
}
