.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

==============
Survey Mailing
==============

* Send emails to survey user inputs' partners using core's mail.compose.message wizard
* Supports using variables in the email templates, i.e. you can send message
  to multiple participants each with message showing fields of their own
  participation record.

Configuration
=============
* Optional: Customize the empty template `survey_mailing.survey_mailing_template`.


Usage
=====
* Go to Survey's Participations list or form view and click Send E-mail
* Select template and send

Known issues / Roadmap
======================
* Note: refactored in 17.0 to call the core email wizard instead of setting up a 
  custom model as was in 14.0. This enables the embedding of user input based
  variables into the templates. Some changes to modules depending on this module
  may still be needed, especially if you need to add additional email recipients.

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>
* Valtteri Lattu <valtteri.lattu@futural.fi>
* Miika Nissi <miika.nissi@tawasta.fi>


Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
        :alt: Oy Tawasta OS Technologies Ltd.
        :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
