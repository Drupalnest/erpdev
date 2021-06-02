# -*- coding: utf-8 -*-
# from odoo import http


# class StaplesWeb(http.Controller):
#     @http.route('/staples_web/staples_web/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/staples_web/staples_web/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('staples_web.listing', {
#             'root': '/staples_web/staples_web',
#             'objects': http.request.env['staples_web.staples_web'].search([]),
#         })

#     @http.route('/staples_web/staples_web/objects/<model("staples_web.staples_web"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('staples_web.object', {
#             'object': obj
#         })
