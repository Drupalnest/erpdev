from odoo import models, fields, api, _


class CustomerOpenOrderReport(models.TransientModel):
    _name = "customer.open.order.report"

    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    target_order = fields.Selection([('draft', 'Quotation'),
                                     ('sale', 'Sales Order'),
                                     ('all', 'All Entries'),
                                     ], string='Target Orders', required=True, default='sale')

    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'target_order', 'company_id'])[0]
        return self.env.ref('staples_oco_report.action_report_open_customer_order').with_context(
            landscape=True).report_action(self, data=data)
