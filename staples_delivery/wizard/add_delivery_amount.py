from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AddDeliveryAmount(models.TransientModel):
    _name = 'add.delivery.amount'
    _description = 'Delivery Amount Add Wizard'

    delivery_price = fields.Float()
    order_id = fields.Many2one('sale.order')

    def button_confirm(self):
        self.order_id.set_delivery_line(self.delivery_price)
