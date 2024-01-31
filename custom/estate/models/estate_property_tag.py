from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estateproperty tag description"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string='Color')

    _sql_constraints = [
        ('check_unique_tags', 'unique(name)',
         'The property tag name must be unique')
    ]
