# -*- coding: utf-8 -*-
from datetime import date

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def get_attendance_allowance(self, payslip,contract):
        total_att = []
        attend = self.env['hr.attendance'].search(
            [('check_in', '>=', payslip.date_from), ('check_out', '<=', payslip.date_to),
             ('employee_id', '=', self.id)])
        for att in attend:
            total_att.append(att.id)
        total_attend = len(total_att) * contract.allowances_per_day
        return total_attend

