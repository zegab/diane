from odoo import api, fields, models, _

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
    level = fields.Integer('Level')
    parent_id = fields.Many2one('diane.nace',string='Parent NACE',ondelete='restrict',index=True)
    child_ids = fields.One2many('diane.nace', 'parent_id',string='Child NACE')
    sequence = fields.Integer('Sequence')
    _parent_store = True
    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')

    def name_get(self):
        return [(nace.id, '%s%s' % (nace.code and '[%s] ' % nace.code or '', nace.name))
                for nace in self]



class Language(models.Model):
    _name = 'diane.language'
    name = fields.Char('Language', translate=True)
