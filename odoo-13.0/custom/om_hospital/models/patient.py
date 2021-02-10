from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(selection_add=[('om', 'Smart'), ('alamin', 'Alamin')])


class HospitalManagement(models.Model):
    _name = 'hospital.management'
    _description = 'Patient Record'
    _rec_name = 'patient_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalManagement, self).create(vals)
        return result

    def write(self, vals):
        res = super(HospitalManagement, self).write(vals)
        print('Write function overwrited.....')
        return res

    def name_get(self):
        result = []
        for field in self:
            result.append((field.id, '%s -- %s' % (field.name_seq, field.patient_name)))
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ['|', ('name_seq', operator, name), ('patient_name', operator, name)]
        return super(HospitalManagement, self).search(domain, limit=limit).name_get()


    @api.constrains('patient_name')
    def check_name(self):
        for rec in self:
            if len(rec.patient_name) > 10:
                raise ValidationError('The name length must be less than or equal 10...')

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age == 0:
                rec.age_group = 'minor'
            if rec.patient_age:
                if rec.patient_age < 18:
                    rec.age_group = 'minor'
                else:
                    rec.age_group = 'major'


    def show_patient_appointment(self):
        print('Clickedddd')
        return {
            'name': 'Appointments',
            'res_model': 'hospital.appoinment',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'view_id': False,
        }

    def get_appointment_number(self):
        self.appointment_count = self.env['hospital.appoinment'].search_count([('patient_id', '=', self.id)])

    @api.constrains('patient_name')
    def check_name(self):
        for rec in self:
            if rec.patient_name:
                if len(rec.patient_name) > 100:
                    raise ValidationError('The name length must be less than or equal 100...')

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age == 0:
                rec.age_group = 'minor'
            if rec.patient_age:
                if rec.patient_age < 18:
                    rec.age_group = 'minor'
                else:
                    rec.age_group = 'major'

    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender = rec.doctor_id.gender

    def button_send_mail(self):
        template_id = self.env.ref("om_hospital.patient_card_email_template").id
        print(template_id)
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)

    @api.depends('patient_name')
    def converttoupper(self):
        for rec in self:
            rec.patient_name_upper = rec.patient_name.upper() if rec.patient_name else False

    def patient_name_reverse(self):
        for rec in self:
            rec.patient_name = rec.patient_name_upper if rec.patient_name_upper else False

    @api.model
    def test_cron_job(self):
        print('cron job is running')

    def print_report(self):
        return self.env.ref('om_hospital.report_patient_card').report_action(self)

    def print_report_excel(self):
        return self.env.ref('om_hospital.report_patient_card_xlsx').report_action(self)

    def action_server_patient(self):
        print('Inside the "action_server_patient" Function')
        return {
            'name': 'Patient Server Action',
            'res_model': 'hospital.management',
            'view_mode': 'tree,form',
            'domain': [],
            'type': 'ir.actions.act_window',
            'view_id': False,
        }

    patient_name = fields.Char(string='Patient Name', required=True, track_visibility='always')
    patient_name_upper = fields.Char()
    patient_age = fields.Integer('Patient Age', track_visibility='always')
    patient_age2 = fields.Float('Age 2')
    notes = fields.Text('Notes')
    patient_image = fields.Binary(string='Patient Image')
    name_seq = fields.Char(string='Patient ID', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))
    appointment_count = fields.Integer(string='Appointments', compute="get_appointment_number")
    active=fields.Boolean(default=True, string="Archive")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    
    company_id = fields.Many2one('res.company', string="Company ID", readonly=False, required=True, default = lambda self: self.env.user.company_id)

    email_id = fields.Char(string="Email")
    user_id = fields.Many2one('res.users', string="PRO")

    doctor_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Doctor Gender', related='doctor_id.gender')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], default='male', string="Gender")
    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor'),
    ], string="Age Group", default='minor', compute='set_age_group')


class InvoiceInherit(models.Model):
    _inherit = 'account.move'
    brother_name = fields.Char(string='Brother Name')
