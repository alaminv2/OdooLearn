from odoo import models, fields, api, _


class HealthCareAppointment(models.Model):
    _name = 'health.care.appointment'
    _description = 'Appointment Records'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    _rec_name = 'patient'

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _('New') == _('New')):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('health.appointment.sequence') or _('New')
        res = super(HealthCareAppointment, self).create(vals_list)
        return res

    patient = fields.Many2one('health.care.patient', string="Patient", required=True, default=2)
    age = fields.Integer(string='Age', related='patient.patient_age')
    date = fields.Date(string='Date', required=True, default=fields.Date.today())
    reason = fields.Text(string='Reason', related='patient.reason')
    name = fields.Char(string="Appointment ID", required=True, index=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
