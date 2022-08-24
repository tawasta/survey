odoo.define("survey_stages.survey", function (require) {
    "use strict";
    var SurveyFormWidget = require("survey.form");

    SurveyFormWidget.include({
        /**
         * Handle keyboard navigation:
         * - 'enter' or 'arrow-right' => submit form
         * - 'arrow-left' => submit form (but go back backwards)
         * - other alphabetical character ('a', 'b', ...)
         *   Select the related option in the form (if available)
         *
         * @param {Event} event
         */
        _onKeyDown: function (event) {
            var keyCode = event.keyCode;

            // Handle Start / Next / Submit
            if (keyCode === 13 || keyCode === 39) {
                // Enter or arrow-right: go Next
                event.preventDefault();
                if (!this.preventEnterSubmit) {
                    if (this.$('button[value="draft"]').length !== 0) {
                        this._submitForm({isFinish: true, isDraft: true});
                    } else {
                        var isFinish = this.$('button[value="finish"]').length !== 0;
                        this._submitForm({isFinish: isFinish});
                    }
                }
            }
            this._super.apply(this, arguments);
        },
        _onSubmit: function (event) {
            event.preventDefault();
            var $target = $(event.currentTarget);
            var options = {};
            if ($target.val() === "draft") {
                options.isFinish = true;
                options.isDraft = true;
                this._submitForm(options);
            } else {
                this._super.apply(this, arguments);
            }
        },

        /**
         * This function will send a json rpc call to the server to
         * - start the survey (if we are on start screen)
         * - submit the answers of the current page
         * Before submitting the answers, they are first validated to avoid latency from the server
         * and allow a fade out/fade in transition of the next question.
         *
         * @param {Array} [options]
         * @param {Integer} [options.previousPageId] navigates to page id
         * @param {Boolean} [options.skipValidation] skips JS validation
         * @param {Boolean} [options.initTime] will force the re-init of the timer after next
         *   screen transition
         * @param {Boolean} [options.isFinish] fades out breadcrumb and timer
         * @param {Boolean} [options.isDraft] sets answer as draft
         * @private
         */
        _submitForm: function (options) {
            var self = this;
            var params = {};
            if (options.previousPageId) {
                params.previous_page_id = options.previousPageId;
            }
            if (options.isDraft) {
                params.isDraft = options.isDraft;
            }
            if (options.isFinish) {
                params.isFinish = options.isFinish;
            }
            var route = "/survey/submit";

            if (this.options.isStartScreen) {
                route = "/survey/begin";
                // Hide survey title in 'page_per_question' layout: it takes too much space
                if (this.options.questionsLayout === "page_per_question") {
                    this.$(".o_survey_main_title").fadeOut(400);
                }
            } else {
                var $form = this.$("form");
                var formData = new FormData($form[0]);

                if (!options.skipValidation) {
                    // Validation pre submit
                    if (!this._validateForm($form, formData)) {
                        return;
                    }
                }

                this._prepareSubmitValues(formData, params);
            }

            // Prevent user from submitting more times using enter key
            this.preventEnterSubmit = true;

            if (this.options.sessionInProgress) {
                // Reset the fadeInOutDelay when attendee is submitting form
                this.fadeInOutDelay = 400;
                // Prevent user from clicking on matrix options when form is submitted
                this.readonly = true;
            }

            var submitPromise = self._rpc({
                route: _.str.sprintf(
                    "%s/%s/%s",
                    route,
                    self.options.surveyToken,
                    self.options.answerToken
                ),
                params: params,
            });
            this._nextScreen(submitPromise, options);
        },
    });
});
