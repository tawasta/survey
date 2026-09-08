.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

==================================
Survey Portal Certificate Download
==================================
* Adds a "Download Certificate" button to the portal survey answers list
* The button is shown for an answer only if:
  * the survey is a certification
  * the user has passed the certification
  * the survey has "Downloadable in Portal" enabled
* The certificate is generated for that exact answer, using the styling selected
  in the survey's "Certification template"


Configuration
=============
* Open a survey and enable "Is a Certification"
* Tick "Downloadable in Portal"
* Pick the wanted "Certification template" style

Usage
=====
* Answer the survey as a portal user
* Go to My Account > Survey Answers
* Click Download Certificate on a passed certification row

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
