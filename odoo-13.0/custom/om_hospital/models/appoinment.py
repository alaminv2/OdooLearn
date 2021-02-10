from odoo import models, fields, api, _
import datetime, pytz


class Hospital_Appoinment(models.Model):
    _name = 'hospital.appoinment'
    _description = 'For Stroring Appoinment records of the patients'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    _rec_name = 'patient_id'

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', _('New Appoint') == _('New Appoint')):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('hospital.appoinment.sequence') or _('New_Appoint')
            print('vals_list', vals_list)
        res = super(Hospital_Appoinment, self).create(vals_list)
        return res

    def confirm_action(self):
        patient = self.env['hospital.management'].search([('id', '=', 7)])
        print(patient.patient_name)
        print(patient.display_name)

    def done_action(self):
        for rec in self:
            rec.state = 'done'

    def delete_lines(self):
        for rec in self:
            print('Time in UTC : ', rec.date)
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            print('user_tz = ', user_tz)
            day_today = pytz.utc.localize(rec.date).astimezone(user_tz)
            print('time in local timezone = ', day_today)
            rec.appointment_lines = [(5, 0, 0)]

    @api.onchange('partner_id')
    def onchange_Un(self):
        for rec in self:
            return {'domain': {'partner_id': [(self.partner_type, '=', True)]}}


    @api.model
    def default_get(self, fields):
        res = super(Hospital_Appoinment, self).default_get(fields)
        appointment_lines = []
        all_products = self.env['product.product'].search([])
        print('all_products = ',all_products)
        for item in all_products:
            vals = (0, 0, {
                'medicine': item.id,
                'quantity': 11,
            })
            appointment_lines.append(vals)
        print('lines = ', appointment_lines)
        res.update({
            'appointment_lines' : appointment_lines,
            'patient_id' : 8,
            'notes' : 'Demo',
        })
        return res

    @api.onchange('product_template')
    def change_value_of_medicine(self):
        print('In change_value_of_medicine...!!!')
        for rec in self:
            if rec.product_template:
                print('rec in onchange = ', rec.product_template)
                print('rec in onchange = ', rec.product_template.product_variant_ids)
                lines = [(5, 0, 0)]
                for item in rec.product_template.product_variant_ids:
                    vals = {
                        'medicine': item.id,
                        'quantity': 1,
                    }
                    lines.append((0, 0, vals))
                print('lines = ', lines)
                rec.appointment_lines = lines


    def test_recordset(self):
        for rec in self:
            print('Inside "test_recordset" Function')
            partners = self.env['res.partner'].search([])
            sorted_partners = partners.sorted(lambda o: o.name, reverse=True)
            filtered_partners = partners.filtered(lambda o: o.user_id.name == 'Alamin').sorted(key=lambda o: o.name)
            for partner in filtered_partners:
                print(partner.mapped('name'))

    patient_id = fields.Many2one('hospital.management', string='Patient', required=True, ondelete='cascade')
    age = fields.Integer(string="Age", related='patient_id.patient_age')
    notes = fields.Text(string='Registration Notes')
    date = fields.Datetime(string="Date Appointed")
    date_end = fields.Datetime(string="Date Appointed End")
    name = fields.Char(string='Appoint ID', default=lambda self: _('New Appoint'))
    doctor_note = fields.Text(string="Doctor's Opinion")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    doctor_ids = fields.Many2many('hospital.doctor', 'patient_doctor_rel', string="Doctors")
    doctor_fees = fields.Float(string="Fees", default=50.5)
    pharmecy_note = fields.Text(string='Pharmecy Note')
    product_template = fields.Many2one('product.template', string="Product Template")
    appointment_lines = fields.One2many('hospital.appoinment.lines', 'appoinment_id', string="Appointment Lines")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='States', readonly=True, default='draft')


class Hospital_Appoinment_Medicine(models.Model):
    _name = 'hospital.appoinment.lines'
    _description = 'For Stroring medicine records of the patients'

    medicine = fields.Many2one('product.product', string="Products")
    quantity = fields.Integer(string="Quantity")
    sequence = fields.Integer(string="Sequence")
    appoinment_id = fields.Many2one('hospital.appoinment', string="Appointment ID")
