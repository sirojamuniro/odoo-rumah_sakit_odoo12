from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'


    @api.model
    def create(self, vals_list):
        res = super(ResPartner, self).create(vals_list)
        print("simpan master data Contacts dari modul gosantha_hospital")
        # do custom script here
        return res

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    patient_name = fields.Char(string='Nama Pasien')

class Initess(models.Model):
    _name = 'ini.tes'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Ini Tes Pasien'
    _rec_name='tes_nama'

    tes_nama= fields.Char(string='nama pasien', required=True)
    tes_umur= fields.Integer('umur', track_visibility='always')
    catatan=fields.Text(String='catatan')
    active = fields.Boolean(string='Active', default=True)
    dokter_id = fields.Many2one('ini.dokter', string='Dokter')
    dokter_gender = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan')
    ], string='Jen. Kel. Dokter')
    name_seq = fields.Char(string='Kode', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: ('New'))
    jenis_kelamin = fields.Selection([
        ('pria', 'Laki-laki'),
        ('wanita', 'Perempuan')
    ], string='Jenis Kelamin', default='pria')
    grup_umur = fields.Selection([
        ('dewasa', 'Dewasa'),
        ('anak', 'Anak')
    ], string='Grup Umur', compute='set_grup')
    # ini si appointment_count sudah disediakan classnya jadi hanya bisa memanggil appointment count
    appointment_count = fields.Integer(string='Releted', compute="get_appointment_count")


    @api.model
    def create(self, vals):
        if vals.get('name_seq', ('New')) == ('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('ini.tes.sequence') or ('New')
        return super(Initess, self).create(vals)

    @api.multi
    def get_appointment_count(self):
        count = self.env['ini.relet'].search_count([('re_id', '=', self.id)])
        self.appointment_count = count

    @api.depends('tes_umur')
    def set_grup(self):
        for rec in self:
            if rec.tes_umur:
                if rec.tes_umur < 18:
                    rec.grup_umur = 'anak'
                else:
                    rec.grup_umur = 'dewasa'

    @api.constrains('tes_umur')
    def cek_umur(self):
        for rec in self:
            if rec.tes_umur <= 5:
                raise ValidationError(_('Umur harus lebih besar dari 5.'))

    @api.multi
    def buka_nama_releted(self):
        return {
            'name': _('Releted'),
            'domain': [('re_nama', '=', self.id)],
            'view_type': 'form',
            'res_model': 'ini.relet',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
                    }

    @api.onchange('dokter_id')
    def set_dokter_gender(self):
        for rec in self:
            if rec.dokter_id:
                rec.dokter_gender = rec.dokter_id.gender

