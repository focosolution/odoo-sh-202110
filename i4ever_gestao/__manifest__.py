# -*- coding: utf-8 -*-
{
    'name': "Gestão Image4ever",  # Module title
    'summary': "Gerenciar Pedidos, Serviços e Pagamentos",  # Module subtitle phrase
    'description': """
Sistema de Controle Interno
===========================
Este Sistema se propõe a ajudar no controle de Pedidos, Serviços e Pagamentos. O objetivo é economizar tempo das pessoas
envolvidas, além de garantir uma maior qualidade nas tarefas desempenhadas.
    """,  # Supports reStructuredText(RST) format
    'author': "Paulo Roberto G. Freire",
    'website': "http://focosolution.com",
    'category': 'Image4ever',
    'version': '1.0.4',
    'depends': ['base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'wizards/concluir_tarefa.xml',
        'views/i4ever_tipo_servico.xml',
        'views/i4ever_pedido.xml',
        'views/i4ever_servico_filtrado.xml',
        'views/i4ever_servico_producao.xml',
        'views/menu.xml',
    ],

    # This demo data files will be loaded if db initialize with demo data (commented because file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
}
