# -*- coding: utf-8 -*-
# from odoo import http


# class BloomsHrWorkSchedule(http.Controller):
#     @http.route('/blooms_hr_work_schedule/blooms_hr_work_schedule', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/blooms_hr_work_schedule/blooms_hr_work_schedule/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('blooms_hr_work_schedule.listing', {
#             'root': '/blooms_hr_work_schedule/blooms_hr_work_schedule',
#             'objects': http.request.env['blooms_hr_work_schedule.blooms_hr_work_schedule'].search([]),
#         })

#     @http.route('/blooms_hr_work_schedule/blooms_hr_work_schedule/objects/<model("blooms_hr_work_schedule.blooms_hr_work_schedule"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('blooms_hr_work_schedule.object', {
#             'object': obj
#         })
