.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

=====================================
Survey Question Save as Company
=====================================

This module extends the Odoo Survey module to allow saving answers as company details.

Features
========
* Save user's survey answer as related partner's company information.
* Optionally save new contacts to the partner's company.
* Answer options to be saved:
  - Company Name
  - Company Street
  - Company Zip
  - Company City
  - Company Website

Configuration
=============
No additional configuration is needed. You can enable saving fields per question in the Survey settings.

To enable these options:
1. Go to Survey → Questions
2. Select a "Char Box" type question
3. Enable the desired fields:
   - Save as user company name
   - Save as user company street
   - Save as user company zip
   - Save as user company city
   - Save as user company website

Usage
=====
* When users answer a survey, if any of the "Save as company" options are checked, the data is saved to the corresponding partner's company.
* If the company does not exist, a new one is created and linked accordingly.
* If `Attach contacts to company` is enabled in the Survey settings:
  - New contacts created from survey answers will be attached to the parent company.

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
