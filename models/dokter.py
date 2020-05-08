from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'ini.dokter'
    _description = 'Master Dokter'

    name = fields.Char(string='Nama', required=True)
    gender = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan')
    ], string='Jenis Kelamin', default='male')
    user_id = fields.Many2one('res.users', string='Relasi User')
# res.users merupakan bawaan odoo dalam database jadi tinggal memanggilnya saja


