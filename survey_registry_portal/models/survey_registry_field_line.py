from odoo import fields, models


class SurveyRegistryFieldLine(models.Model):
    _name = "survey.registry.field.line"
    _description = "Survey Registry Field Line"
    _order = "survey_id, sequence, id"

    sequence = fields.Integer(default=10)

    survey_id = fields.Many2one(
        "survey.survey", string="Survey", required=True, ondelete="cascade"
    )
    field_id = fields.Many2one(
        "ir.model.fields",
        string="User Input Record's Field",
        required=True,
        domain=[("model", "=", "survey.user_input")],
        ondelete="cascade",
    )

    title_on_website = fields.Char(required=True, translate=True)

    # TODO: simple solution for showing e.g. "€" after monetary amounts, but
    # can need more complex handling if actually dealing with multicurrencies
    value_suffix_on_website = fields.Char()
