.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

======================
Survey Registry Portal
======================

* Adds **"Survey Registry"** section to the portal (`/surveys/registry`)
* Public users can view and search through completed surveys
* Surveys can be searched by respondent name, tags, answer title and survey title
* Sorting options:
  * Newest submissions first
  * Respondent name
  * Survey title
  * Title in survey registry
* Each survey submission has its own detailed page including detailed answers provided by the respondent
* Also any backend fields of Survey User Input fields can be shown in frontend,
  if you have some info that is e.g. added to custom fields by the administrator after they 
  have checked the survey submission

Configuration
=============

* Mark public user input records by checking 'Show Answers in Survey Registry' field
* If you wish to show Survey User Input records' backend custom fields in the portal,
  select which ones to show in the "Survey Registry" tab of the survey
* In the survey questions, 

  * configure one to have the 'Use answer as title in survey registry' checked
  * optionally, configure the 'Show answer in survey registry', to show/hide specific questions as needed
  * optionally, configure one Multiple Choice question to have the 'Use answer as category in survey registry' checked
  * optionally, check 'Answer Controls Registry Visibility' for one question. If a user answers 
    **yes/true/1/kyllä** to such a question, then the user input record will get the 
    field 'Show Answers in Survey Registry' automatically checked.


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
