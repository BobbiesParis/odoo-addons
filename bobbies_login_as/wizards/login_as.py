# (C) 2021 Bobbies (<https://www.bobbies.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class LoginAs(models.TransientModel):
    _name = "res.users.login_as"
    _description = "Wizard to login as"

    login_as_user_id = fields.Many2one("res.users", "Login as", required=True)

    def login_as(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/login_as?uid={self.login_as_user_id.id}",
            "target": "self",
        }
