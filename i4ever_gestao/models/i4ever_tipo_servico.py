# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TipoServico(models.Model):
    _name = 'i4ever.tipo.servico'
    _description = 'Tipo de Serviço'
    _order = 'sequencial'

    name = fields.Char('Descrição', required=True, index=True)

    percentual_comissao = fields.Float('Percentual Comissão', digits=(5,2), )
    is_producao = fields.Boolean('Serviço de Produção?')
    sequencial = fields.Integer('Sequencial', help="Define a ordem de exibição")
    # O campo abaixo tem como objetivo relacionar cada tipo de serviço com um status do Pedido correspondente
    status_pedido = fields.Char('Código Status Pedido')

    responsavel_default_id = fields.Many2one('res.users', string='Prof. Responsável Padrão', 
        # optional:
        ondelete='restrict',
        context={},
        domain=[],
    )

    # O campo abaixo tem como objetivo definir o sequencial default que será utilizado na criação dos serviços
    sequencial_default = fields.Integer('Seq. Padrão')

    status_default = fields.Selection(
            [('aguardando', 'Aguardando'),
             ('a_iniciar', 'A iniciar'),
             ('em_andamento', 'Em andamento'),
             ('concluido', 'Concluído'),
             ('suspenso', 'Suspenso'),
             ('conclusao_parcial', 'Conclusão Parcial')],
            'Status Padrão', default="aguardando")    


