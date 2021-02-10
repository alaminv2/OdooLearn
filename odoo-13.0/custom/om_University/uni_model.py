from odoo import models, fields, api, _


class UniStudents(models.Model):
    _name = 'university.students.managements'
    _description = 'University Students Records'
    _rec_name = 'username'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    roll = fields.Integer('Roll', required=True)
    username = fields.Char('User Name', required=True)
    fullname = fields.Char('Full Name', required=False)
    dept = fields.Char('Depertment', required=True)
    sess = fields.Char('Session', required=True)
    address = fields.Text('Address')
    name_seq = fields.Char('Student ID', required=True, readonly=True, index=True, copy=False,
                           default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('studnts.sequence') or _('New')
        result = super(UniStudents, self).create(vals)
        return result


class UniTeachers(models.Model):
    _name = 'university.teachers.managements'
    _description = 'University Teachers Records'
    _rec_name = 'username'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    username = fields.Char('User Name')
    fullname = fields.Char('Full Name')
    coursename = fields.Char('Course Name')
    phone = fields.Char('Phone')
    email = fields.Char('E-mail')
    address = fields.Text('Address')
    name_seq = fields.Char('Teacher ID', required=True, readonly=True, index=True, copy=False,
                           default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('teachers.sequence') or _('New')
        result = super(UniTeachers, self).create(vals)
        return result
