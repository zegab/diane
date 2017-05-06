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
        partner = request.env['res.users'].browse(request.uid).partner_id
        sections = request.env['diane.section'].sudo().search([])
        diplomas = request.env['diane.diploma'].sudo().search([])

        values={
            'sections': sections,
            'diplomas': diplomas,
            'partner': partner,
            'result':{},
            'message':"",
            'random': random,
            'default_diploma': partner.diploma.id,
            'default_section': partner.section.id,
            'default_d_year': partner.d_year,
        }

        if post:
            diploma = int(post['diploma']) if post['diploma'].isdigit() else False
            section = int(post['section']) if post['section'].isdigit() else False
            d_year = int(post['d_year']) if post['d_year'].isdigit() else False

            values.update({
                'default_diploma': diploma,
                'default_section': section,
                'default_d_year': d_year,
            })

            search_domain = []

            if d_year:
                search_domain.append(('d_year','=',d_year))
            if diploma:
                search_domain.append(('diploma', '=', diploma))
            if section:
                search_domain.append(('section', '=', section))


            filtered = request.env['res.partner'].sudo().search(search_domain)
            if filtered:
                p_ids = [p.id for p in filtered]
            else:
                p_ids = [p.id for p in request.env['res.partner'].sudo().search([('alumni', '=', True)])]


            if post['address'] == 'a':
                request.env.cr.execute("""
                    SELECT perso_anciens_ok, p.name as name, forename, lastname, m_name, s.name AS section, section AS section_id, d.name AS diploma,diploma AS diploma_id, d_year, partner_latitude AS lat, partner_longitude AS lng, p.id,
                    CASE WHEN p.email IS NOT NULL THEN True
                                ELSE False
                                END AS has_email
                    FROM res_partner p
                    LEFT JOIN diane_section s ON p.section = s.id
                    LEFT JOIN diane_diploma d ON p.diploma = d.id
                    WHERE p.id IN %s
                """,[tuple(p_ids)])
            if post['address'] == 'c':
                request.env.cr.execute("""
                    SELECT pro_anciens_ok, p.name as name, forename, lastname, m_name, s.name AS section, section AS section_id, d.name AS diploma,diploma AS diploma_id, d_year, c_latitude AS lat, c_longitude AS lng, p.id,
                    CASE WHEN p.email IS NOT NULL THEN True
                                ELSE False
                                END AS has_email
                    FROM res_partner p
                    LEFT JOIN diane_section s ON p.section = s.id
                    LEFT JOIN diane_diploma d ON p.diploma = d.id
                    WHERE p.id IN %s
                """,[tuple(p_ids)])
            if post['address'] == 'h':
                request.env.cr.execute("""
                    SELECT perso_anciens_ok, p.name as name, forename, lastname, m_name, s.name AS section, section AS section_id, d.name AS diploma,diploma AS diploma_id, d_year, h_latitude AS lat, h_longitude AS lng, p.id,
                    CASE WHEN p.email IS NOT NULL THEN True
                                ELSE False
                                END AS has_email
                    FROM res_partner p
                    LEFT JOIN diane_section s ON p.section = s.id
                    LEFT JOIN diane_diploma d ON p.diploma = d.id
                    WHERE p.id IN %s
                """,[tuple(p_ids)])
            values.update({'address': post['address']})
        else:
            request.env.cr.execute("""
                SELECT perso_anciens_ok, p.name as name, forename, lastname, m_name, s.name AS section, section AS section_id, d.name AS diploma,diploma AS diploma_id, d_year, partner_latitude AS lat, partner_longitude AS lng, p.id,
                CASE WHEN p.email IS NOT NULL THEN True
                                ELSE False
                                END AS has_email
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

        if post and 'msg_body' not in post:
                diploma = int(post['diploma']) if post['diploma'].isdigit() else False
                section = int(post['section']) if post['section'].isdigit() else False
                d_year = int(post['d_year']) if post['d_year'].isdigit() else False

                if diploma and section and d_year:
                    alumni = request.env['res.partner'].sudo().search([('diploma','=',diploma),('section','=',section),('d_year','=',d_year)])
                    if alumni:
                        alumni_ids = [a.id for a in alumni]
                        request.env.cr.execute("""
                            SELECT
                            forename,
                            lastname,
                            m_name,
                            s.name AS section,
                            section AS section_id,
                            d.name AS diploma,
                            diploma AS diploma_id,
                            d_year,
                            p.id,
                            CASE WHEN p.email IS NOT NULL THEN True
                                ELSE False
                                END AS has_email
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


    @http.route(['/diane/send_message'], type='http', auth='user', website=True)
    def send_message(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        sections = request.env['diane.section'].sudo().search([])
        diplomas = request.env['diane.diploma'].sudo().search([])

        values = {
            'error': {},
            'error_message': [],
            'sections': sections,
            'diplomas': diplomas,
            'partner': partner,
        }

        if post:
            if post['msg_body']:
                if not partner.alumni:
                    values.update({'message': "Uniquement les Alumnis peuvent utiliser ce service"})
                    return request.website.render("diane.alumni_search", values)
                if (partner.messages_sent > partner.messages_limit and partner.messages_limit != 0) or (partner.messages_sent > 10 and partner.messages_limit == 0):
                    values.update({'message': "Vous avez atteint la limite d'envoi, veuillez nous envoyer un message par le formulaire de contact pour augmenter votre limite!"})
                    return request.website.render("diane.alumni_search", values)
                else:
                    send_to = request.env['res.partner'].sudo().browse(int(post['p_id']))
                    try:
                        template = request.env.ref('diane.email_template_alumni_contact').sudo()
                        template.with_context(
                            lang=send_to.lang,
                            body=post['msg_body'],
                            send_to_email = send_to.email,
                            send_to_name = send_to.name,
                            send_to_id= send_to.id,
                        ).send_mail(partner.id, force_send=False, raise_exception=True)
                        partner.write({'messages_sent':partner.messages_sent+1})
                    except:
                        values.update({'message': "Échec de l'envoi. Veuillez utiliser le formulaire de contact pour nous faire remonter le problème."})
                        return request.website.render("diane.alumni_search", values)

                    values.update({'message': "Votre message a été envoyé avec succès!"})
                    messages = request.env['mail.mail'].sudo().search(
                        [('model', '=', 'res.partner'), ('res_id', '=', partner.id)])
                    values.update({
                        'messages': messages,
                        'partner': partner,
                    })
                    return request.website.render("diane.alumni_message", values)

    @http.route(['/diane/alumni_message'], type='http', auth='user', website=True)
    def message_read(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        messages= request.env['mail.mail'].sudo().search([('model','=','res.partner'),('res_id','=',partner.id)])

        values={
            'messages': messages,
            'partner': partner,
        }
        return request.website.render("diane.alumni_message", values)



