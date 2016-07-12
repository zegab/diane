from openerp import api, fields, models, _

class Blog(models.Model):
	_name = 'blog.blog'
	_inherit = 'blog.blog'

	sequence = fields.Integer('Sequence')

class BlogPost(models.Model):
	_name = 'blog.post'
	_inherit = 'blog.post'

	sequence = fields.Integer('Sequence')