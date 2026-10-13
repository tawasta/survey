.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
Survey Answer Timed Cleanup
============================

* Intended for surveys that collect personal data which must not be kept longer
  than necessary (e.g. GDPR storage limitation).
* Adds an "Answer Data Retention (days)" field to survey questions.
* A scheduled action deletes submitted answers to those questions once they are
  older than the configured retention period.

Configuration
=============
* Open a survey question and set "Answer Data Retention (days)" on the Options
   tab. Empty or zero keeps the answers indefinitely.


Usage
=====
Answers to questions with a retention period are deleted by the scheduled action
once their recorded date is older than that period. Every response is purged,
including unfinished ones, so no answer data outlives its retention window.
The second action wipes all answer data of those questions on demand, with no
time restriction.

Known issues / Roadmap
======================
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
