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
	nationality1 = fields.Many2one('res.country', 'Nationality 1', ondelete='restrict')
	nationality2 = fields.Many2one('res.country', 'Nationality 2', ondelete='restrict')
	language1 = fields.Many2one('diane.language', 'Language 1', ondelete='restrict')
	language2 = fields.Many2one('diane.language', 'Language 2', ondelete='restrict')
	diploma = fields.Many2one('diane.diploma', 'Diploma', ondelete='restrict')
	section = fields.Many2one('diane.section', 'Section', ondelete='restrict')
	d_year = fields.Integer('Diploma Year')
	d_other = fields.Char('Other Diplomas')
	c_name = fields.Char('Company Name')
	c_nace = fields.Many2one('diane.nace', 'NACE Code', ondelete='restrict')
	c_street = fields.Char('Company Street')
	c_street2 = fields.Char('Company Street2')
	c_zip = fields.Char('Company ZIP')
	c_city = fields.Char('Company City')
	c_country_id = fields.Many2one('res.country', 'Company Country', ondelete='restrict')
	c_date_joined = fields.Date('Date Joined')
	c_email = fields.Char('Company Email')
	c_phone = fields.Char('Company Phone')
	c_web = fields.Char('Company Website')
	hr_name = fields.Char('HR Name')
	hr_phone = fields.Char('HR Phone')
	hr_email = fields.Char('HR Email')
	h_street = fields.Char('Home Street')
	h_street2 = fields.Char('Home Street2')
	h_zip = fields.Char('Home ZIP')
	h_city = fields.Char('Home City')
	h_country_id = fields.Many2one('res.country', 'Home Country', ondelete='restrict')
	h_email = fields.Char('Home Email')
	h_phone = fields.Char('Home Phone')
	h_mobile = fields.Char('Home Mobile')

	annuaire_ok = fields.Boolean('Publication in Alumni directory')
	sponsoring_ok = fields.Boolean('Allow to contact for sponsoring requests')
	recruitment_ok = fields.Boolean('Allow recruiters to contact me')
	map_ok = fields.Boolean('Allow to be identified on the map')
	hr_contact_ok = fields.Boolean('Allow us to contact the HR of your company')

class ResPartnerTitle(models.Model):
	_name = 'res.partner.title'
	_inherit = 'res.partner.title'

	website_published = fields.Boolean('Website Published')
