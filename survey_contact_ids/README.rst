.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

===============
Survey Contacts
===============

* Add multiple contacts to view and receive mails from a survey answer.
* Survey contacts have the same access to view and edit survey answers as the owner.
* Invite links are sent via email, and accepted invites automatically grant access.
* Contacts can be added via backend, portal UI, or directly from survey questions.
* Contact list and invite history are shown on the portal survey answer view.
* Integrated modal forms for adding contacts and showing existing invites.

Configuration
=============
\- No additional configuration needed. Simply install the module.

Usage
=====
- Add partners to `contact_ids` in backend (form view of a survey answer).
- Use **Add Contacts** button in the portal to invite new users via email.
- Use **Show Invites** button in the portal to view sent invites and their status.
- Use the survey question flags ("Save as contact name / phone / email") to automatically create contacts via survey answers.
- Supports up to **9 distinct contacts** per answer, via `survey_contact_number`.
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
