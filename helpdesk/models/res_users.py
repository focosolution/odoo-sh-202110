# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):

    _inherit = "res.users"

    # cliente_ids = fields.Many2many('res.partner', 'helpdesk_res_partner_res_users_rel', 'res_users_id', 'res_partner_id',
    #     # Aqui, eu poderia ter mais 2 parâmetros que seriam os nomes das colunas, no caso: res_users_id e res_partner_id
    #     # como resolvi omitir, o framework automaticamente fez isso pra mim.
    #     string='Clientes', help='Dados do usuário relacionado ao cliente')

    cliente_id = fields.Integer('Cliente', required=False)
    nome_cliente = fields.Char(string='Cliente', compute='_nome_cliente', store=False, compute_sudo=False)

    is_atendente = fields.Boolean('Atendente', default=False,
                                help="Indica se o uduário é técnico")

    categoria_ids = fields.Many2many('helpdesk.categoria', 'helpdesk_res_users_categoria_rel', 'res_users_id', 'categoria_id',
        string='Categorias', help='Categorias a qual o atendente tem aptidão')

    # Campo computado com o objetivo de exibir as categorias de cada usuário
    categorias = fields.Char(string='Categorias', compute='_categorias', store=False, compute_sudo=False)

    @api.depends('categoria_ids')
    def _categorias(self):
        _logger.info('Estou no _categorias')

        usuario = self.env['res.users']
        for linha in self:
            # lista_usuario = usuario.search([['cliente_id', '=', linha.id]])

            if len(linha.categoria_ids) == 0:
                linha.categorias = "----------"
            else:
                temp_categorias = ''
                divisoria = ''
                _logger.info('Categorias encontradas... %s', len(linha.categoria_ids.ids))
                for categoria_corrente in linha.categoria_ids:
                    temp_categorias = temp_categorias + divisoria + categoria_corrente.name
                    divisoria = ', '

                linha.categorias = temp_categorias


    # usuario_ids = fields.One2many('res.users', 'cliente_id',
    #                               string='Usuários')

    # cliente_id = fields.Many2one('res.partner', string='Cliente',
    #     # optional:
    #     ondelete='restrict',
    #     context={},
    #     domain=[],
    # )

    @api.depends('cliente_id')
    def _nome_cliente(self):
        _logger.info('Estou no _nome_cliente')

        # modelo aonde vou buscar a informação que preciso
        cliente = self.env['res.partner']
        for linha in self:
            lista_cliente = cliente.search([['id', '=', linha.cliente_id]])

            if len(lista_cliente.ids) == 0:
                linha.nome_cliente = "----------"
            else:
                _logger.info('Cliente encontrado... %s', len(lista_cliente.ids))
                for cliente_corrente in lista_cliente:
                    linha.nome_cliente = cliente_corrente.name

    @api.model
    def create(self, vals):
        _logger.info('Estou no create do ResUsers, %s', vals)

        new_user = super(ResUsers, self).create(vals)
        return new_user

    # @api.model
    def write(self, vals):
        _logger.info('Estou no write do ResUsers, %s', vals)

        # cliente_ids = vals.get('cliente_ids')
        # if (cliente_ids):
        #     _logger.info('cliente_ids[0] = %s', cliente_ids[0])
        #     _logger.info('cliente_ids[0][2] = %s', cliente_ids[0][2])
        #     _logger.info('Tamanho cliente_ids[0][2] = %s', len(cliente_ids[0][2]))
        #


        res = super(ResUsers, self).write(vals)

        return res