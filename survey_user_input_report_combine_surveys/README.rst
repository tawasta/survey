.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

========================================
Survey User Input Report Combine surveys
========================================
* Print an xlsx report from survey user inputs
* Report follows format:
    - Checks all the surveys the user has answered (there can be 3 surveys on the event -> user has answered 3 surveys)
    - Users' survey answers (survey.user_input recs) are combined based on the registration_id
    - All questions from all surveys are written as the column headers
    - Answers of one user are written on a singular row, no matter how many surveys
    - Columns widths are adjusted and empty cells are replaced with "-"

Configuration
=============
\-

Usage
=====
* Install the module, overrides the survey_user_input_report_xlsx

Known issues / Roadmap
======================

Credits
=======

Contributors
------------

* Kalle Rantalainen <kalle.rantalainen@futural.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
        :alt: Oy Tawasta OS Technologies Ltd.
        :target: http://tawasta.fi/

This module is maintained by Futural Oy.
