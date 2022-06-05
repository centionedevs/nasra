# -*- coding:utf-8 -*-

from odoo import models, fields


class EmployeeExcuseApprobation(models.Model):
    _name = "hr.employee.excuse.approbation"
    _order = "sequence"

    excuses = fields.Many2one('hr.excuse', string='Excuses', required=True)
    approver = fields.Many2one('res.users', string='Approver', required=True)
    sequence = fields.Integer(string='Approbation sequence', default=10, required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now())
