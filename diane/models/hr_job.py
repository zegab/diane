from odoo import tools,api, fields, models, _
from odoo.tools.translate import _

class hr_job(models.Model):
    _name = 'hr.job'
    _inherit = 'hr.job'

    _defaults = {
        'address_id': False
    }

    _order = "create_date desc"

    section_id = fields.Many2one('diane.section', 'Section', ondelete='restrict')

    def send_job_notification(self):
        partners = self.env['res.partner'].search([
            ('send_job_notification','=', True),
            '|',
                ('send_job_section', '=', self.section_id.id),
                ('send_job_section', '=', False),
        ])

        template = self.env.ref('diane.email_template_alumni_job_notification')
        template.send_mail(self.id, force_send=False, raise_exception=True, email_values={'recipient_ids': [(4, pid) for pid in [p.id for p in partners]]})

        partner_string = '<br/>'.join([p.name for p in partners])
        body = "<p>The job notification has been sent to the following %s partners: <br/> %s</p>" %(len(partners), partner_string)

        values = {
            'author_id': self.env.uid,
            'body': body,
            'message_type': 'comment',
            'subtype_xmlid': 'mail.mt_comment',
        }
        self.message_post(**values)

        return True