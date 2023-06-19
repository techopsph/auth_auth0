# -*- coding: utf-8 -*-
{
    'name': 'Auth0',
    'version': '16.0.0',
    'author': 'Tech Ops PH',
    'summary': 'Auth0 module for Odoo',
    'website': 'https://github.com/techopsph/auth0',
    'description': 'Enables OAuth authentication through Auth0',
    'category': 'Authentication',
    'depends': [
        'auth_oauth','website'
    ],
    'data': [
        'data/data_auth0.xml',
        'data/auto_signup_data.xml',
        'views/auth0_views.xml',
        'views/signup.xml',
        'views/templates.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': "LGPL-3"
}
