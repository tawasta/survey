.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================================
Survey: Invite Sender's E-mail from E-mail Template
===================================================

* By default the survey's "Share" dialog pulls the sender's e-mail
  address from the current user and bypasses e-mail templates
* With this module the sender e-mail is primarily
  pulled from the e-mail template's "From" field, and if that has not
  been set, only then from the current user

Configuration
=============
* Configure the email template (usually "Survey: Invite") and set its
  "From" field. Note: jinja expressions are not supported, must be an
  actual e-mail address.

Usage
=====
* Send an e-mail with the wizard, and the mail's sender now matches
  the template's "From" field.

Known issues / Roadmap
======================
* None

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
