.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

=============================
Survey Question: Model Select
=============================

This module adds a new survey question type called **Odoo Model Dropdown**.

The question allows survey respondents to select a value from records stored in
an Odoo model. Dropdown values are generated automatically from the selected
model and can be filtered using a standard Odoo domain.

Typical use cases include selecting:

* Contacts
* Projects
* Products
* Events
* Custom business records

Configuration
=============

#. Go to *Surveys* and create or edit a survey question.
#. Select **Odoo Model Dropdown** as the question type.
#. Select the source model in **Dropdown Model**.
#. Optionally define a domain in **Condition Domain** to filter records.
#. Set **Maximum Values** if needed.
#. Click **Update Dropdown Values** to generate the available options.

Usage
=====

When the survey is displayed, respondents will see a dropdown field containing
records from the configured Odoo model.

The selected value is stored as a normal survey suggested answer while also
keeping a reference to the originating Odoo record:

* Source Model
* Source Record ID

Administrators can refresh the available dropdown values at any time by using
the **Update Dropdown Values** button on the survey question.

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
