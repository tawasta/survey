.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

=====================================================
Survey Participation: Funding Application Base Fields
=====================================================

* Adds basic backend fields for when survey participations are used for collecting funding applications
* The fields are intended to be updated by the internal users managing the applications, not
  the applicants answering the survey.
* Also installs as a dependency survey_payment_link, so account.payment records can be used for tracking
  how much of the funding has actually been paid out

Configuration
=============
* None needed

Usage
=====
* Survey participation form contains the new fields in a new notebook tab

Known issues / Roadmap
======================
* Make configurable if draft payments should be taken into account or not when showing how much of
  funding has been paid out.

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
        :alt: Oy Tawasta OS Technologies Ltd.
        :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
