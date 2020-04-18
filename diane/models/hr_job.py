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
        for send_to in partners:
            template = self.env.ref('diane.email_template_alumni_job_notification')
            template.with_context(
                lang=send_to.lang,
                send_to_email=send_to.email,
                send_to_name=send_to.name,
                send_to_id=send_to.id,
            ).send_mail(self.id, force_send=False, raise_exception=True)

        body = "The job notification has been sent following %s partners: %s" %(len(partners), [p.name for p in partners])

        values = {
            'author_id': self.env.uid,
            'body': body,
            'message_type': 'comment',
            'subtype': 'mail.mt_comment',
        }
        self.message_post(**values)

        return True