# -*- coding:utf-8 -*-

from odoo import models, fields


class EmployeeMissionApprobation(models.Model):
    _name = "hr.employee.mission.approbation"
    _order = "sequence"

    missions = fields.Many2one('hr.mission', string='Missions', required=True)
    approver = fields.Many2one('res.users', string='Approver', required=True)
    sequence = fields.Integer(string='Approbation sequence', default=10, required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now())
