.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
Survey Answer Timed Cleanup
============================

* Intended for survey questions that collect personal data which must not be kept longer
  than necessary
* Adds an "Answer Data Retention (days)" field to survey questions.
* A scheduled action deletes submitted answers to those questions once they are
  older than the configured retention period.

Configuration
=============

* Check "Enable Answer Data Retention" on the questions whose answers must be
  purged and set "Answer Data Retention (days)". A question without a retention
  period keeps its answers indefinitely.
* Activate the scheduled action "Survey: purge expired answer data".

Usage
=====
Answers to questions with a retention period are deleted by the scheduled action
once their recorded date is older than that period. The answers are gone
permanently and cannot be recovered afterwards.

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
