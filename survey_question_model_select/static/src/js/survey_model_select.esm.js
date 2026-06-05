/** @odoo-module **/

import SurveyFormWidget from "@survey/js/survey_form";

SurveyFormWidget.include({
    _prepareSubmitValues: function (formData, params) {
        this._super.apply(this, arguments);

        this.$("select.o_survey_question_model_select").each(function () {
            const $select = $(this);
            const questionId = $select.data("name") || $select.attr("name");

            if (!questionId) {
                return;
            }

            const value = $select.val() || "";

            params[questionId] = {
                value: value,
                suggested_answer_id: value,
                model_select_answer_id: value,
            };

            if (formData && typeof formData.set === "function") {
                formData.set(questionId, value);
            }
        });

        return params;
    },
});