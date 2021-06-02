# -*- coding: utf-8 -*-
# from odoo import http


# class StaplesFob(http.Controller):
#     @http.route('/staples_fob/staples_fob/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/staples_fob/staples_fob/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('staples_fob.listing', {
#             'root': '/staples_fob/staples_fob',
#             'objects': http.request.env['staples_fob.staples_fob'].search([]),
#         })

#     @http.route('/staples_fob/staples_fob/objects/<model("staples_fob.staples_fob"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('staples_fob.object', {
#             'object': obj
#         })
