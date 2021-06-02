from odoo import api, fields, models


class AgedPartnerBalanceWizard(models.TransientModel):
    _name = 'aged.partner.balance.wizard'
    _description = 'AgedPartnerBalanceWizard'

    date_from = fields.Date(default=fields.Date.today())
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    partner_ids = fields.Many2many('res.partner', string="Partners")
    result_selection = fields.Selection([('customer', 'Receivable Accounts'), ('supplier', 'Payable Accounts')], default='customer')
    target_move = fields.Selection([('all', 'All Entries'), ('posted', 'All Posted Entries')], default='posted')

    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'result_selection', 'target_move', 'company_id', 'partner_ids'])[0]
        data['form']['period_length'] = 30
        return self.env.ref('staples_aged_report.action_report_aged_partner_balance').with_context(landscape=True).report_action(self, data=data)
