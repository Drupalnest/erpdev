# -*- coding: utf-8 -*-
# from odoo import http


# class StaplesBase(http.Controller):
#     @http.route('/staples_base/staples_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/staples_base/staples_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('staples_base.listing', {
#             'root': '/staples_base/staples_base',
#             'objects': http.request.env['staples_base.staples_base'].search([]),
#         })

#     @http.route('/staples_base/staples_base/objects/<model("staples_base.staples_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('staples_base.object', {
#             'object': obj
#         })
