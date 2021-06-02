from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    delivery_charge_default_product_id = fields.Many2one(
        'product.product',
        'Delivery Cost Product',
        domain="[('type', '=', 'service')]",
        config_parameter='staples_delivery.delivery_charge_default_product_id',
        help='Default product used for delivery charges')
