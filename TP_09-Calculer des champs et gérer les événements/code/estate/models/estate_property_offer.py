from odoo import models, fields, api
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection(
        [('accepted', 'Accepted'),
         ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(default=7, store=True)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )


    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = (record.create_date.date() if record.create_date else fields.Date.today())
            record.date_deadline = create_date + timedelta(days=record.validity)
    
    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            create_date = (record.create_date.date() if record.create_date else fields.Date.today())
            record.validity = (record.date_deadline - create_date).days
