.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Survey: Share wizard group access
=================================

* Adds the group "Survey: Share wizard reader", which is allowed to read the
  survey field "User responses". The Share wizard of a survey needs it, so a
  user can use the wizard without the Surveys / User group.

Configuration
=============
* Add the group "Survey: Share wizard reader" to the group (or role) of the
  users, in the tab "Inherited".
* The group also needs the access rights to the models of the wizard: Survey
  (read), Survey Invitation Wizard (read, write, create) and Survey User Input
  (read, create).

Usage
=====
* The reader group gives access to the field only. The access rights and the
  record rules of the user still apply to the participations.

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
