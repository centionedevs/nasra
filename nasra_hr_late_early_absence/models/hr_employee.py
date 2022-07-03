from odoo import models, fields, api, _
from datetime import datetime, timedelta


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    late_early_absence_rule = fields.Boolean('Late Early Absence Apply Rule')