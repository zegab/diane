from odoo import api, fields, models, _

class Blog(models.Model):
	_name = 'blog.blog'
	_inherit = 'blog.blog'

	sequence = fields.Integer('Sequence')

class BlogPost(models.Model):
	_name = 'blog.post'
	_inherit = 'blog.post'

	sequence = fields.Integer('Sequence')

	#perspectives: add related fields from the partner to display the videos + interview
	alumni_id = fields.Many2one('res.partner', 'Alumni')
	video_url = fields.Char('Video URL')

	forename = fields.Char(related='alumni_id.forename', string='Forename', readonly=True)
	lastname = fields.Char(related='alumni_id.lastname', string='Last Name', readonly=True)
	x_title = fields.Char(related='alumni_id.x_title', string='Title', readonly=True)
	diploma = fields.Many2one(related='alumni_id.diploma', string='Diploma', readonly=True)
	section = fields.Many2one(related='alumni_id.section', string='Section', readonly=True)
	d_year = fields.Integer(related='alumni_id.d_year', string='Diploma Year', readonly=True)
	d_other = fields.Char(related='alumni_id.d_other', string='Other Diplomas', readonly=True)
	function = fields.Char(related='alumni_id.function', string='Company Name', readonly=True)
	c_name = fields.Char(related='alumni_id.c_name', string='Company Name', readonly=True)
