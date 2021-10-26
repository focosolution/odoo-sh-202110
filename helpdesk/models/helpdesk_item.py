# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class HelpdeskItem(models.Model):
    _name = 'helpdesk.item'
    _description = 'Item a ser controlado pelo sistema de Helpdesk, podendo ser Produto, Serviço ou algo similar'
    _order = 'name'

    name = fields.Char('Item', required=True, index=True)
    descricao = fields.Text('Descrição')
    company_id = fields.Many2one('res.company', string='Empresa',
        # optional:
        ondelete='restrict',
        context={},
        domain=[],
    )

    categoria_id = fields.Many2one('helpdesk.categoria', string='Categoria',
                                 # optional:
                                 ondelete='restrict',
                                 context={},
                                 domain=[],
                                 required=True
                                 )

    cliente_id = fields.Many2one('res.partner', string='Cliente',
        # optional:
        ondelete='restrict',
        context={},
        domain=[],
    )

    # responsavel_id = fields.Many2one('res.partner', string='Responsável',
    #     ondelete='set null',
    #     context={},
    #     domain=[],
    # )

    local = fields.Char('Local')
    fabricante = fields.Char('Fabricante')
    modelo = fields.Char('Modelo')
    numero_serie = fields.Char('Numero Série')
    custo = fields.Float('Custo',  digits=(10,2), )
    data_compra = fields.Date('Data Compra')

    @api.model
    def create(self, vals):
        company_id = self.env.user.company_id.id
        _logger.info('>>> company_id = %s', company_id)
        vals['company_id'] = company_id
        new_categoria_item = super(HelpdeskItem, self).create(vals)
        return new_categoria_item
