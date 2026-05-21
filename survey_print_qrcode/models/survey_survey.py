import base64
import io
import logging

import qrcode

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    qr_code = fields.Binary(
        string="QR Code",
        compute="_compute_qr_code",
        store=True,
        readonly=True,
    )

    @api.depends("title")
    def _compute_qr_code(self):
        for record in self:
            try:
                base_url = (
                    self.env["ir.config_parameter"].sudo().get_param("web.base.url")
                )
                url = (
                    f"{base_url}/web#id={record.id}&model=survey.survey&view_type=form"
                )

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=8,
                    border=2,
                )
                qr.add_data(url)
                qr.make(fit=True)
                img = qr.make_image()

                buf = io.BytesIO()
                img.save(buf, format="PNG")
                record.qr_code = base64.b64encode(buf.getvalue())
            except Exception as e:
                _logger.exception(
                    "QR code generation failed for survey %s: %s", record.id, e
                )
                record.qr_code = False
