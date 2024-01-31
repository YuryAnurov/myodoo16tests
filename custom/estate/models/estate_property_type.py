from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estateproperty type description"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    # если добавить строку ниже, в автоматически созданный form view добавятся все поля из offer
    # property_ids = fields.One2many("estate.property.offer", "property_id")
    property_ids = fields.One2many("estate.property", "property_type_id")

    _sql_constraints = [
        ('check_unique_tags', 'unique(name)',
         'The property type name must be unique')
    ]
