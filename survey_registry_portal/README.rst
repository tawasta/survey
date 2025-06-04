.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

======================
Survey Registry Portal
======================

* Adds **"Survey Registry"** section to the portal (`/surveys/registry`)
* Portal users can view and search through completed surveys
* Surveys can be searched by respondent name and survey title
* Sorting options:
  * Newest submissions first
  * Respondent name
  * Survey title
* Each survey submission has its own detailed page including:
  * Respondent name
  * Submission date
  * Survey title
  * Detailed answers provided by the respondent
* Integrated neatly within the default Odoo portal layout

- `survey.question` has field `save_as_registry_visibility`
- If a user answers **yes/true/1/kyllä** to such a question, then:
  - `survey.user_input.show_in_registry = True`
- Only those marked `True` are visible in registry
* Also any backend fields of Survey User Input fields can be shown in frontend,
  if you have some info that is e.g. added to custom fields by the administrator after they 
  have checked the survey submission

Configuration
=============
  
- Ensure `survey.user_input` records have a `partner_id` assigned for visibility
- If you wish to show Survey User Input records' backend custom fields in the portal,
  select which ones to show in the "Survey Registry" tab of the survey

Usage
=====

- Go to **Survey Registry** (`/surveys/registry`)  
- Browse or search survey submissions  
- Select a submission to view detailed answers  

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>
* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
        :alt: Oy Tawasta OS Technologies Ltd.
        :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
