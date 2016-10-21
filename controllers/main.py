# -*- coding: utf-8 -*-
import datetime

from openerp import http
from openerp.http import request
from openerp import tools
from openerp.tools.translate import _
import random

class website_diane_account(http.Controller):
    @http.route(['/diane/alumni_map'], type='http', auth='user', website=True)
    def show_map(self, redirect=None, **post):
        values={
            'result':{},
            'random':random,
        }

        if post:
            if post['address'] == 'a':
                request.env.cr.execute("""
                    SELECT perso_anciens_ok, p.name as name, forename, lastname, m_name, s.name AS section, section AS section_id, d.name AS diploma,diploma AS diploma_id, d_year, partner_latitude AS lat, partner_longitude AS lng
                    FROM res_partner p
                    LEFT JOIN diane_section s ON p.section = s.id
                    LEFT JOIN diane_diploma d ON p.diploma = d.id
                """,)
            if post['address'] == 'c':
                request.env.cr.execute("""
                    SELECT pro_anciens_ok, p.name as name, forename, lastname, m_name, s.name AS section, section AS section_id, d.name AS diploma,diploma AS diploma_id, d_year, c_latitude AS lat, c_longitude AS lng
                    FROM res_partner p
                    LEFT JOIN diane_section s ON p.section = s.id
                    LEFT JOIN diane_diploma d ON p.diploma = d.id
                """, )
            if post['address'] == 'h':
                request.env.cr.execute("""
                    SELECT perso_anciens_ok, p.name as name, forename, lastname, m_name, s.name AS section, section AS section_id, d.name AS diploma,diploma AS diploma_id, d_year, h_latitude AS lat, h_longitude AS lng
                    FROM res_partner p
                    LEFT JOIN diane_section s ON p.section = s.id
                    LEFT JOIN diane_diploma d ON p.diploma = d.id
                """, )
            values.update({'address': post['address']})
        else:
            request.env.cr.execute("""
                SELECT perso_anciens_ok, p.name as name, forename, lastname, m_name, s.name AS section, section AS section_id, d.name AS diploma,diploma AS diploma_id, d_year, partner_latitude AS lat, partner_longitude AS lng
                FROM res_partner p
                LEFT JOIN diane_section s ON p.section = s.id
                LEFT JOIN diane_diploma d ON p.diploma = d.id
            """, )

        result = request.env.cr.dictfetchall()
        values.update({'result':result})
        return request.website.render("diane.alumni_map", values)

    @http.route(['/diane/alumni_search'], type='http', auth='user', website=True)
    @http.route(['/diane/alumni_search_result'], type='http', auth='user', website=True)
    def search(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        sections = request.env['diane.section'].sudo().search([])
        diplomas = request.env['diane.diploma'].sudo().search([])

        values={
            'sections': sections,
            'diplomas': diplomas,
            'partner': partner,
            'result':{},
            'message':"",
        }

        if post:
                diploma = int(post['diploma']) if post['diploma'].isdigit() else False
                section = int(post['section']) if post['section'].isdigit() else False
                d_year = int(post['d_year']) if post['d_year'].isdigit() else False

                if diploma and section and d_year:
                    alumni = request.env['res.partner'].sudo().search([('diploma','=',diploma),('section','=',section),('d_year','=',d_year)])
                    if alumni:
                        alumni_ids = [a.id for a in alumni]
                        request.env.cr.execute("""
                            SELECT forename, lastname, m_name, s.name AS section, section AS section_id, d.name AS diploma,diploma AS diploma_id, d_year
                            FROM res_partner p
                            INNER JOIN diane_section s ON p.section = s.id
                            INNER JOIN diane_diploma d ON p.diploma = d.id
                            WHERE p.id IN %s
                        """,(tuple(alumni_ids),))
                        result = request.env.cr.dictfetchall()
                        values.update({'result':result})
                        return request.website.render("diane.alumni_search_result", values)
                else:
                    values.update({'message':"Aucun Résultat!"})

        return request.website.render("diane.alumni_search", values)


    @http.route(['/diane/account_update'], type='http', auth='user', website=True)
    def details(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        values = {
            'error': {},
            'error_message': [],
        }

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

        if post:
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            #activate if birthday is needed
            #if post['birthday'] == "":
            #        post['birthday']=None
            if post['c_date_joined'] == "":
                    post['c_date_joined']=None
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
            if 'd_year'in post and not post['d_year'].isdigit():
                post['d_year']=False

            values.update(post)
            if not error:
                post.update({'zip': post.pop('zipcode', ''),'self_updated':True})
                #raise Warning(post)
                partner.sudo().write(post)
                if redirect:
                    return request.redirect(redirect)
                values.update({'message':"Merci d'avoir actualisé vos données!"})
                return request.website.render("diane.alumni_search", values)


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
