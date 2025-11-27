import {Component, useState} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {registry} from "@web/core/registry";
import {user} from "@web/core/user";

export class LoginAsSystrayItem extends Component {
  static props = [];
  static template = "bobbies_login_as.SystrayItem";

  setup() {
    const self = this;
    self.state = useState({canLoginAs: false});
    user.hasGroup("bobbies_login_as.group_login_as").then(function (canLoginAs) {
      self.state.canLoginAs = canLoginAs;
    });
  }

  onClick() {
    this.env.services.action.doAction({
      type: "ir.actions.act_window",
      name: _t("Login as"),
      res_model: "res.users.login_as",
      views: [[false, "form"]],
      target: "new",
    });
  }
}

registry.category("systray").add("LoginAs", {Component: LoginAsSystrayItem}, {sequence: 10});
