.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================
Survey Payment Link
===================
This module links survey user inputs (projects, grants, etc.) with accounting payments in Odoo.

Features
--------

- **Two-way relation** between `survey.user_input` and `account.payment`
    - `account.payment.survey_user_input_id`: Points to the related survey user input.
    - `survey.user_input.payment_ids`: Lists all payments related to the survey input.

- **Create Payment** button in `survey.user_input` form view:
    - Opens the payment form pre-filled with relevant data (partner, type, etc.).
    - The link to the survey is created automatically upon saving.

- **New "Payments" tab** on the survey user input form:
    - Shows all payments related to the response.
    - Allows quick access and management of financial records related to a survey-based project.

- **Survey link visible on the payment form**:
    - Quick traceability from the accounting side to the project/grant that the payment is associated with.

Usage
-----

1. Navigate to **Surveys > Participations (User Inputs)**.
2. Open any record (e.g. a project or application).
3. Use the **Payments** tab to:
    - View existing linked payments.
    - Create a new payment using the *Create Payment* button.
4. When a new payment is created, the link to the survey input is pre-filled.
5. From the **Accounting > Payments** screen, the payment record shows the linked survey input.


Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: http://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: http://futural.fi/

This module is maintained by Futural Oy
