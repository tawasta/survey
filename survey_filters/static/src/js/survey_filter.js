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

        $("#select_course").select2({
            placeholder: "Select courses",
            allowClear: true,
        });
        $("#select_event").select2({
            placeholder: "Select events",
            allowClear: true,
        });

        $("#select_course").on("change", function () {
            $("#hidden_courses").val($("#select_course").val().toString());
            var path = window.location.pathname;
            var val = $("#hidden_courses").val();
            if (path.indexOf("/course") >= 0) {
                path = window.location.pathname.split("/course")[0];
            }

            if (val) {
                window.location.href = path + "/course/" + val;
            } else {
                window.location.href = path;
            }
        });

        $("#select_event").on("change", function () {
            $("#hidden_events").val($("#select_event").val().toString());
            var path = window.location.pathname;
            var val = $("#hidden_events").val();
            if (path.indexOf("/event") >= 0) {
                path = window.location.pathname.split("/event")[0];
            }

            if (val) {
                window.location.href = path + "/event/" + val;
            } else {
                window.location.href = path;
            }
        });

        var path = window.location.pathname;
        if (path.indexOf("/date_start") >= 0) {
            var date_current = path.split("/date_start/")[1];
            var newDateTime = moment(date_current, "DD.MM.YYYY").toDate();
            $("#datetimepicker-filter-date").datetimepicker({
                format: "DD.MM.Y",
                locale: moment.locale(),
                defaultDate: newDateTime,
            });
        } else {
            var dateNow = new Date();
            $("#datetimepicker-filter-date").datetimepicker({
                format: "DD.MM.Y",
                locale: moment.locale(),
                defaultDate: dateNow,
            });
        }

        $("#datetimepicker-filter-date").on("change.datetimepicker", function () {
            var date = $(this).find(".datetimepicker-input").val();
            var path = window.location.pathname;
            if (path.indexOf("/date_start") >= 0) {
                path = window.location.pathname.split("/date_start")[0];
            }

            if (date) {
                window.location.href = path + "/date_start/" + date;
            } else {
                window.location.href = path;
            }
        });
        if (path.indexOf("/date_end") >= 0) {
            var date_current = path.split("/date_end/")[1];
            var newDateTime = moment(date_current, "DD.MM.YYYY").toDate();
            $("#datetimepicker-filter-end-date").datetimepicker({
                format: "DD.MM.Y",
                locale: moment.locale(),
                defaultDate: newDateTime,
            });
        } else {
            var dateNow = new Date();
            $("#datetimepicker-filter-end-date").datetimepicker({
                format: "DD.MM.Y",
                locale: moment.locale(),
                defaultDate: dateNow,
            });
        }

        $("#datetimepicker-filter-end-date").on("change.datetimepicker", function () {
            var date = $(this).find(".datetimepicker-input").val();
            var path = window.location.pathname;
            if (path.indexOf("/date_end") >= 0) {
                path = window.location.pathname.split("/date_end")[0];
            }

            if (date) {
                window.location.href = path + "/date_end/" + date;
            } else {
                window.location.href = path;
            }
        });
    });
});
