from lxml import etree

from odoo import models, fields, api, _
from odoo.exceptions import UserError

import json
from odoo.tools import ustr


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_specific_emp = fields.Boolean('Special Employee')