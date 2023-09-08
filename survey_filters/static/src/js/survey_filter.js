odoo.define("survey.survey_page_statistics_inner", function () {
    "use strict";

    $(function () {
        $("#select_user").on("change", function () {
            var val = $(this).val();
            var path = window.location.pathname;

            if (path.indexOf("/user") >= 0) {
                path = window.location.pathname.split("/user")[0];
            }
            console.log("path:", path);
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
        $("#selectevent").select2({
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
                console.log("path5:", window.location.pathname);
            } else {
                window.location.href = path;
            }
        });

        $("#selectevent").on("change", function () {
            $("#hiddenevents").val($("#selectevent").val().toString());
            var path = window.location.pathname;
            var val = $("#hiddenevents").val();
            console.log("event filter hiddenevents val:", val);
            if (path.indexOf("/event") >= 0) {
                path = window.location.pathname.split("/event")[0];
            }

            if (val) {
                window.location.href = path + "/event/" + val;
                console.log(path + "/event/" + val);
                console.log("path4:", window.location.pathname);
            } else {
                window.location.href = path;
            }
        });

        var path = window.location.pathname;
        console.log("path2:", path);
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
        console.log("path3:", path);

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
