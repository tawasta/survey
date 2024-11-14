/** @odoo-module */

import SurveyFormWidget from '@survey/js/survey_form';

SurveyFormWidget.include({
    _prepareSubmitValues(formData, params) {
        this._super(...arguments); // Kutsutaan alkuperäistä funktiota

        this.$('[data-question-type]').each(function () {
            if ($(this).data('questionType') === 'ssn') {
                params[$(this).attr('name')] = $(this).val();
            }
        });
    },
});
