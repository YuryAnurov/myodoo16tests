from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estateproperty offer description"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    create_date = fields.Datetime(string="Create Date", default=lambda self: fields.Datetime.now())
    validity = fields.Integer(default=7, string='Validity (days)')
    date_deadline = fields.Date(string='Deadline', compute='_compute_deadline', inverse='_inverse_deadline')

    @api.depends('validity', )
    def _compute_deadline(self):
        for record in self:
            create_date = fields.Date.from_string(record.create_date)
            validity = record.validity
            record.date_deadline = create_date + timedelta(days=validity)

    def _inverse_deadline(self):
        for record in self:
            create_date = fields.Date.from_string(record.create_date)
            date_deadline = fields.Date.from_string(record.date_deadline)
            record.validity = (date_deadline - create_date).days

    def action_accept(self):
        for record in self:
            try:
                estate_property = record.property_id
                # поля Many2one в Odoo в действительности представляют собой ссылки на записи в другой модели.
                # Когда вы обращаетесь к полю record.property_id, вы фактически получаете доступ к объекту-ссылке,
                # и вы можете устанавливать или получать значения полей этой записи, как если бы это было
                # полноценным объектом.
                estate_property.selling_price = record.price
                estate_property.buyer_id = record.partner_id
                estate_property.state = 'accepted'
            except ValidationError as e:
                raise e

        self.status = 'Accepted'
        return True

    def action_refuse(self):
        for record in self:
            self.status = 'Refused'
        return True

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'The offer price must be strictly posititve')
    ]
