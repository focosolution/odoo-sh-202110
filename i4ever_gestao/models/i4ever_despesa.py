# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Despesa(models.Model):
    _name = 'i4ever.despesa'
    _description = 'Despesas'
    _order = 'despesa'

    despesa = fields.Char('Despesa', required=True)

    data_despesa = fields.Date('Data Despesa', required=True)
    valor_despesa =  fields.Float('Valor Despesa', required=True)

    tipo = fields.Selection(
            [('frete', 'Frete'),
             ('papelaria', 'Papelaria'),
             ('comissao', 'Comissão'),
             ('outros', 'Outros')],
            'Tipo de despesa')      

    pago = fields.Boolean()
    data_pagamento = fields.Date('Data Pagamento')

    beneficiario_id = fields.Many2one('res.users', string='Beneficiário', 
        # optional:
        ondelete='restrict',
        context={},
        domain=[],
    )

    pedido_id = fields.Many2one('i4ever.pedido.resumo', string='Pedido', 
        # optional:
        ondelete='restrict',
        context={},
        domain=[],
    )    



