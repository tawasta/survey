/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import Dialog from "@web/legacy/js/core/dialog";
import { _t } from "@web/core/l10n/translation";

const SurveyContactInvite = publicWidget.Widget.extend({
    selector: ".o_portal_wrap",
    events: {
        "click #modal_invite_contacts": "_onClickInvite",
        "click #modal_survey_contact_invites": "_showInvites",
    },

    start: function () {
        this._super.apply(this, arguments);
        $(document).on(
            "submit",
            "#survey_invite_form",
            this._onFormSubmit.bind(this)
        );
    },

    _showInvites: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        const answerId = $(ev.currentTarget).attr("answer-id");
        const answerToken = $(ev.currentTarget).attr("data-token");
        const surveyToken = $(ev.currentTarget).attr("data-survey");

        if (!answerId) {
            console.error("Anwer ID not found.");
            return;
        }

        jsonrpc(`/get/invites/${surveyToken}/${answerToken}`, {})
            .then(function (modalContent) {
                const $modal = $(modalContent);
                $modal.find(".modal-body > div").removeClass("container");
                $modal.appendTo(document.body);
                // eslint-disable-next-line no-undef
                const modalBS = new Modal($modal[0], {
                    backdrop: "static",
                    keyboard: false,
                });
                modalBS.show();

                $modal.on("click", ".btn-close", function () {
                    $modal.remove();
                });
                $modal.on("hidden.bs.modal", function () {
                    $modal.remove();
                });
            })
            .catch(function (err) {
                console.error("Failed to load modal content", err);
            });
    },

    _onClickInvite: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        const answerId = $(ev.currentTarget).attr("answer-id");
        const answerToken = $(ev.currentTarget).attr("data-token");
        const surveyToken = $(ev.currentTarget).attr("data-survey");

        if (!answerId) {
            console.error("Anwer ID not found.");
            return;
        }

        jsonrpc(`/survey/contacts/${surveyToken}/${answerToken}`, {})
            .then(function (modalContent) {
                const $modal = $(modalContent);
                $modal.find(".modal-body > div").removeClass("container");
                $modal.appendTo(document.body);
                // eslint-disable-next-line no-undef
                const modalBS = new Modal($modal[0], {
                    backdrop: "static",
                    keyboard: false,
                });
                modalBS.show();

                $modal.on("click", ".btn-close", function () {
                    $modal.remove();
                });
                $modal.on("hidden.bs.modal", function () {
                    $modal.remove();
                });
            })
            .catch(function (err) {
                console.error("Failed to load modal content", err);
            });
    },

    _onFormSubmit: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();

        const $form = $(ev.currentTarget);
        const actionUrl = $form.attr("action");
        const formData = new FormData($form[0]);
        this._showLoadingScreen();

        $.ajax({
            url: actionUrl,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: (response) => {
                const jsonResponse = JSON.parse(response);

                if (jsonResponse.error) {
                    this._showErrorMessage(jsonResponse.msg);
                } else {
                    this._showSuccessMessage(jsonResponse.msg);
                    $form.closest(".modal").modal("hide");
                }
            },
            error: (err) => {
                console.error("Form submission failed:", err);
                this._showErrorMessage(_t("An unexpected error occurred."));
            },
            complete: () => {
                this._hideLoadingScreen();
            },
        });
    },

    _showSuccessMessage: function (message) {
        new Dialog(this, {
            title: _t("Success"),
            size: "medium",
            $content: $("<div/>").html(message),
            buttons: [
                {
                    text: _t("OK"),
                    close: true,
                    click: function () {
                        location.reload();
                    },
                },
            ],
        }).open();
    },

    _showLoadingScreen: function () {
        const loadingMessage = `
            <div id="loading-screen" style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                z-index: 9999;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #fff;
                font-size: 20px;">
                <div>
                    <div class="spinner-border text-light" role="status"></div>
                    <p>Loading, please wait...</p>
                </div>
            </div>`;
        $("body").append(loadingMessage);
    },

    _hideLoadingScreen: function () {
        $("#loading-screen").remove();
    },

    _showErrorMessage: function (message) {
        alert(`Error: ${message}`);
    },
});

publicWidget.registry.SurveyContactInvite = SurveyContactInvite;

export default SurveyContactInvite;