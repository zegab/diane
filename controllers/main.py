# -*- coding: utf-8 -*-
import datetime

from openerp import http
from openerp.http import request
from openerp import tools
from openerp.tools.translate import _

class website_diane_account(http.Controller):
    @http.route(['/diane/account_update'], type='http', auth='user', website=True)
    def details(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        values = {
            'error': {},
            'error_message': []
        }

        if post:
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                post.update({'zip': post.pop('zipcode', '')})
                if post['birthday']:
                    del post['birthday']
                raise Warning(post)
                partner.sudo().write(post)
                if redirect:
                    return request.redirect(redirect)
                return request.website.render("diane.thanks", values)

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        titles = request.env['res.partner.title'].sudo().search([])
        nace = request.env['diane.nace'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'titles': titles,
            'nace': nace,
            'redirect': redirect,
        })

        return request.website.render("diane.details", values)

    def details_form_validate(self, data):
        error = dict()
        error_message = []

        #mandatory_billing_fields = ["name", "phone", "email", "street2", "city", "country_id"]

        # Validation
        #for field_name in mandatory_billing_fields:
        #    if not data.get(field_name):
        #        error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        if data.get("vat") and hasattr(request.env["res.partner"], "check_vat"):
            if request.website.company_id.vat_check_vies:
                # force full VIES online check
                check_func = request.env["res.partner"].vies_vat_check
            else:
                # quick and partial off-line checksum validation
                check_func = request.env["res.partner"].simple_vat_check
            vat_country, vat_number = request.env["res.partner"]._split_vat(data.get("vat"))
            if not check_func(vat_country, vat_number):     # simple_vat_check
                error["vat"] = 'error'
        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        return error, error_message
