from lxml import etree

from odoo import models, fields, api, _
from odoo.exceptions import UserError,ValidationError

import json
from odoo.tools import ustr


class HrContract(models.Model):
    _inherit = 'hr.contract'

    is_invisible_salary = fields.Boolean(compute='_compute_is_invisible_salary')

    @api.onchange('employee_id')
    def _compute_is_invisible_salary(self):
        if not self.env.user.has_group('nasra_top_managment_group.group_top_managment') and self.employee_id.is_specific_emp:
            self.is_invisible_salary = True
        else:
            self.is_invisible_salary = False


    @api.constrains('wage','allowances_per_day','variable')
    def constrain_import_salary_info(self):
        if not self.env.user.has_group(
            'nasra_top_managment_group.group_top_managment') and self.employee_id.is_specific_emp:
            raise ValidationError(_("Cannot Edit Those Fields in this employee"))

    def export_data(self, fields_to_export):
        print('awwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
        if not self.env.user.has_group(
            'nasra_top_managment_group.group_top_managment') and ('wage' in fields_to_export or 'allowances_per_day' in fields_to_export or 'variable' in fields_to_export):
            for rec in self:
                if rec.employee_id.is_specific_emp:
                    raise ValidationError(_("Cannot Export Those Fields in this employee"))

        return super(HrContract, self).export_data(fields_to_export)



    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     if view_type == 'form':
    #         print('aaaaaaaaaaaaa')
    #         form_view = self.env.ref('hr_contract.hr_contract_view_form')
    #         group = self.env.user.has_group('nasra_top_managment_group.group_top_managment')
    #         doc = etree.XML(res['arch'])
    #         for node in doc.xpath("//page[@name='information']"):
    #             node.set("invisible", "1")
    #             modifiers = {}
    #             modifiers['invisible'] = True
    #             node.set("modifiers", json.dumps(modifiers))
    #         res['arch'] = etree.tostring(doc)
    #     return res
