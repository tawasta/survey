.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Survey: Share wizard group access
=================================

* Adds the group "Survey: Share and test", so that a user can use the Share and
  Test buttons of a survey without the Surveys / User group:

  * the group is allowed to read the survey field "User responses", which the
    Share wizard needs
  * the group is allowed to create a test answer. Without it the Test button
    ends up in the home page of the website.

Configuration
=============
* Add the group "Survey: Share and test" to the group (or role) of the users,
  in the tab "Inherited".
* The group also needs the access rights to the models of the wizard: Survey
  (read), Survey Invitation Wizard (read, write, create), Survey User Input
  (read, create) and Survey User Input Line (read, create).

Usage
=====
* The group gives access to the field and to the test answer only. The group
  has no record rules of its own, so the access rights and the record rules of
  the user's other groups limit the participations. Without a record rule the
  user can read all the participations.

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

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
