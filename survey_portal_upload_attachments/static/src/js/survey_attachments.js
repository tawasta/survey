odoo.define("survey_portal_upload_attachments.survey_attachments", function (require) {
    "use strict";
    var ajax = require("web.ajax");
    var Widget = require("web.Widget");
    var publicWidget = require("web.public.widget");
    var utils = require("web.utils");
    var core = require("web.core");
    var _t = core._t;

    var SurveyAttachmentsForm = Widget.extend({
        /**
         * @override
         */
        start: function () {
            var self = this;
            var res = this._super.apply(this.arguments).then(function () {
                $("#survey_attachments .a-submit")
                    .off("click")
                    .click(function (ev) {
                        self.on_click(ev);
                    });
            });
            return res;
        },

        // --------------------------------------------------------------------------
        // Handlers
        // --------------------------------------------------------------------------
        /**
         * @private
         * @param {Event} ev
         * @returns {ajax} ajax
         */
        on_click: function (ev) {
            ev.preventDefault();
            ev.stopPropagation();
            var $form = $(ev.currentTarget).closest("form");
            var $button = $(ev.currentTarget).closest('[type="submit"]');
            var post = {};
            $button.attr("disabled", true);
            var self = this;
            self.useFileAPI = Boolean(window.FileReader);
            self.file_value = {};
            if (!self.useFileAPI) {
                self.fileupload_id = _.uniqueId("o_fileupload");
                $(window).on(self.fileupload_id, function () {
                    var args = [].slice.call(arguments).slice(1);
                    self.on_file_uploaded.apply(self, args);
                });
            }
            return ajax
                .jsonRpc($form.attr("action"), "call", post)
                .then(function (modal) {
                    var $modal = $(modal);
                    $modal.modal({backdrop: "static", keyboard: false});
                    $modal.find(".modal-body > div").removeClass("container");
                    $modal.appendTo("body").modal();

                    // Validate and save attachment to file_value
                    $modal.on("change", ".portal_question_attachment", function (e) {
                        var file_node = e.target;
                        var files_list = [];
                        var validation_size_max =
                            e.target.getAttribute("validation-size-max") * 1024 * 1024;
                        if (
                            (self.useFileAPI && file_node.files.length) ||
                            (!self.useFileAPI && $(file_node).val() !== "")
                        ) {
                            if (self.useFileAPI) {
                                var files = file_node.files;
                                for (const file of files) {
                                    if (file.size > validation_size_max) {
                                        var msg = _t(
                                            "The selected attachment exceed the maximum file size of %s."
                                        );
                                        self.do_warn(
                                            _t("File upload"),
                                            _.str.sprintf(
                                                msg,
                                                utils.human_size(validation_size_max)
                                            )
                                        );
                                        return false;
                                    }
                                    utils
                                        .getDataURLFromFile(file)
                                        .then(function (data) {
                                            data = data.split(",")[1];
                                            files_list.push({
                                                file_name: file.name,
                                                data: data,
                                            });
                                        });
                                    self.file_value[
                                        $(file_node).data("name")
                                    ] = files_list;
                                    self.file_value[
                                        $(file_node).data("name")
                                    ].is_answer_update = true;
                                }
                            }
                        }
                    });

                    // Hide modal on event
                    $modal.on("click", ".js_goto_event", function () {
                        $modal.modal("hide");
                        $button.prop("disabled", false);
                    });
                    // Hide modal on cancel
                    $modal.on("click", ".close-modal", function () {
                        $modal.modal("hide");
                        $button.prop("disabled", false);
                    });

                    // Remove review form modal once it's hidden
                    $modal.on("hidden.bs.modal", function (e) {
                        // Fixes scrolling if another modal remains open
                        if ($(".modal.show").length > 0) {
                            $("body").addClass("modal-open");
                        }
                        if (this === e.target) {
                            this.remove();
                        }
                    });

                    // Enable tooltips with no delay
                    $(document).ready(function () {
                        $("body").tooltip({
                            selector: "[data-toggle=tooltip]",
                            delay: {show: 0, hide: 0},
                        });
                    });
                });
        },
    });

    publicWidget.registry.SurveyAttachmentsFormInstance = publicWidget.Widget.extend({
        selector: "#survey_attachments",

        /**
         * @override
         */
        start: function () {
            var def = this._super.apply(this, arguments);
            this.instance = new SurveyAttachmentsForm(this);
            return Promise.all([def, this.instance.attachTo(this.$el)]);
        },
        /**
         * @override
         */
        destroy: function () {
            this.instance.setElement(null);
            this._super.apply(this, arguments);
            this.instance.setElement(this.$el);
        },
    });

    return SurveyAttachmentsForm;
});
