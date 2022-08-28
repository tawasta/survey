odoo.define("survey_question_attachment.survey", function (require) {
    "use strict";
    var SurveyFormWidget = require("survey.form");
    var utils = require("web.utils");
    var core = require("web.core");
    var _t = core._t;

    SurveyFormWidget.include({
        events: _.extend({}, SurveyFormWidget.prototype.events, {
            "change .o_survey_question_attachment": "_onChangeFileInput",
        }),

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.useFileAPI = Boolean(window.FileReader);
                self.file_value = {};
                if (!self.useFileAPI) {
                    self.fileupload_id = _.uniqueId("o_fileupload");
                    $(window).on(self.fileupload_id, function () {
                        var args = [].slice.call(arguments).slice(1);
                        self.on_file_uploaded.apply(self, args);
                    });
                }
            });
        },

        _onChangeFileInput: function (e) {
            var self = this;
            var file_node = e.target;
            var files_list = [];
            var validation_size_max =
                e.target.getAttribute("validation-size-max") * 1024 * 1024;
            if (
                (this.useFileAPI && file_node.files.length) ||
                (!this.useFileAPI && $(file_node).val() !== "")
            ) {
                if (this.useFileAPI) {
                    var files = file_node.files;
                    for (const file of files) {
                        if (file.size > validation_size_max) {
                            var msg = _t(
                                "The selected attachment exceed the maximum file size of %s."
                            );
                            this.do_warn(
                                _t("File upload"),
                                _.str.sprintf(
                                    msg,
                                    utils.human_size(validation_size_max)
                                )
                            );
                            return false;
                        }
                        utils.getDataURLFromFile(file).then(function (data) {
                            data = data.split(",")[1];
                            files_list.push({file_name: file.name, data: data});
                        });
                        self.file_value[$(file_node).data("name")] = files_list;
                        self.file_value[
                            $(file_node).data("name")
                        ].is_answer_update = true;
                    }
                }
            }
        },

        _prepareSubmitValues: function (_formData, params) {
            this._super.apply(this, arguments);
            var self = this;
            // Get all question answers by question type
            this.$(".o_survey_question_attachment[data-question-type]").each(
                function () {
                    switch ($(this).data("questionType")) {
                        case "attachment":
                            if (self.file_value[$(this).data("name")]) {
                                params = self._prepareSubmitFiles(
                                    params,
                                    $(this),
                                    $(this).data("name")
                                );
                                self.file_value[
                                    $(this).data("name")
                                ].is_answer_update = false;
                            } else if (
                                $("div.o_survey_attachment_answer").length !== 0
                            ) {
                                params[$(this).data("name")] = {
                                    values: null,
                                    is_answer_update: false,
                                };
                            }
                            break;
                    }
                }
            );
        },

        _prepareSubmitFiles: function (params, _$parent, questionId) {
            if (this.file_value[questionId]) {
                params[questionId] = {
                    values: this.file_value[questionId],
                    is_answer_update: this.file_value[questionId].is_answer_update,
                };
            }
            return params;
        },
    });
});
