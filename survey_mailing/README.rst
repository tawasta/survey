.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

==============
Survey Mailing
==============
This module allows sending emails to survey participants (`survey.user_input`) using a simple wizard interface.
It posts the message into the chatter and sends the message via email to each participant.

Features
========

- Compose a message with subject, HTML body, and attachments
- Automatically fetch default values from a template
- Sends the message as email to each survey participant (`res.partner`)
- Posts the message into the chatter (mail.message) of each survey answer
- Uses `mail.template` to control layout and content
- Works with multi-record selection in `survey.user_input`



Configuration
=============
No special configuration required.  
Optional: Customize the template `survey_mailing.survey_mailing_template`.


Usage
=====
1. Go to **Survey > Answers**
2. Select one or multiple survey answers
3. From the action menu, choose **Send message to user input**
4. Fill in subject, body, attachments, and click **Send**
5. Message is sent by email and saved to chatter

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Miika Nissi <miika.nissi@tawasta.fi>
* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
        :alt: Oy Tawasta OS Technologies Ltd.
        :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
