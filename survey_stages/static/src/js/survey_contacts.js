odoo.define("survey_stages.survey_contacts", function (require) {
    "use strict";
    var ajax = require("web.ajax");
    var Widget = require("web.Widget");
    var publicWidget = require("web.public.widget");

    var SurveyContactsForm = Widget.extend({
        /**
         * @override
         */
        start: function () {
            var self = this;
            var res = this._super.apply(this.arguments).then(function () {
                $("#survey_contacts .a-submit")
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
            return ajax
                .jsonRpc($form.attr("action"), "call", post)
                .then(function (modal) {
                    var $modal = $(modal);
                    $modal.modal({backdrop: "static", keyboard: false});
                    $modal.find(".modal-body > div").removeClass("container");
                    $modal.appendTo("body").modal();
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

    publicWidget.registry.SurveyContactsFormInstance = publicWidget.Widget.extend({
        selector: "#survey_contacts",

        /**
         * @override
         */
        start: function () {
            var def = this._super.apply(this, arguments);
            this.instance = new SurveyContactsForm(this);
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

    return SurveyContactsForm;
});
