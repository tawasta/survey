.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
Survey Answer Renderer
======================

This Odoo module extends the survey functionality by providing methods to render survey questions and user answers into HTML format. It allows easy embedding of survey results in emails or web pages with clean and formatted output.

Configuration
=============
No additional configuration is needed. Simply install the module and use the provided methods.

Usage
=====
- Use the `render_answers_html()` method on a `survey.user_input` record to get all questions and answers as an HTML string.
- Each answer is rendered with question title and formatted answer.

Example of embedding in an email template:

```xml
<div>
    <h4>Your Answers:</h4>
    <t t-raw="object.render_answers_html()"/>
</div>

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
