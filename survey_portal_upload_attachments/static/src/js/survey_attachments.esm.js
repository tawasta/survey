/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { _t } from "@web/core/l10n/translation";
import { getDataURLFromFile } from "@web/core/utils/urls";
import { humanSize } from "@web/core/utils/binary";
import { uniqueId } from "@web/core/utils/functions";
import Dialog from "@web/legacy/js/core/dialog";

const SurveyAttachmentsForm = publicWidget.Widget.extend({
    selector: ".o_portal_wrap",
    events: {
        "click #modal_upload_attachment": "_onClickSubmit",
    },

    start() {
        this.useFileAPI = Boolean(window.FileReader);
        this.file_value = {};
        this._super.apply(this, arguments);
        $(document).on(
            "submit",
            "#survey-attachments-form",
            this._onFormSubmit.bind(this)
        );
    },

    _onClickSubmit(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        const answerId = $(ev.currentTarget).attr("answer-id");
        const answerToken = $(ev.currentTarget).attr("data-token");
        const surveyToken = $(ev.currentTarget).attr("data-survey");

        if (!answerId) {
            console.error("Anwer ID not found.");
            return;
        }

        jsonrpc(`/survey/attachments/${surveyToken}/${answerToken}`, {})
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

                $modal.on("change", ".portal_question_attachment", (e) => {
                    const fileInput = e.target;
                    const maxSizeMB = parseFloat(fileInput.getAttribute("validation-size-max") || "0");
                    const maxSizeBytes = maxSizeMB * 1024 * 1024;

                    if (this.useFileAPI && fileInput.files.length) {
                        const files = Array.from(fileInput.files);
                        const filesList = [];

                        for (const file of files) {
                            if (file.size > maxSizeBytes) {
                                this._showWarning(
                                    _t("Tiedosto on liian suuri"),
                                    _t(
                                        "Valittu liite ylittää suurimman sallitun tiedostokoon (%s)",
                                        human_size(maxSizeBytes)
                                    )
                                );
                                return;
                            }

                            getDataURLFromFile(file).then((data) => {
                                const base64Data = data.split(",")[1];
                                filesList.push({
                                    file_name: file.name,
                                    data: base64Data,
                                });

                                this.file_value[$(fileInput).data("name")] = filesList;
                                this.file_value[$(fileInput).data("name")].is_answer_update = true;
                            });
                        }
                    }
                });

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

    _showWarning(title, message) {
        // Simple browser alert - you can replace with OWL Dialog
        alert(`${title}\n\n${message}`);
    },
});

publicWidget.registry.SurveyAttachmentsForm = SurveyAttachmentsForm;

export default SurveyAttachmentsForm;
