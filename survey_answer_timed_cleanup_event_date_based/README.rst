.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================================
Survey Answer Timed Cleanup Event Date Based
============================================

* Adds an "Answer Data Retention Basis" radio to survey questions, counting
  the retention period from the event start or end date instead of from when
  the answer was recorded.
* The existing cleanup action of survey_answer_timed_cleanup purges each
  question's answers aged against its selected basis, no separate scheduled
  action needed.

Configuration
=============

* Set "Answer Data Retention (days)" on the questions to purge, as in
  survey_answer_timed_cleanup. Zero or empty keeps the answers indefinitely.
* Choose "Event Start Date" or "Event End Date" as the retention basis;
  "Answer Date" keeps the default behaviour of the base module.
* An event date basis can only purge answers that carry the event link
  ("event_id") stored by society_event_core.
* Activate the scheduled action "Survey: purge expired answer data" from
  survey_answer_timed_cleanup.

Usage
=====
Answers linked to an event are deleted by the cleanup action once the
selected event date is older than the question's retention period. Answers
without an event are never purged by the event date rules (Odoo default behaviour).

Known issues / Roadmap
======================
* Short retention periods can purge feedback survey answers while the survey is
  still being answered, since the countdown starts from the event date.
* Deleting answer lines recomputes the stored scoring and statistics of the
  affected responses, so historical results shift over time.
* If answer attachments are stored by other modules, their files are not removed
  together with the answer line.

Credits
=======

Contributors
------------

* Joonas Lahtinen <joonas.lahtinen@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
