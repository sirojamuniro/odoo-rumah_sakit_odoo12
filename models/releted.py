from odoo import models, fields, api, _

class IniRelasi(models.Model):
    _name = 'ini.relet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Ini Releted'
    _order = "id desc"


    re_id = fields.Many2one('ini.tes', string='nama pasien', required=True)
    re_umur= fields.Integer(string='umur' ,related="re_id.tes_umur")
    name_seq = fields.Char(string='Kode', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: ('New'))
    re_tanggal= fields.Date(string='Tanggal', required=True)
    re_catatan=fields.Text(string='catatan', default='Ini Catatan')
    re_dokter = fields.Text(string="catatan")
    re_obat = fields.Text(string="catatan")
    re_lines = fields.One2many('ini.relet.lines', 'relet_id', string="Detail Obat")

    state = fields.Selection([
        ('draft', 'Draf'),
        ('confirm', 'Konfirmasi'),
        ('done', 'Selesai'),
        ('cancel', 'Batalkan'),
    ], string='Status', readOnly=True, default='draft')

    class ReletLiness(models.Model):
        _name = 'ini.relet.lines'
        _description = 'Detail Obat'
        # produc.produc mengambil dari database odoo yang telah disediakan
        product_id = fields.Many2one('product.product', string='Obat')
        product_qty = fields.Integer(string='Jumlah')
        relet_id = fields.Many2one('ini.relet', string='Appointment ID')
        name = fields.Char(string='Releted ID', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name_seq', ('New')) == ('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('ini.relet.sequence') or ('New')
        return super(inireleted, self).create(vals)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

