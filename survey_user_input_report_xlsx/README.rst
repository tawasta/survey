.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

=============================
Survey User Input Report XLSX
=============================
* Print an xlsx report from survey user inputs
* Report follows format:
    - First few columns are field data from survey.user_input followed by all survey
      questions (can be multiple surveys in one report) (Matrix questions get their own
      column for each row)

Configuration
=============
\-

Usage
=====
\-

Known issues / Roadmap
======================
* When getting reports for event attendees (society_event_core), each attendee can have
  multiple survey answers (ie. basic information survey, allergy information survey) -
  In this case attendees will have multiple rows in XLSX report. Find a way to combine
  these in one row.

Credits
=======

Contributors
------------

* Miika Nissi <miika.nissi@futural.fi>

Maintainer
----------

.. image:: http://futural.fi/templates/tawastrap/images/logo.png
        :alt: Futural Oy
        :target: http://futural.fi/

This module is maintained by Futural Oy
