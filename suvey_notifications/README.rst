.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

================================
Survey File Upload Notifications
================================
This module adds automatic notifications when files are uploaded to surveys, either through portal answers, backend chatter, or during final submission.

It enhances the survey app by notifying selected users when:
- A respondent uploads files during survey filling
- A user attaches files via the survey response form's chatter
- A survey response is submitted (if enabled)

It uses email templates to notify selected users configured on each survey.

Configuration
=============

1. Go to **Surveys > Survey** and open a survey form.
2. In the *Notifications* section (new tab or group), configure:
   - **Notification Users**: Users who will receive email notifications.
   - **Notify on File Upload**: Enable to send notifications when attachments are uploaded.
   - **Notify on Response Submission**: Enable to send notifications when responses are submitted.

3. Email templates must be available:
   - `mail_template_survey_file_upload`
   - `mail_template_survey_response_submission`

   These are provided by this module.

Usage
=====

**1. File Upload During Portal Survey Fill**

- When a portal user uploads files via a survey form (e.g., `attachment` question types), the system sends a notification email to configured users.

**2. File Upload via Backend Chatter**

- When an internal user uploads an attachment to a survey response (e.g., via chatter), notifications are sent to the configured users.

**3. On Response Submission**

- If enabled, the system sends a summary email to the notification users when a response is marked as *done* or submitted.

**Email Content**

- Includes:
  - The name of the respondent and their organization
  - The uploaded file names
  - The reference to the response (e.g., application ID)
  - The survey title


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

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
        :alt: Oy Tawasta OS Technologies Ltd.
        :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
