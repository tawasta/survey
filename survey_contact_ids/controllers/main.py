##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:
import logging

from werkzeug import exceptions

# 3. Odoo imports (openerp):
from odoo import _, http
from odoo.exceptions import AccessError
from odoo.http import request

# 4. Imports from Odoo modules:
from odoo.addons.auth_signup.models.res_partner import SignupError
from odoo.addons.base.models.ir_mail_server import MailDeliveryException
from odoo.addons.survey.controllers.main import Survey

# 2. Known third party imports:


# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class SurveyContacts(Survey):
    def _check_validity(
        self, survey_token, answer_token, ensure_token=True, check_partner=True
    ):
        """
        Override to check for contact_ids instead of partner_id
        """
        res = super(SurveyContacts, self)._check_validity(
            survey_token, answer_token, ensure_token, check_partner
        )
        if res == "answer_wrong_user":
            survey_sudo, answer_sudo = self._fetch_from_access_token(
                survey_token, answer_token
            )
            if (
                not request.env.user._is_public()
                and request.env.user.partner_id in answer_sudo.contact_ids
            ):
                return True
        return res

    def _create_or_get_signup_user(self, partner_values):
        """Find existing user by email. If no user exists then create a new user.

        :param dict partner_values: dictionary of values for partner
        :return res.users user: new or existing user
        """
        user = (
            request.env["res.users"]
            .sudo()
            .search([("login", "=ilike", partner_values.get("email"))])
        )
        # If no user exists. Create a new user.
        if not user:
            if not partner_values.get("login") and partner_values.get("email"):
                partner_values["login"] = partner_values.get("email")
            try:
                user = (
                    request.env["res.users"].sudo()._signup_create_user(partner_values)
                )
                _logger.info(_("Created a new user %s.") % user)
            except SignupError as err:
                raise AccessError(
                    _("Signup is not allowed for uninvited users.")
                ) from err
            try:
                user.with_context(**{"create_user": True}).action_reset_password()
            except MailDeliveryException:
                _logger.warning(
                    _("Could not deliver mail to %s") % partner_values.get("email")
                )
        return user

    def _names_order_default(self):
        return "first_last"

    def _get_names_order(self):
        """Get names order configuration from system parameters.
        You can override this method to read configuration from language,
        country, company or other"""
        return (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("partner_names_order", self._names_order_default())
        )

    def _get_name(self, lastname, firstname):
        order = self._get_names_order()
        if order == "last_first_comma":
            return ", ".join(p for p in (lastname, firstname) if p)
        elif order == "first_last":
            return " ".join(p for p in (firstname, lastname) if p)
        else:
            return " ".join(p for p in (lastname, firstname) if p)

    @http.route(
        "/survey/contacts/<string:survey_token>/<string:answer_token>",
        type="json",
        auth="public",
        methods=["POST"],
        website=True,
        sitemap=False,
    )
    def survey_contacts(self, survey_token, answer_token, **post):
        """Contacts to survey modal"""
        # Get the current answer token from cookie
        answer_from_cookie = False
        if not answer_token:
            answer_token = request.httprequest.cookies.get("survey_%s" % survey_token)
            answer_from_cookie = bool(answer_token)

        access_data = self._get_access_data(
            survey_token, answer_token, ensure_token=False, check_partner=False
        )

        if answer_from_cookie and access_data["validity_code"] in (
            "answer_wrong_user",
            "token_wrong",
        ):
            # If the cookie had been generated for another user or does not correspond
            # to any existing answer object (probably because it has been deleted),
            # ignore it and redo the check. The cookie will be replaced by a legit
            # value when resolving the URL, so we don't clean it further here.
            access_data = self._get_access_data(survey_token, None, ensure_token=False)

        if access_data["validity_code"] is not True:
            return self._redirect_with_error(access_data, access_data["validity_code"])

        answer_sudo = access_data["answer_sudo"]

        if answer_sudo and request.env.user.partner_id in answer_sudo.contact_ids:
            return (
                request.env["ir.ui.view"]
                .sudo()
                ._render_template(
                    "survey_contact_ids.survey_contacts_modal",
                    {
                        "answer_token": answer_token,
                        "survey_token": survey_token,
                        "answer": answer_sudo,
                    },
                )
            )

    @http.route(
        ["""/survey/contacts/<string:survey_token>/<string:answer_token>/post"""],
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def survey_contacts_post(self, survey_token, answer_token, **post):
        """Add contacts to survey"""
        answer_from_cookie = False
        if not answer_token:
            answer_token = request.httprequest.cookies.get("survey_%s" % survey_token)
            answer_from_cookie = bool(answer_token)
        access_data = self._get_access_data(
            survey_token, answer_token, ensure_token=False, check_partner=False
        )

        if answer_from_cookie and access_data["validity_code"] in (
            "answer_wrong_user",
            "token_wrong",
        ):
            # If the cookie had been generated for another user or does not correspond
            # to any existing answer object (probably because it has been deleted),
            # ignore it and redo the check. The cookie will be replaced by a legit
            # value when resolving the URL, so we don't clean it further here.
            access_data = self._get_access_data(survey_token, None, ensure_token=False)

        if access_data["validity_code"] is not True:
            return self._redirect_with_error(access_data, access_data["validity_code"])

        answer_sudo = access_data["answer_sudo"]
        if answer_sudo and request.env.user.partner_id in answer_sudo.contact_ids:
            # Create invitation link for answer
            email = post.get("email")
            survey_invite = request.env["survey.user.invite"].create(
                {
                    "survey_user_input_id": answer_sudo.id,
                    "email": email,
                }
            )
            _logger.info(
                "Created invitation link {} for email {} for answer {}".format(
                    survey_invite.id,
                    email,
                    answer_sudo.id,
                )
            )
        return request.redirect("/my/surveys/%d" % answer_sudo.id)

    @http.route(
        ["/survey/invite/code/<string:code>"],
        type="http",
        auth="user",
        website=True,
    )
    def survey_invite_accept(self, code):
        """
        Accept invitation code

        :param code: uuid4
        :return: exception|redirect
        """
        user = request.env.user
        invitation = (
            request.env["survey.user.invite"]
            .sudo()
            .search(
                [
                    ("code", "=", code),
                    ("user_id", "=", False),
                ]
            )
        )
        if not invitation:
            # Code doesn't exist or already used
            raise exceptions.Forbidden()

        invitation.survey_user_input_id.message_subscribe(
            partner_ids=[user.partner_id.id]
        )
        invitation.survey_user_input_id.write(
            {"contact_ids": [(4, user.partner_id.id)]}
        )
        invitation.user_id = user.id
        _logger.info(
            "Added a new contact {} to answer {}.".format(
                user.partner_id.id, invitation.survey_user_input_id.id
            )
        )
        return request.redirect(
            "/my/surveys/{}".format(invitation.survey_user_input_id.id)
        )
