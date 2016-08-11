# -*- coding: utf-8 -*-
import datetime

from openerp import http
from openerp.http import request
from openerp import tools
from openerp.tools.translate import _

class website_diane_search(http.Controller):
    @http.route(['/diane/alumni_search'], type='http', auth='user', website=True)
    def search(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        values = {}

        if post:
            diploma = request.env['diane.diploma'].search([('name','=',post['diploma'])])
            section = request.env['diane.section'].search([('name','=',post['section'])])
            try:
                d_year = int(post['d_year'])
            except:
                d_year = 0
            alumni = request.env['res.partner'].search([('diploma','=',diploma),('section','=',section),('d_year','=',d_year)])
            ids = [a.id for a in alumni]
            request.cr.execute("""
                SELECT p.forename, p.lastname, p.m_name, s.name, d.name, d_year
                FROM res_partner p
                INNER JOIN diane_section s ON p.section = s.id
                INNER JOIN diane_diploma d ON p.diploma = d.id
                WHERE p.id IN %s
            """,(ids) )
            result = cr.fetchall()
            return request.website.render("diane.search_result", result)

        countries = request.env['res.country'].sudo().search([]).sorted(key=lambda r:r.display_name)
        states = request.env['res.country.state'].sudo().search([])
        titles = request.env['res.partner.title'].sudo().search([])
        nace = request.env['diane.nace'].sudo().search([])
        sections = request.env['diane.section'].sudo().search([])
        diplomas = request.env['diane.diploma'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'titles': titles,
            'nace': nace,
            'sections': sections,
            'diplomas': diplomas,
            'redirect': redirect,
        })

        return request.website.render("diane.details", values)



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
            #activate if birthday is needed
            #if post['birthday'] == "":
            #        post['birthday']=None
            if not 'recruitment_ok' in post:
                post['recruitment_ok']=False
            if not 'hr_contact_ok' in post:
                post['hr_contact_ok']=False
            if not 'perso_annuaire_ok' in post:
                post['perso_annuaire_ok']=False
            if not 'pro_annuaire_ok' in post:
                post['pro_annuaire_ok']=False
            if not 'perso_anciens_ok' in post:
                post['perso_anciens_ok']=False
            if not 'pro_anciens_ok' in post:
                post['pro_anciens_ok']=False
            if not 'pro_stage_ok' in post:
                post['pro_stage_ok']=False
            if not 'hr_stage_ok' in post:
                post['hr_stage_ok']=False
            #add here all the other checkboxes

            values.update(post)
            if not error:
                post.update({'zip': post.pop('zipcode', '')})
                partner.sudo().write(post)
                if redirect:
                    return request.redirect(redirect)
                return request.website.render("diane.thanks", values)

        countries = request.env['res.country'].sudo().search([]).sorted(key=lambda r:r.display_name)
        states = request.env['res.country.state'].sudo().search([])
        titles = request.env['res.partner.title'].sudo().search([])
        nace = request.env['diane.nace'].sudo().search([])
        sections = request.env['diane.section'].sudo().search([])
        diplomas = request.env['diane.diploma'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'titles': titles,
            'nace': nace,
            'sections': sections,
            'diplomas': diplomas,
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
