from openerp import api, fields, models, _

class ResPartner(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	forename = fields.Char('Forename')
	m_name = fields.Char('Maiden Name')
	birthday = fields.Date('Birthday')
	facebook = fields.Char('Facebook Page')
	xing = fields.Char('Xing Page')
	linkedin = fields.Char('LinkedIn Page')
	o_country_id = fields.Many2one('res.country', 'Country of Origin', ondelete='restrict')
	nationality = fields.Many2one('res.country', 'Nationality', ondelete='restrict')
	#language = fields.Many2one('res.country', 'Language', ondelete='restrict')
	diploma = fields.Many2one('diane.diploma', 'Diploma', ondelete='restrict')
	section = fields.Many2one('diane.section', 'Section', ondelete='restrict')
	d_year = fields.Integer('Diploma Year')
	c_name = fields.Char('Company Name')
	c_nace = fields.Char('NACE Code')
	c_street = fields.Char('Company Street')
	c_street2 = fields.Char('Company Street2')
	c_zip = fields.Char('Company ZIP')
	c_city = fields.Char('Company City')
	c_country_id = fields.Many2one('res.country', 'Company Country', ondelete='restrict')
	c_email = fields.Char('Company Email')
	c_phone = fields.Char('Company Phone')
	c_fax = fields.Char('Company Fax')
	c_mobile = fields.Char('Company Mobile')
	h_street = fields.Char('Home Street')
	h_street2 = fields.Char('Home Street2')
	h_zip = fields.Char('Home ZIP')
	h_city = fields.Char('Home City')
	h_country_id = fields.Many2one('res.country', 'Home Country', ondelete='restrict')
	h_email = fields.Char('Home Email')
	h_phone = fields.Char('Home Phone')
	h_fax = fields.Char('Home Fax')
	h_mobile = fields.Char('Home Mobile')		

class ResPartnerTitle(models.Model):
	_name = 'res.partner.title'
	_inherit = 'res.partner.title'

	website_published = fields.Boolean('Website Published')
