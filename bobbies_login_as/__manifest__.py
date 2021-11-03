# -*- coding: utf-8 -*-
# (C) 2021 Bobbies (<https://www.bobbies.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': 'Login as another user',
    'version': '0.1',
    'license': 'LGPL-3',
    'category': 'Tools',
    'description': """
This module allows to login as another user in back-office / portal / website.

For example, this option could be useful to check what's displayed for your employees / customers.
    """,
    'author': 'Bobbies',
    'website': 'https://bobbies.com',
    'depends': [
        'web',
    ],
    'data': [
        'security/login_as_security.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'wizards/login_as_views.xml',
    ],
    'qweb': [
        'static/src/xml/login_as.xml',
    ],
    'installable': True,
    'application': True,
}
