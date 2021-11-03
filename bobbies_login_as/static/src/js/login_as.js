odoo.define('bobbies_login_as.LoginAs', function (require) {
    'use strict';

    var core = require('web.core');
    var session = require('web.session');
    var UserMenu = require('web.UserMenu');
    var _t = core._t;

    UserMenu.include({
        willStart: function () {
            var self = this;
            var ready = session.user_has_group(
                'bobbies_login_as.group_login_as')
            .then(hasGroup => {
                self.hasLoginAsGroup = hasGroup;
            });
            return Promise.all([this._super.apply(this, arguments), ready]);
        },
        _onMenuLoginAs: function() {
            return this.do_action({
                type: 'ir.actions.act_window',
                name: _t('Login as'),
                res_model: 'res.users.login_as',
                views: [[false, 'form']],
                target: 'new',
            });
        }
    });

});
