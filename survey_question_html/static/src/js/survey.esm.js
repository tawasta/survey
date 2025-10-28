/** @odoo-module **/

import SurveyFormWidget from "@survey/js/survey_form";

/*
 * CssEscape(str)
 * Tekee merkkijonosta turvallisen CSS-selektorin (esim. jos ID:ssä on erikoismerkkejä).
 */
function cssEscape(str) {
    var hasCSS = window.CSS && typeof window.CSS.escape === "function";
    if (hasCSS) return window.CSS.escape(str);
    return String(str).replace(/[^a-zA-Z0-9_\-]/g, function (s) {
        return "\\" + s;
    });
}
/*
 * IsHtmlEmpty(html)
 * Palauttaa true, jos HTML-kenttä on käytännössä tyhjä (vain tageja, välilyöntejä tai &nbsp;).
 */
function isHtmlEmpty(html) {
    if (!html) return true;
    const text = String(html)
        .replace(/<style[\s\S]*?<\/style>/gi, "")
        .replace(/<script[\s\S]*?<\/script>/gi, "")
        .replace(/<[^>]*>/g, "")
        .replace(/&nbsp;/gi, " ")
        .replace(/\u200B/g, "")
        .trim();
    return text.length === 0;
}
/*
 * SyncCkToTextareas($root, formData)
 * Synkronoi CKEditorin sisällön takaisin textarea-elementteihin ja tarvittaessa myös FormDataan.
 */
function syncCkToTextareas($root, formData) {
    $root.find("textarea.o_survey_question_html").each(function () {
        const $ta = $(this);
        const name = $ta.attr("name");
        if (!name) return;
        const editor = $ta.data("ckeditorInstance");
        const raw = editor ? editor.getData() : $ta.val();
        const normalized = isHtmlEmpty(raw) ? "" : raw;
        $ta.val(normalized);
        if (formData && typeof formData.set === "function") {
            formData.set(name, normalized);
        }
    });
}
/*
 * CreateEditorFor($textarea)
 * Luo CKEditor-instanssin annetulle textarea-elementille (jos sitä ei vielä ole).
 */
function createEditorFor($textarea) {
    if (
        !$textarea ||
        !$textarea.length ||
        $textarea.data("ckeditorInstance") ||
        !window.ClassicEditor
    ) {
        return Promise.resolve();
    }
    return window.ClassicEditor.create($textarea[0], {
        toolbar: [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "|",
            "undo",
            "redo",
        ],
    }).then((editor) => {
        $textarea.data("ckeditorInstance", editor).attr("data-ckeditor", "1");
        $textarea.css("height", "auto");
        $textarea.closest(".o_wysiwyg_textarea_wrapper").css("height", "auto");
        $textarea.closest(".position-relative").find(".o_wysiwyg_loading").hide();
    });
}
/*
 * InitEditorsIn($root)
 * Käynnistää CKEditorin kaikille näkyville textarea.o_survey_question_html -kentille.
 */
function initEditorsIn($root) {
    const tasks = [];
    $root.find("textarea.o_survey_question_html:visible").each(function () {
        tasks.push(createEditorFor($(this)));
    });
    return Promise.all(tasks);
}

/*
 * SurveyFormWidget override
 * Lisää CKEditor-tuen, required-validoinnin ja synkronoinnin Odoon survey-lomakkeeseen.
 */
SurveyFormWidget.include({
    start() {
        const _super = this._super.apply(this, arguments);
        const observer = new MutationObserver((muts) => {
            for (const m of muts) {
                for (const n of m.addedNodes || []) {
                    if (
                        n instanceof HTMLElement &&
                        ((n.matches && n.matches("textarea.o_survey_question_html")) ||
                            (n.querySelector &&
                                n.querySelector("textarea.o_survey_question_html")))
                    ) {
                        initEditorsIn(this.$el);
                        return;
                    }
                }
            }
        });
        observer.observe(this.el, {childList: true, subtree: true});
        this._ckObserver = observer;
        return Promise.resolve(_super).then(() => initEditorsIn(this.$el));
    },

    destroy() {
        if (this._ckObserver) {
            this._ckObserver.disconnect();
            this._ckObserver = null;
        }
        this.$("textarea.o_survey_question_html").each(function () {
            const ed = $(this).data("ckeditorInstance");
            if (ed && ed.destroy)
                ed.destroy().then(() => $(this).removeData("ckeditorInstance"));
        });
        return this._super.apply(this, arguments);
    },

    // eslint-disable-next-line no-unused-vars
    _submitForm: async function (options) {
        if (!this.options.isStartScreen) {
            syncCkToTextareas(this.$el);

            const errors = {};
            const fieldLogs = [];
            const $form = this.$("form");

            $form.find("textarea.o_survey_question_html").each((_, el) => {
                const $ta = $(el);
                const name = $ta.attr("name") || "";
                // Wrapper can be separate from textarea → resolve by id=name
                let $wrapper = this.$(`.js_question-wrapper#${cssEscape(name)}`);
                if (!$wrapper.length) $wrapper = $ta.closest(".js_question-wrapper");

                const qid = $wrapper.attr("id") || name;
                const rawReq = $wrapper.attr("data-required");
                const reqAttr = (
                    rawReq === undefined || rawReq === null ? "" : String(rawReq)
                )
                    .trim()
                    .toLowerCase();
                const required =
                    reqAttr === "true" || reqAttr === "1" || reqAttr === "yes";
                const val = $ta.val();
                const empty = isHtmlEmpty(val);

                fieldLogs.push({
                    name,
                    wrapperId: qid,
                    required,
                    isEmpty: empty,
                    valuePreview: String(val || "").slice(0, 120),
                });

                if (required && empty) {
                    const msg =
                        $wrapper.data("constrErrorMsg") ||
                        "This question requires an answer.";
                    errors[qid] = msg;
                }
            });

            if (Object.keys(errors).length) {
                this._resetErrors();
                this._showErrors(errors);
                const firstKey = Object.keys(errors)[0];
                if (firstKey)
                    this._scrollToError(
                        this.$(`.js_question-wrapper#${cssEscape(firstKey)}`)
                    );
                return;
            }
        }

        return this._super.apply(this, arguments);
    },
    /*
     * _prepareSubmitValues(formData, params)
     * Lisää HTML-vastausten arvot params-objektiin ennen lomakkeen lähettämistä.
     */
    _prepareSubmitValues(formData, params) {
        this._super.apply(this, arguments);
        syncCkToTextareas(this.$el, formData);

        this.$("textarea.o_survey_question_html").each(function () {
            const $ta = $(this);
            const qid = $ta.attr("name");
            if (!qid) return;
            const val = $ta.val() || "";
            params[qid] = {value: val, value_html: val};
        });

        return params;
    },
});
