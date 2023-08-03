# -*- coding: utf-8 -*-
{
    'name': 'Api',
    'summary': "Information sur le module",
    'version': '1.0',
    'category': '',
    'author': 'MicenDev',
    'maintainer': '',
    'depends': [
        # Les dependance du module
        'base',
        'mail',
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/test_api_view.xml'
        # Les vues
        # 'views/assets.xml',
    ],
    # Autre parametres du module
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
