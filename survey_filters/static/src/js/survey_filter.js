odoo.define("survey.survey_page_statistics_inner", function () {
    "use strict";

    $(function () {
        // Asetusten määrittely yhdellä kertaa
        const initDatePicker = (selector) => {
            $(selector).datetimepicker({
                format: "DD.MM.YYYY",
                locale: moment.locale(),
            });
        };

        const initSelect2 = (selector, placeholder) => {
            $(selector).select2({
                placeholder: placeholder,
                allowClear: true,
            });
        };

        // Päivämäärävalitsimien ja pudotusvalikkojen alustaminen
        initDatePicker("#datetimepicker-filter-date");
        initDatePicker("#datetimepicker-filter-end-date");
        initSelect2("#select_course", "Select courses");
        initSelect2("#selectevent", "Select events");

        // Päivitä-painikkeen toiminnallisuus
        $("#apply_filters").on("click", function () {
            const selectedCourses = $("#select_course").val();
            const selectedEvents = $("#selectevent").val();
            const startDate = $("#filter-date").val();
            const endDate = $("#filter-end-date").val();

            // Poimitaan nykyisestä URL:sta survey-tieto (esim. "testi-1")
            const surveyPathMatch = window.location.pathname.match(/\/survey\/results\/([^\/]+)/);
            const surveyPath = surveyPathMatch ? surveyPathMatch[1] : null;

            if (!surveyPath) {
                alert("Survey information is missing from the URL!");
                return;
            }

            // Luo URL-suodatinpolku vain valituista arvoista
            const filters = [];
            if (selectedCourses && selectedCourses.length > 0) {
                filters.push("course/" + selectedCourses.join(","));
            }
            if (selectedEvents && selectedEvents.length > 0) {
                filters.push("event/" + selectedEvents.join(","));
            }
            if (startDate) {
                filters.push("date_start/" + encodeURIComponent(startDate));
            }
            if (endDate) {
                filters.push("date_end/" + encodeURIComponent(endDate));
            }

            // Rakennetaan uusi URL
            let newPath = `/survey/results/${surveyPath}`; // Säilytetään survey ID tai nimi
            if (filters.length > 0) {
                newPath += `/${filters.join("/")}`; // Lisätään valitut suodattimet
            }

            // Päivitä sivu suodattimien mukaan
            window.location.href = newPath;
        });
    });
});
