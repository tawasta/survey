odoo.define('suvey_notifications.survey_keydown_override', function (require) {
    'use strict';

    const SurveyFormWidget = require("survey.form");

    // Pakotettu yliajo poistamalla mahdolliset muut määrittelyt
    SurveyFormWidget.prototype._onKeyDown = function (event) {
        // Block Enter key
        if (event.keyCode === 13) {
            console.log("Enter key behavior completely disabled.");
            event.preventDefault();
            return false; // Estää Enter-näppäimen toiminnon
        }

        // Jos muita näppäimiä, voit lisätä muuta logiikkaa tähän
        console.log("Key pressed: ", event.keyCode);
    };

    console.log("suvey_notifications forcibly overrides _onKeyDown.");
});
