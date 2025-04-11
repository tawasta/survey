/** @odoo-module **/

import SurveyFormWidget from "@survey/js/survey_form";

SurveyFormWidget.include({
    /**
     * Override _onKeyDown to handle "draft" submit
     */
    _onKeyDown: function (event) {
        const keyCode = event.keyCode;
        console.log("=====KEYCODE======");
        console.log(keyCode);
        if (keyCode === 13 || keyCode === 39) {
            event.preventDefault();

            if (!this.preventEnterSubmit) {
                if (this.$('button[value="draft"]').length !== 0) {
                    this._submitForm({ isFinish: true, isDraft: true });
                } else {
                    const isFinish = this.$('button[value="finish"]').length !== 0;
                    this._submitForm({ isFinish });
                }
            }
        }

        return this._super.apply(this, arguments);
    },

    /**
     * Override _onSubmit to support custom draft handling
     */
    _onSubmit: function (event) {
        event.preventDefault();
        const $target = $(event.currentTarget);
        const options = {};

        if ($target.val() === "draft") {
            options.isFinish = true;
            options.isDraft = true;
            return this._submitForm(options);
        }

        return this._super.apply(this, arguments);
    },

    /**
     * Patch _submitForm to support isDraft option
     */
    _submitForm: function (options) {
        options = options || {};
        const params = {};

        if (options.previousPageId) {
            params.previous_page_id = options.previousPageId;
        }
        if (options.isDraft) {
            params.isDraft = true;
        }
        if (options.isFinish) {
            params.isFinish = true;
        }

        const $form = this.$("form");
        const formData = new FormData($form[0]);

        if (!options.skipValidation && !this._validateForm($form, formData)) {
            return;
        }

        this._prepareSubmitValues(formData, params);
        this.preventEnterSubmit = true;

        if (this.options.sessionInProgress) {
            this.fadeInOutDelay = 400;
            this.readonly = true;
        }

        const route = this.options.isStartScreen
            ? "/survey/begin"
            : "/survey/submit";

        const submitPromise = this.rpc(
            `${route}/${this.options.surveyToken}/${this.options.answerToken}`,
            params
        );

        return this._nextScreen(submitPromise, options);
    },
});
