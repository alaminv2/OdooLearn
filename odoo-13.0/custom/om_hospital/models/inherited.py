from odoo import models, api, fields

class ResPartners(models.Model):
    _inherit = ['res.partner']

    @api.model
    def create(self, vals_list):
        result = super(ResPartners, self).create(vals_list)
        print(result)
        return  result


class EmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    patient = fields.Many2one('hospital.management', string="Patient")

    def employee_inherit_button(self):
        print('A button is added to the Employee model which was inherited.......!!!')