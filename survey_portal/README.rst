.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

=============
Survey Portal
=============
* Adds **"Survey Answers"** section to the portal (`/my/surveys`)
* Portal users can view and review their own submitted surveys
* Each answer has its own detail page, including:
  * Survey title
  * Submission date
  * Reference (if enabled)
  * Partner info
  * Button to re-open the survey in review mode
* Adds **chatter to portal view**, allowing users to send messages
* Survey answers are visible only if linked to the logged-in user's partner (`partner_id`)
* After submission, a **"View in Portal"** button is added to the thank-you screen and PDF view
  * This can be toggled on/off in backend survey form.


Configuration
=============
\- No additional configuration is required  
\- Make sure `survey.user_input` has a `partner_id` assigned

Usage
=====
\- Log in as a portal user  
\- Go to **My Account > Survey Answers**  
\- Browse your submitted survey responses  
\- Open a submission to review answers and view history  
\- Use the message thread (chatter) if available

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Miika Nissi <miika.nissi@tawasta.fi>
* Valtteri Lattu <valtteri.lattu@futural.fi>
* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
        :alt: Oy Tawasta OS Technologies Ltd.
        :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
