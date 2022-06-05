# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError, AccessError

from odoo import models, fields, api,_



class sure_employee_profile(models.Model):
    _inherit = 'res.users'

    # def write(self, values):
    #     if self.env.user.has_group('base.group_portal'):
    #         raise ValidationError(_("You Can't Edit Your Profile"))
    #     res = super(sure_employee_profile, self).write(values)
    #     return res


    def user_has_employee(self):
        employee = self.env['hr.employee'].sudo().search([('user_id','=',self.env.user.id)],limit=1)
        if employee:
            return True
        else:
            return False


class hr_employee(models.Model):
    _inherit = 'hr.employee'

    def write(self, values):
        res = super(hr_employee, self).write(values)
        if 'work_email' in values:
            if self.env.user.has_group('hr.group_hr_manager'):
                self.user_id.sudo().update({'login':values.get('work_email')})
                self.user_id.partner_id.sudo().update({'email':values.get('work_email')})
        return res

    def _compute_total_allocation_used(self):
        for employee in self:
            employee.allocation_used_count = employee.allocation_count - round(employee.remaining_leaves,2)
            employee.allocation_used_display = "%g" % employee.allocation_used_count

    birthday = fields.Date('Date of Birth', groups="hr.group_hr_user,base.group_portal", tracking=True)
    payslip_count = fields.Integer(compute='_compute_payslip_count', string='Payslip Count', groups="hr_payroll.group_hr_payroll_user,base.group_portal")

    barcode = fields.Char(string="Badge ID", help="ID used for employee identification.", groups="hr.group_hr_user,base.group_portal",
                          copy=False)

    contract_warning = fields.Boolean(string='Contract Warning', store=True, compute='_compute_contract_warning', groups="hr.group_hr_user,base.group_portal")

    @api.depends('contract_id', 'contract_id.state', 'contract_id.kanban_state')
    def _compute_contract_warning(self):
        for employee in self:
            employee.contract_warning = not employee.contract_id or employee.contract_id.kanban_state == 'blocked' or employee.contract_id.state != 'open'

    @api.depends('contract_ids.state')
    def _compute_first_contract_date(self):
        for employee in self:
            contracts = employee.sudo().contract_ids.filtered(lambda c: c.state != 'cancel')
            if contracts:
                employee.first_contract_date = min(contracts.mapped('date_start'))
            else:
                employee.first_contract_date = False

    first_contract_date = fields.Date(compute='_compute_first_contract_date', groups="hr.group_hr_user,base.group_portal")


