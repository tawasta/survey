.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

======================
Survey Registry Portal
======================

* Adds a **"Survey Registry"** section to the website (`/surveys/registry`)
* Public users can view and search through completed surveys' answers
* Each survey submission has its own detailed page including detailed answers provided by the respondent
* You can customize per question if their answers should be shown in the public registry
* Also, any backend fields of Survey User Input records can be shown in the registry,
  if you have some info that is e.g. added to custom fields by the administrator after they 
  have checked the survey submission.

Configuration
=============

* Mark public user input records by checking 'Show Answers in Survey Registry' field
* If you wish to show Survey User Input records' backend custom fields in the portal,
  select which ones to show in the "Survey Registry" tab of the survey
* In the survey questions, 

  * configure one to have the 'Use answer as title in survey registry' checked
  * configure the 'Show answer in survey registry', to show/hide specific questions as needed
  * optionally, depending on your set of questions: 
  
     * configure one Multiple Choice question to have the 'Use answer as Category in survey registry' checked
     * configure one text-based question to have the 'Use answer as Schedule in survey registry' checked
     * configure one text-based question to have the 'Use answer as Implementer Organization in survey registry' checked
     * configure one text-based question to have the 'Use answer as Other Implementers in survey registry' checked
     * optionally, check 'Answer Controls Registry Visibility' for one question. If a user answers 
       **yes/true/1/kyllä** to such a question, then the user input record will get the 
       field 'Show Answers in Survey Registry' automatically checked.


Usage
=====

* Go to `/surveys/registry` to browse the registry


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
