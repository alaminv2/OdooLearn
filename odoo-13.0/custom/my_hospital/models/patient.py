from odoo import models, fields, api, _


class HealthCarePatient(models.Model):
    _name = 'health.care.patient'
    _description = 'Health Care Patient Records'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    _rec_name = 'patient_name'

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _('New Patient')) == _('New Patient'):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('health.patients.sequence') or _('New Patient')
        result = super(HealthCarePatient, self).create(vals_list)
        return result

    def open_patient_appointments(self):
        print('Clicked')
        return {
            'name': 'Appointments',
            'res_model': 'health.care.appointment',
            'view_mode': 'tree,form',
            'domain': [('patient', '=', self.id)],
            'type': 'ir.actions.act_window',
            'view_id': False,
        }

    def get_appointment_number(self):
        count = self.env['health.care.appointment'].search_count([('patient', '=', self.id)])
        self.appointment_count = count + 1

    patient_name = fields.Char('Patient Name', required=True, track_visibility='always')
    patient_age = fields.Integer('Patient Age', required=True, track_visibility='always')
    patient_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others'),
    ], string='Patient Gender', required=True, track_visibility='always', default='male')
    patient_dob = fields.Date('Date of Birth', required=True, track_visibility='always', default=fields.Date.today())
    patient_phone = fields.Char('Phone', required=True, track_visibility='always', default='xxxxxxxxxxx')
    reason = fields.Text('Reason', track_visibility='always')
    patient_image = fields.Binary(string='Patient Image')
    name = fields.Char('Patient ID', required=True, readonly=True, index=True, copy=False,
                       default=lambda self: _('New Patient'))
    appointment_count = fields.Integer(string='Appointments', compute='get_appointment_number')
