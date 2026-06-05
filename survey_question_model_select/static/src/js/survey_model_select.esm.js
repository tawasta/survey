/** @odoo-module **/

import SurveyFormWidget from "@survey/js/survey_form";

SurveyFormWidget.include({
    _prepareSubmitValues: function (formData, params) {
        console.info("[model_select] _prepareSubmitValues before super", {
            params: params,
        });

        this._super.apply(this, arguments);

        console.info("[model_select] _prepareSubmitValues after super", {
            params: params,
        });

        this.$("select.o_survey_question_model_select").each(function () {
            const $select = $(this);
            const questionId = $select.data("name") || $select.attr("name");

            console.info("[model_select] found select", {
                questionId: questionId,
                name: $select.attr("name"),
                dataName: $select.data("name"),
                value: $select.val(),
            });

            if (!questionId) {
                console.warn("[model_select] missing questionId, skipping select");
                return;
            }

            const value = $select.val() || "";

            params[questionId] = {
                value: value,
                suggested_answer_id: value,
                model_select_answer_id: value,
            };

            console.info("[model_select] params updated", {
                questionId: questionId,
                value: value,
                paramsValue: params[questionId],
            });

            if (formData && typeof formData.set === "function") {
                formData.set(questionId, value);

                console.info("[model_select] formData updated", {
                    questionId: questionId,
                    value: value,
                });
            }
        });

        console.info("[model_select] _prepareSubmitValues done", {
            params: params,
        });

        return params;
    },
});