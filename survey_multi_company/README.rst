.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

====================
Survey Multi Company
====================

Configuration
=============
- No special configuration is required. The module adds a `company_id` field to the following models:
  - survey.question
  - survey.question.answer
  - survey.user_input
  - survey.user_input.line

- These fields are related to the survey or its parts from which the company information is inherited. All fields are `readonly` and `store=True`.

- Access control rules (`ir.rule`) have been updated to enforce multi-company visibility: users can only see records belonging to their company or records without any company.

Usage
=====
- Enables multi-company compatibility for surveys, questions, answers, and user inputs.

- The `company_id` field is shown in the form views of:
  - `survey.question`
  - `survey.user_input`
  - `survey.user_input.line`

- No manual actions are needed – company data is automatically handled and displayed appropriately.


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

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
        :alt: Oy Tawasta OS Technologies Ltd.
        :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
