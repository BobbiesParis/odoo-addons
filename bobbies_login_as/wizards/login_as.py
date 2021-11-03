# -*- coding: utf-8 -*-
# (C) 2021 Bobbies (<https://www.bobbies.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class LoginAs(models.Model):
    _name = 'res.users.login_as'
    _description = 'Wizard to login as'

    login_as_user_id = fields.Many2one('res.users', 'Login as')

    def login_as(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/login_as?uid=%s' % self.login_as_user_id.id,
            'target': 'self',
        }
