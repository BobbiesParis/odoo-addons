# -*- coding: utf-8 -*-
# (C) 2021 Bobbies (<https://www.bobbies.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from uuid import uuid4

from odoo.http import redirect_with_hash, request, route

from odoo.addons.web.controllers.main import Home, Session

SCOPE = 'login_as'

def _login_as(uid):
    request.session.pre_uid = int(uid)
    request.session.finalize()
    request.context = request.session.context


class LoginAsHome(Home):

    @route('/web/login_as', type='http', auth='user', sitemap=False)
    def login_as(self, uid=None, **kwargs):
        key = False
        user = request.env.user
        if uid and user.has_group(
                'bobbies_login_as.group_login_as'):
            if not request.httprequest.cookies.get(SCOPE):
                key = user.env['res.users.apikeys']._generate(
                    SCOPE, uuid4().hex)
            _login_as(uid)
        response = redirect_with_hash(
            self._login_redirect(request.session.uid))
        if key:
            response.set_cookie(SCOPE, key)
        return response


class LoginAsSession(Session):

    @route('/web/session/logout', type='http', auth="none")
    def logout(self, redirect='/web'):
        uid = self._get_origin_user_id()
        if uid:
            _login_as(uid)
            response = redirect_with_hash('/web')
        else:
            response = super().logout(redirect)
        if request.httprequest.cookies.get(SCOPE):
            response.delete_cookie(SCOPE)
        return response

    def _get_origin_user_id(self):
        key = request.httprequest.cookies.get(SCOPE)
        if key and request.env:
            result = request.env['res.users.apikeys']._check_credentials(
                scope=SCOPE, key=key)
            if result:
                for apikey in request.env['res.users.apikeys'].sudo().search([
                    ('user_id', '=', result),
                    ('scope', '=', SCOPE),
                ]):
                    apikey._remove()
            return result
