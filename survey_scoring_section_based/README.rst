.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================
Survey: section-based scoring
=============================

* Allows Survey passing to depend on Section-specific minimum scores.
* This check is done in addition to the standard passing check of having
  achieved a certain percentage of the whole survey's total maximum score.

Configuration
=============
* When creating a new Survey, set Scoring to be something else than "No Scoring". Afterwards,
  check the "Use Section-specific Score Limits" checkbox that appears.
* Start adding the Sections and Questions. For each section, click the small "i" icon, and
  in the modal window that opens, and fill in the "Section Minimum Score" field.
* For the questions, use the type "Numerical value", check the "Scored" checkbox and set 
  the max points in the "Score" field (e.g. "5")

Usage
=====
* Answer the survey as usual. On the Participation page, the "Quizz passed" checkbox will 
  take into account if the Section-specific minimums were met.
* Additionally, the Participation page shows for each Section what the minimum score was
  and did the participant achieve that score.


Known issues / Roadmap
======================
* Built for a specific use case that uses only questions that are all a) scored and
  2) of type "Numerical value". Other scenarios likely require tweaking of the module.
* UI improvement: in the Survey question view, somehow show each Section's minimum
  score without having to click on the small "i" icon.


Credits
=======

Contributors
------------
* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: https://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
