from odoo import api, fields, models

class HospitalSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    notes = fields.Char(String='Default Note')

    def set_values(self):
        res = super(HospitalSetting, self).set_values()
        self.env['ir.config_parameter'].set_param('om_hospital.note', self.notes)
        return res


    @api.model
    def get_values(self):
        res = super(HospitalSetting, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        notes = ICPSudo.get_param('om_hospital.notes')
        return res