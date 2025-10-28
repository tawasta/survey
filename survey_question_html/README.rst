.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

======================================
Survey: HTML Field Question (CKEditor)
======================================
This module extends Odoo's **Survey** application by introducing a new question type — **HTML field**.  
It allows respondents to answer survey questions using a rich text editor (CKEditor 5), enabling formatted text input (bold, lists, links, etc.) instead of plain text.

This is particularly useful for surveys or forms where participants need to provide long or formatted answers, such as essays, feedback forms, or open-ended text sections.

Features
========
* Adds a new question type **“HTML Field”** to Odoo surveys.
* Integrates **CKEditor 5** for a rich text editing experience.
* Supports full validation for required HTML questions (empty detection even if tags or spaces remain).
* Ensures proper synchronization between the CKEditor and Odoo’s data model.
* Displays submitted HTML answers with formatting preserved in the survey review screen.
* Extends both backend (Python) and frontend (JavaScript + XML) survey logic cleanly through inheritance.

Configuration
=============
No specific configuration is required.

Usage
=====
1. Navigate to **Surveys → Questions**.
2. Create a new question and set its type to **HTML Field**.
3. When a respondent opens the survey, a CKEditor will appear for that question.
4. Responses can include rich formatting.
5. Results are stored as HTML and can be viewed in formatted form in the review screen.

Validation Behavior
-------------------
* Required HTML questions are validated both client-side and server-side.
* The validation logic strips tags and spaces to ensure the field contains actual content before submission.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: http://futural.fi/templates/tawastrap/images/logo.png
        :alt: Futural Oy
        :target: http://futural.fi/

This module is maintained by Futural Oy
