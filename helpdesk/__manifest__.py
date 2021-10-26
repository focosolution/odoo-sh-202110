# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Solution",
    'summary': "Gerenciar chamados do Helpdesk com o intuito de solucionar problemas",
    'sequence': -10,
    'description': """
Sistema de Helpdesk
===================
Este Sistema se propõe a ajudar no controle de Chamados do Helpdesk no formato multiempresa. O objetivo é 
centralizar todos os problemas e necessidades dos clientes em único lugar, facilitando assim a identificação 
e solução dos problemas pelos colaboradores.""",
    'author': "FocoSolution",
    'website': "http://focosolution.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'FSHelpdesk',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts',],
    # always loaded
    'data': [
        'security/groups.xml',
        'security/security_rules.xml',
        'security/ir.model.access.csv',
        'views/helpdesk_categoria.xml',
        'views/helpdesk_tipo_chamado.xml',
        'wizards/criar_chamado.xml',
        'wizards/interagir_chamado.xml',
        'wizards/criar_usuario.xml',
        'views/helpdesk_item.xml',
        'views/helpdesk_chamado.xml',
        'views/res_partner_views.xml',
        'views/res_users_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    # This demo data files will be loaded if db initialize with demo data
    # (commented because file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
}
