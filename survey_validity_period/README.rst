.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
Survey: period of qualification
===============================

* It's possible to specify for the Survey whether this increases the qualification or not and how many days it generates the qualification.
* If the survey gives a qualification, then when the answer is accepted in the confirm state, the start date and end date are saved in the record.
* Add a cron that checks if the qualification is about to expire and has expired.
* If it's about to run out, a reminder message is sent to the person, through which they can apply for the qualification again.
* At the same time, the status of the record is returned to draft status.
* If the qualification has ended, the record is moved to the state ended and a message is sent to the user.

Configuration
=============
\-

Usage
=====
\-

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@tawasta.fi>

Maintainer
----------

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: https://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
