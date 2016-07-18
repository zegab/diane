from openerp import api, fields, models, _

class Diploma(models.Model):
    _name = 'diane.diploma'
    name = fields.Char('Diploma', translate=True)

class Section(models.Model):
    _name = 'diane.section'
    name = fields.Char('Section', translate=True)

class NACE(models.Model):
    _name = 'diane.nace'
    name = fields.Char('NACE Description')
    code = fields.Char('NACE Code')


class Language(models.Model):
    _name = 'diane.language'
    name = fields.Char('Language', translate=True)