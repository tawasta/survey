odoo.define("survey.survey_page_statistics_inner", function () {
    "use strict";

    $(function () {
        $("#select_user").on("change", function () {
            var val = $(this).val();
            var path = window.location.pathname;

            if (path.indexOf("/user") >= 0) {
                path = window.location.pathname.split("/user")[0];
            }

            if (val) {
                window.location.href = path + "/user/" + val;
            } else {
                window.location.href = path;
            }
        });
    });
});
