.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

====================================
Survey User Input Reference Sequence
====================================
This Odoo module adds a unique reference code to each survey answer
(`survey.user_input`) using a sequence, similar to how Sales Orders
or Invoices are identified.

This is particularly useful when survey answers are treated as formal
applications — the reference can be used as an *application number*
for tracking and communication purposes.

Features
========

- Adds a `ref` field to `survey.user_input`, generated from a sequence (`REF/YYYY/xxxxx`)
- Reference is automatically generated upon:
  
  - Record creation
  - Duplication (copy)
- Reference is visible in:
  
  - Backend form, tree, kanban, and search views
  - Public survey header (if enabled)
  - Survey PDF printout
- New boolean field `show_survey_answer_ref` added to `survey.survey` to control visibility of reference in public view


Configuration
=============
No additional configuration is required after module installation.

To control public visibility of the reference:

- Navigate to *Surveys* > select a survey
- Enable or disable **"Show Survey Answer Reference"** as needed

Usage
=====
When users fill out a survey, a unique reference will be generated
automatically. This reference can be used for communication, filtering,
or tracking survey submissions.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Miika Nissi <miika.nissi@tawasta.fi>
* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
        :alt: Oy Tawasta OS Technologies Ltd.
        :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
