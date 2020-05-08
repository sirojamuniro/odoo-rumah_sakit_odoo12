from odoo import fields, models, api


class CreateRelet (models.TransientModel):
    _name = 'create.relet'
    _description = 'Wizard Membuat Janji Bertemu'

    tes_nama = fields.Many2one('ini.tes', string="Pasien")
    re_tanggal = fields.Date(string="Tanggal")

    def create_relet(self):
        vals = {
            'tes_nama': self.tes_nama.id,
            're_tanggal': self.re_tanggal

        }
        self.env['ini.relet'].create(vals)