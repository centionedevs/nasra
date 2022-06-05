# -*- coding:utf-8 -*-

from odoo import models, fields


class EmployeeLoanApprobation(models.Model):
    _name = "hr.employee.loan.approbation"
    _order = "sequence"

    loans = fields.Many2one('hr.loan', string='Loan', required=True)
    approver = fields.Many2one('res.users', string='Approver', required=True)
    sequence = fields.Integer(string='Approbation sequence', default=10, required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now())
