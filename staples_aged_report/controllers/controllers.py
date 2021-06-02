# -*- coding: utf-8 -*-
# from odoo import http


# class StaplesAgedReceivable(http.Controller):
#     @http.route('/staples_aged_report/staples_aged_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/staples_aged_report/staples_aged_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('staples_aged_report.listing', {
#             'root': '/staples_aged_report/staples_aged_report',
#             'objects': http.request.env['staples_aged_report.staples_aged_report'].search([]),
#         })

#     @http.route('/staples_aged_report/staples_aged_report/objects/<model("staples_aged_report.staples_aged_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('staples_aged_report.object', {
#             'object': obj
#         })
