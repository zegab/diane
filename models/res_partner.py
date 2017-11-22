try:
	import simplejson as json
except ImportError:
	import json     # noqa
import urllib
import datetime

from odoo import osv, fields
from odoo import tools,api, fields, models, _
from odoo.tools.translate import _

def geo_find(addr):
	url = 'https://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='
	url += urllib.quote(addr.encode('utf8'))

	try:
		result = json.load(urllib.urlopen(url))
	except Exception, e:
		raise osv.except_osv(_('Network error'),
							 _('Cannot contact geolocation servers. Please make sure that your internet connection is up and running (%s).') % e)
	if result['status'] != 'OK':
		return None

	try:
		geo = result['results'][0]['geometry']['location']
		return float(geo['lat']), float(geo['lng'])
	except (KeyError, ValueError):
		return None


def geo_query_address(street=None, zip=None, city=None, state=None, country=None):
	if country and ',' in country and (country.endswith(' of') or country.endswith(' of the')):
		# put country qualifier in front, otherwise GMap gives wrong results,
		# e.g. 'Congo, Democratic Republic of the' => 'Democratic Republic of the Congo'
		country = '{1} {0}'.format(*country.split(',', 1))
	return tools.ustr(', '.join(filter(None, [street,
											  ("%s %s" % (zip or '', city or '')).strip(),
											  state,
											  country])))

class ResPartner(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	forename = fields.Char('Forename')
	lastname = fields.Char('Last name')
	m_name = fields.Char('Maiden Name')
	x_title = fields.Char('Title')
	alumni = fields.Boolean('Alumni')
	birthday = fields.Date('Birthday')
	social_network = fields.Char('Other Social Network Link')
	facebook = fields.Char('Facebook Page')
	xing = fields.Char('Xing Page')
	linkedin = fields.Char('LinkedIn Page')
	viadeo = fields.Char('Viadeo Page')
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
	c_nace1 = fields.Many2one('diane.nace', 'NACE Code', ondelete='restrict')
	c_nace2 = fields.Many2one('diane.nace', 'NACE Code', ondelete='restrict')
	c_nace3 = fields.Many2one('diane.nace', 'NACE Code', ondelete='restrict')
	c_nace4 = fields.Many2one('diane.nace', 'NACE Code', ondelete='restrict')
	c_nace_text = fields.Char('NACE Code (Text)')
	c_street = fields.Char('Company Street')
	c_street2 = fields.Char('Company Street2')
	c_zip = fields.Char('Company ZIP')
	c_city = fields.Char('Company City')
	c_country_id = fields.Many2one('res.country', 'Company Country', ondelete='restrict')
	c_date_joined = fields.Date('Date Joined')
	c_email = fields.Char('Company Email')
	c_phone = fields.Char('Company Phone')
	c_mobile = fields.Char('Company Mobile')
	c_web = fields.Char('Company Website')
	c_latitude = fields.Float('Company Latitude')
	c_longitude = fields.Float('Company Longitude')
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
	h_latitude = fields.Float('Home Latitude')
	h_longitude = fields.Float('Home Longitude')
	annuaire_ok = fields.Boolean('Publication in Alumni directory')
	sponsoring_ok = fields.Boolean('Allow to contact for sponsoring requests')
	recruitment_ok = fields.Boolean('Allow recruiters to contact me')
	map_ok = fields.Boolean('Allow to be identified on the map')
	hr_contact_ok = fields.Boolean('Allow us to contact the HR of your company')
	perso_annuaire_ok = fields.Boolean('Personal data in Alumni Directory')
	pro_annuaire_ok = fields.Boolean('Professional data in Alumni Directory')
	perso_anciens_ok = fields.Boolean('Personal data available to Anciens')
	pro_anciens_ok = fields.Boolean('Professional data available to Anciens')
	pro_stage_ok = fields.Boolean('Professional Email for Stage Requests')
	hr_stage_ok = fields.Boolean('HR Email for Stage Requests')
	date_entry = fields.Date('Entry Date')
	date_exit = fields.Date('Exit Date')
	failed = fields.Boolean('No Diploma!')
	gender = fields.Selection([('m', 'M'), ('f', 'F')], string='Gender')
	self_updated = fields.Boolean('Self Updated')
	deceased = fields.Boolean('Deceased')
	messages_sent = fields.Integer('Messages sent')
	messages_limit = fields.Integer('Limit of messages')

	@api.onchange('c_nace1','c_nace2','c_nace3','c_nace4',)
	def _onchange_nace(self):
		if self.c_nace4:
			self.c_nace = self.c_nace4
		if self.c_nace3:
			self.c_nace = self.c_nace3
			self.c_nace4 = False
			return {'domain': {'c_nace4': [('parent_id', '=', self.c_nace3.id)]}}
		if self.c_nace2:
			self.c_nace = self.c_nace2
			self.c_nace3 = False
			self.c_nace4 = False
			return {'domain': {'c_nace3': [('parent_id', '=', self.c_nace2.id)]}}
		if self.c_nace1:
			self.c_nace = self.c_nace1
			self.c_nace2 = False
			self.c_nace3 = False
			self.c_nace4 = False
			return {'domain': {'c_nace2': [('parent_id', '=', self.c_nace1.id)]}}

	def geo_localize(self, context=None):
		# Don't pass context to browse()! We need country names in english below
		for partner in self:
			if partner.city:
				result = geo_find(geo_query_address(street=partner.street,
													zip=partner.zip,
													city=partner.city,
													state=partner.state_id.name,
													country=partner.country_id.name))
				if result:
					partner.write({
						'partner_latitude': result[0],
						'partner_longitude': result[1],
						'date_localization': datetime.date.today(),
					})
			if partner.c_city:
				c_result = geo_find(geo_query_address(street=partner.c_street,
													zip=partner.c_zip,
													city=partner.c_city,
													country=partner.c_country_id.name))
				if c_result:
					partner.write({
						'c_latitude': c_result[0],
						'c_longitude': c_result[1],
					})
			if partner.h_city:
				h_result = geo_find(geo_query_address(street=partner.h_street,
													  zip=partner.h_zip,
													  city=partner.h_city,
													  country=partner.h_country_id.name))
				if h_result:
					partner.write({
						'h_latitude': h_result[0],
						'h_longitude': h_result[1],
					})
		return True

	def search_xing(self):
		url = "https://www.xing.com/search/members?hdr=1&keywords=%s" % (self.name.replace(' ', '+'))
		return {'type': 'ir.actions.act_url',
				  'name': "Social Network",
				  'target': 'new',
				  'url': url,
				  }

	def search_linkedin(self):
		url = "https://www.linkedin.com/search/results/index/?keywords=%s&origin=GLOBAL_SEARCH_HEADER" % (self.name.replace(' ', '%20'))
		return {'type': 'ir.actions.act_url',
				  'name': "Social Network",
				  'target': 'new',
				  'url': url,
				  }

	def search_viadeo(self):
		url = "http://www.viadeo.com/en/search/#/?q=%s" % (self.name.replace(' ', '%20'))
		return {'type': 'ir.actions.act_url',
				  'name': "Social Network",
				  'target': 'new',
				  'url': url,
				  }

	def search_facebook(self):
		url = "https://www.facebook.com/search/top/?q=%s" % (self.name.replace(' ', '%20'))
		return {'type': 'ir.actions.act_url',
				  'name': "Social Network",
				  'target': 'new',
				  'url': url,
				  }

class ResPartnerTitle(models.Model):
	_name = 'res.partner.title'
	_inherit = 'res.partner.title'

	website_published = fields.Boolean('Website Published')


