# -*- coding: utf-8 -*-
# from odoo import http


# class NasraHrEmployeeCustomizations(http.Controller):
#     @http.route('/nasra_hr_employee_customizations/nasra_hr_employee_customizations', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nasra_hr_employee_customizations/nasra_hr_employee_customizations/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('nasra_hr_employee_customizations.listing', {
#             'root': '/nasra_hr_employee_customizations/nasra_hr_employee_customizations',
#             'objects': http.request.env['nasra_hr_employee_customizations.nasra_hr_employee_customizations'].search([]),
#         })

#     @http.route('/nasra_hr_employee_customizations/nasra_hr_employee_customizations/objects/<model("nasra_hr_employee_customizations.nasra_hr_employee_customizations"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nasra_hr_employee_customizations.object', {
#             'object': obj
#         })
