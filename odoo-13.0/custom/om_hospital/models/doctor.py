from odoo import models, fields, api, _

class Doctor(models.Model):
    _name='hospital.doctor'
    _description = 'Doctor and patient relationship records...'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'doctor_name'

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _('New')) == _('New'):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('hospital.doctor.sequence') or _('New')
        res = super(Doctor, self).create(vals_list)
        return  res

    doctor_name = fields.Char(string="Name", track_visibility = 'always')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', default='male', tract_visibility = 'always')
    related_user = fields.Many2one('res.users')
    name=fields.Char(string="Doctor_ID", copy=False, index=True, readonly=True, default=lambda self: _("New"))