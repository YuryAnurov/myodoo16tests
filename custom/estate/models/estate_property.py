from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare
from datetime import datetime, timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estateproperty description"
    _order = "id desc"

    name = fields.Char(required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string='Available From', default=datetime.today().date() + timedelta(days=+90), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string=' ')
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    active = fields.Boolean(default=True)
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')],)
    state = fields.Selection(default='new', string="Status", copy=False, required=True, selection=[
        ('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'), ('cancelled', 'Cancelled')
        ])
    total_area = fields.Float(string='Total Area (sqm)', compute='_compute_total_area', store=True)
    best_price = fields.Float(string='Best price', compute='_compute_best_price')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be strictly posititve'),
        ('check_selling_price', 'CHECK(expected_price >= 0)',
         'The selling price must be posititve')
    ]

    @api.constrains('selling_price')
    def check_selling_price(self):
        for record in self:
            # if record.selling_price < 0.9 * record.expected_price:
            # Метод float_compare() возвращает отрицательное число, если первое число меньше второго, 0, если числа
            # равны, и положительное число, если первое число больше второго. Метод float_is_zero() возвращает True,
            # если заданное число близко к 0.
            if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) == -1:
                # record.selling_price = 0  # вызывает рекурсию
                raise ValidationError(
                    'The selling price must be at least 90% of expected price. You must reduce the '
                    'expected price if you want to accept this offer'
                )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            # record.best_price = max(record.mapped('offer_ids.price')) # для новых записей возникала проблема
            prices = record.mapped('offer_ids.price')
            if prices:
                record.best_price = max(prices)
                if record.state == 'new':
                    record.state = 'received'
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_set_cancel(self):
        for record in self:
            if self.state != 'sold':
                self.state = 'cancelled'
            else:
                raise UserError("Sold properties cannot be cancelled.")
        return True

    def action_set_sold(self):
        for record in self:
            if self.state != 'cancelled':
                self.state = 'sold'
            else:
                raise UserError("Cancelled properties cannot be sold.")
        return True
