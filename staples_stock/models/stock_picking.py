from odoo import api, fields, models, _
from odoo.exceptions import UserError
import json
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    carrier_tracking_ref = fields.Char(string='Tracking Reference', copy=False)
    carrier_tracking_url = fields.Char(string='Tracking URL', compute='_compute_tracking_url')

    @api.depends('carrier_tracking_ref')
    def _compute_tracking_url(self):
        for rec in self:
            if rec.carrier_tracking_ref:
                if rec.sale_id.shipvia_id.name.lower().find('ups') != -1:
                    rec.carrier_tracking_url = 'https://www.ups.com/track?loc=null&tracknum=%s&requester=WT/trackdetails' % rec.carrier_tracking_ref
                if rec.sale_id.shipvia_id.name.lower().find('fed') != -1:
                    rec.carrier_tracking_url = 'https://www.fedex.com/fedextrack/?action=track&trackingnumber=%s' % rec.carrier_tracking_ref

    # https://www.fedex.com/fedextrack/?action=track&trackingnumber=
    # https://www.ups.com/track?loc=null&tracknum=1ZR5R0120327410867&requester=WT/trackdetails

    def open_tracking_url(self):
        self.ensure_one()
        if not self.carrier_tracking_url:
            raise UserError(_("Your delivery method has no redirect on courier provider's website to track this order."))

        carrier_trackers = []
        try:
            carrier_trackers = json.loads(self.carrier_tracking_url)
        except ValueError:
            carrier_trackers = self.carrier_tracking_url
        else:
            msg = "Tracking links for shipment: <br/>"
            for tracker in carrier_trackers:
                msg += '<a href=' + tracker[1] + '>' + tracker[0] + '</a><br/>'
            self.message_post(body=msg)
            # return self.env.ref('delivery.act_delivery_trackers_url').read()[0]

        client_action = {
            'type': 'ir.actions.act_url',
            'name': "Shipment Tracking Page",
            'target': 'new',
            'url': self.carrier_tracking_url,
        }
        return client_action