from openerp import api, fields, models, _

class Diploma(models.Model):
    _name = 'diane.diploma'
    name = fields.Char('Diploma')

class Section(models.Model):
    _name = 'diane.section'
    name = fields.Char('Section')

class NACE(models.Model):
    _name = 'diane.nace'
    name = fields.Char('NACE Description')
    code = fields.Char('NACE Code')