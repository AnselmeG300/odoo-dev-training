from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError

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

    validity = fields.Integer(
        default=7, 
    )
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_deadline",
        store=True
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = (record.create_date.date() if record.create_date else fields.Date.today())
            record.date_deadline = create_date + timedelta(days=record.validity)

    @api.depends("date_deadline")
    def _inverse_deadline(self):
        for record in self:
            create_date = (record.create_date.date() if record.create_date else fields.Date.today())
            record.validity = (record.date_deadline - create_date).days

    def action_accept(self):
        for record in self:
            if record.property_id.state in ['sold', 'cancelled']:
                raise UserError("Cannot accept an offer for a sold or cancelled property.")
            # Une seule offre acceptée par bien
            other_offers = record.property_id.offer_ids - record
            other_offers.write({'status': 'refused'})
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True