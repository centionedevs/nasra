# -*- coding: utf-8 -*-
# from odoo import http


# class SureHrMultiApprovalChain(http.Controller):
#     @http.route('/sure_hr_multi_approval_chain/sure_hr_multi_approval_chain/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sure_hr_multi_approval_chain/sure_hr_multi_approval_chain/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sure_hr_multi_approval_chain.listing', {
#             'root': '/sure_hr_multi_approval_chain/sure_hr_multi_approval_chain',
#             'objects': http.request.env['sure_hr_multi_approval_chain.sure_hr_multi_approval_chain'].search([]),
#         })

#     @http.route('/sure_hr_multi_approval_chain/sure_hr_multi_approval_chain/objects/<model("sure_hr_multi_approval_chain.sure_hr_multi_approval_chain"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sure_hr_multi_approval_chain.object', {
#             'object': obj
#         })
