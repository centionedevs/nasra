# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrLoan(models.Model):
    _inherit = 'hr.loan'

    def _default_employee(self):
        return self.env.user.employee_id

    def _default_approver(self):
        employee = self._default_employee()
        if type(employee) is int:
            employee_obj = self.env['hr.employee'].browse(employee)
        else:
            employee_obj = employee
        if employee_obj.holidays_approvers:
            return employee_obj.holidays_approvers[0].approver.id

    pending_approver = fields.Many2one('hr.employee', string="Pending Approver", default=_default_approver)
    pending_approver_rel = fields.Char(string="Pending Approver",
                                       related='pending_approver.name', readonly=True)
    pending_approver_user = fields.Many2one('res.users', string='Pending approver user',
                                            related='pending_approver.user_id', related_sudo=True, store=True,
                                            readonly=True)
    current_user_is_approver = fields.Boolean(string='Current user is approver',
                                              compute='_compute_current_user_is_approver')
    current_user_is_refusers = fields.Boolean(string='Current user is refuser',
                                              compute='_compute_current_user_is_refuser')
    approbations = fields.One2many('hr.employee.loan.approbation', 'loans', string='Approvals', readonly=True)
    pending_transfered_approver_user = fields.Many2one('res.users', string='Pending transfered approver user',
                                                       compute="_compute_pending_transfered_approver_user",
                                                       search='_search_pending_transfered_approver_user')

    def approve(self):
        for loan in self:
            is_last_approbation = False
            sequence = 0
            next_approver = None
            loan = loan.sudo()
            approvers_0day = loan.employee_id.holidays_approvers.filtered(lambda d: d.max_allow_days == 0).sorted(
                key=lambda x: x.sequence)
            approvers_days = loan.employee_id.holidays_approvers.filtered(
                lambda d: d.max_allow_days != 0 and d.max_allow_days < loan.number_of_days_temp).sorted(
                key=lambda x: x.max_allow_days)

            if approvers_0day:
                for index, appr in enumerate(approvers_0day):
                    if loan.pending_approver.id == appr.approver.id:
                        if index == len(approvers_0day) - 1:
                            if approvers_days:
                                next_approver = approvers_days[0].approver
                            else:

                                is_last_approbation = True
                        else:
                            next_approver = approvers_0day[index + 1].approver

                for indexes, apprs in enumerate(approvers_days):
                    if loan.pending_approver.id == apprs.approver.id:
                        if indexes == len(approvers_days) - 1:
                            is_last_approbation = True
                        else:
                            next_approver = approvers_days[indexes + 1].approver

            elif approvers_days:
                for indexess, apprss in enumerate(approvers_days):
                    if loan.pending_approver.id == apprss.approver.id:
                        if indexess == len(approvers_days) - 1:
                            is_last_approbation = True
                        else:
                            next_approver = approvers_days[indexess + 1].approver

            if is_last_approbation:
                loan.action_approved()
            else:
                loan.write({'state': 'draft', 'pending_approver': next_approver and next_approver.id or False})
                self.env['hr.employee.loan.approbation'].create(
                    {'loans': loan.id, 'approver': self.env.uid, 'sequence': sequence,
                     'date': fields.Datetime.now()})

    def action_approved(self):
        self.write({'pending_approver': None})
        super(HrLoan, self).action_approved()
        for loan in self:
            self.env['hr.employee.loan.approbation'].create(
                {'loans': loan.id, 'approver': self.env.uid, 'date': fields.Datetime.now()})

    def _compute_current_user_is_approver(self):
        if self.sudo().pending_approver.user_id.id == self.env.user.id:  # or self.env.user.has_group('hr.group_hr_manager'):
            self.current_user_is_approver = True
        else:
            self.current_user_is_approver = False

    def _compute_current_user_is_refuser(self):
        if self.sudo().pending_approver.user_id.id == self.env.user.id:  # or self.env.user.has_group('hr.group_hr_manager'):
            self.current_user_is_refusers = True
        else:
            self.current_user_is_refusers = False

    @api.onchange('employee_id')
    def _onchange_employee(self):
        for holiday in self:
            holiday = holiday.sudo()
            if holiday.employee_id and holiday.employee_id.holidays_approvers:
                app_0day = holiday.employee_id.holidays_approvers.filtered(lambda d: d.max_allow_days == 0).sorted(
                    key=lambda x: x.sequence)
                if app_0day:
                    holiday.pending_approver = app_0day[0].approver.id
                else:
                    app_days = holiday.employee_id.holidays_approvers.filtered(
                        lambda d: d.max_allow_days != 0 and d.max_allow_days < holiday.number_of_days_temp).sorted(
                        key=lambda x: x.max_allow_days)
                    if app_days:
                        holiday.pending_approver = app_days[0].approver.id
            else:
                holiday.pending_approver = False

    def _compute_pending_transfered_approver_user(self):
        self.pending_transfered_approver_user = self.pending_approver.transfer_holidays_approvals_to_user

    def _search_pending_transfered_approver_user(self, operator, value):
        replaced_employees = self.env['hr.employee'].search([('transfer_holidays_approvals_to_user', operator, value)])
        employees_ids = []
        for employee in replaced_employees:
            employees_ids.append(employee.id)
        return [('pending_approver', 'in', employees_ids)]


