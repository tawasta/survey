odoo.define("survey_question_type_privacy", [], function () {
    "use strict";

    const survey_form = odoo.loader.modules.get("@survey/js/survey_form")[
        Symbol.for("default")
    ];
    survey_form.include({
        events: $.extend({}, survey_form.prototype.events, {
            "change .o_survey_form_privacy_item": "_onChangePrivacyItem",
        }),
        _onChangePrivacyItem: function (event) {
            console.log("CHANGE");
            var self = this;
            var $target = $(event.currentTarget);
            var $label = $target.closest("label");
            $label.toggleClass(
                "o_survey_selected",
                !$label.hasClass("o_survey_selected")
            );

            // Conditional display
            if (
                this.options.questionsLayout !== "page_per_question" &&
                Object.keys(this.options.triggeredQuestionsByAnswer).includes(
                    $target.val()
                )
            ) {
                var isInputSelected = $label.hasClass("o_survey_selected");
                // Hide and clear or display depending question
                this.options.triggeredQuestionsByAnswer[$target.val()].forEach(
                    function (questionId) {
                        var dependingQuestion = $(".js_question-wrapper#" + questionId);
                        dependingQuestion.toggleClass("d-none", !isInputSelected);
                        if (!isInputSelected) {
                            self._clearQuestionInputs(dependingQuestion);
                        }
                    }
                );
                // Add/remove answer to/from selected answer
                if (!isInputSelected) {
                    self.selectedAnswers.splice(
                        self.selectedAnswers.indexOf(parseInt($target.val(), 10)),
                        1
                    );
                } else {
                    self.selectedAnswers.push(parseInt($target.val(), 10));
                }
            }
        },
        _prepareSubmitValues: function (formData, params) {
            this._super.apply(this, arguments);
            var self = this;
            this.$("[data-question-type]").each(function () {
                switch ($(this).data("questionType")) {
                    case "privacy":
                        params = self._prepareSubmitChoices(
                            params,
                            $(this),
                            $(this).data("name")
                        );
                        break;
                }
            });
        },
    });
});
