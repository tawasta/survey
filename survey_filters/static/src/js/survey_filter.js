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

        $("#select_event").on("change", function () {
            var val = $(this).val();
            var path = window.location.pathname;

            if (path.indexOf("/event") >= 0) {
                path = window.location.pathname.split("/event")[0];
            }

            if (val) {
                window.location.href = path + "/event/" + val;
            } else {
                window.location.href = path;
            }
        });

        var path = window.location.pathname
        if (path.indexOf("/date") >= 0) {
            var date_current = path.split("/date/")[1];
            var newDateTime = moment(date_current, "DD.MM.YYYY").toDate();
            $('#datetimepicker-filter-date').datetimepicker({
                format : 'DD.MM.Y',
                locale: moment.locale(),
                defaultDate: newDateTime,
            });
        }else {
            var dateNow = new Date();
            $('#datetimepicker-filter-date').datetimepicker({
                format : 'DD.MM.Y',
                locale: moment.locale(),
                defaultDate: dateNow,
            });
        }

        $("#datetimepicker-filter-date").on("change.datetimepicker", function() {
            var date = $(this).find('.datetimepicker-input').val();
            var path = window.location.pathname
            if (path.indexOf("/date") >= 0) {
                path = window.location.pathname.split("/date")[0];
            }

            if (date) {
                window.location.href = path + "/date/" + date;
            } else {
                window.location.href = path;
            }
        });
    });
});
