# (C) 2021 Bobbies (<https://www.bobbies.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Login as another user",
    "version": "19.0.0.1",
    "license": "LGPL-3",
    "category": "Tools",
    "author": "Bobbies",
    "website": "https://bobbies.com",
    "depends": [
        "web",
    ],
    "data": [
        "security/login_as_security.xml",
        "security/ir.model.access.csv",
        "wizards/login_as_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "bobbies_login_as/static/src/js/login_as.js",
            "bobbies_login_as/static/src/xml/login_as.xml",
        ],
    },
    "installable": True,
    "application": False,
}
