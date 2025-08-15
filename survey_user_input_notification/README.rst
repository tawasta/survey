.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
Survey User Input Notifications
===============================

Odoo module that sends automatic notifications and creates a CRM lead when a new survey answer is submitted.

Features
========
- Adds a new field **Notify partners** on the survey form
- When a new survey answer is marked as done:
  
  - Automatically creates a **crm.lead** with the respondent's information
  - Sends a message with a link to the survey answer to the selected partners
  - Subscribes the selected partners to the newly created lead

Configuration
=============
1. Open any survey in Odoo
2. Set the **Notify partners** field to the partners you want to be notified of new answers
3. When a survey response is marked as done, the module will automatically:
   
   - Create a CRM lead
   - Subscribe and notify the selected partners

Usage
=====
- The survey administrator adds the desired partners to the *Notify partners* field
- When a respondent submits and finalizes their answer, notifications and a CRM lead are created automatically

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Aleksi Savijoki <aleksi.savijoki@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
