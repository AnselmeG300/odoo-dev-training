from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer()
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _unique_property_type_name = models.Constraint("UNIQUE (name)", "The property type name must be unique.")
    _order = "sequence, name"

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
