# (C) 2021 Bobbies (<https://www.bobbies.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from uuid import uuid4

from odoo import fields
from odoo.http import request, route

from odoo.addons.web.controllers.home import Home
from odoo.addons.web.controllers.session import Session

SCOPE = "login_as"


def _login_as(uid):
    request.session["pre_uid"] = int(uid)
    request.session["pre_login"] = request.env["res.users"].sudo().browse(int(uid)).login
    request.session.finalize(request.env)
    request.update_env(context=request.session.context)
    request.params["login_as_success"] = True


class LoginAsHome(Home):
    @route("/web/login_as", type="http", auth="user", sitemap=False)
    def login_as(self, uid=None, **kwargs):
        key = False
        user = request.env.user
        if uid and uid != "False" and user.has_group("bobbies_login_as.group_login_as"):
            if not request.httprequest.cookies.get(SCOPE):
                hours = int(
                    request.env["ir.config_parameter"]
                    .sudo()
                    .get_param("bobbies_login_as.apikey_expiration_hours", default="1")
                )
                expiration_date = fields.Datetime.add(fields.Datetime.now(), hours=hours)
                key = user.env["res.users.apikeys"]._generate(SCOPE, uuid4().hex, expiration_date)
            _login_as(uid)
        response = request.redirect(self._login_redirect(request.session.uid))
        if key:
            response.set_cookie(SCOPE, key)
        return response


class LoginAsSession(Session):
    @route("/web/session/logout", type="http", auth="none")
    def logout(self, redirect="/web"):
        uid = self._get_origin_user_id()
        if uid:
            _login_as(uid)
            response = request.redirect("/web")
        else:
            response = super().logout(redirect=redirect)
        if request.httprequest.cookies.get(SCOPE):
            response.delete_cookie(SCOPE)
        return response

    def _get_origin_user_id(self):
        key = request.httprequest.cookies.get(SCOPE)
        if key and request.env:
            uid = request.env["res.users.apikeys"]._check_credentials(scope=SCOPE, key=key)
            if uid:
                for apikey in (
                    request.env["res.users.apikeys"]
                    .sudo()
                    .search(
                        [
                            ("user_id", "=", uid),
                            ("scope", "=", SCOPE),
                        ]
                    )
                ):
                    apikey._remove()
            return uid
