# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    # _name = 'helpdesk.cliente'
    # _description = 'Cliente helpdesk'

    _inherit = "res.partner"

    usuario_ids = fields.Many2many('res.users', 'helpdesk_res_partner_res_users_rel', 'res_partner_id', 'res_users_id',
        # Aqui, eu poderia ter mais 2 parâmetros que seriam os nomes das colunas, no caso: res_partner_id e res_users_id
        # como resolvi omitir, o framework automaticamente fez isso pra mim.
        string='Usuários', help='Dados do cliente relacionado ao Parceiro')

    item_ids = fields.One2many('helpdesk.item', "cliente_id", string="Itens")

    # cliente_id = fields.Integer(string='id cliente')
    # Campo computado com o objetivo de exibir os usuários de cada cliente
    usuarios = fields.Char(string='Usuários', compute='_usuarios', store=False, compute_sudo=False)

    # @api.depends('cliente_id')
    def _usuarios(self):
        _logger.info('Estou no _usuarios')

        # for linha in self:
        #     if linha.id:
        #         linha.usuarios = linha.id
        #     else:
        #         linha.usuarios = "---"


        usuario = self.env['res.users']
        for linha in self:
            lista_usuario = usuario.search([['cliente_id', '=', linha.id]])

            if len(lista_usuario.ids) == 0:
                linha.usuarios = "----------"
            else:
                temp_usuarios = ''
                divisoria = ''
                _logger.info('Usuários encontrados... %s', len(lista_usuario.ids))
                for usuario_corrente in lista_usuario:
                    temp_usuarios = temp_usuarios + divisoria + usuario_corrente.name + " - " + usuario_corrente.login
                    divisoria = ', '

                linha.usuarios = temp_usuarios


    # usuario_ids = fields.One2many('res.users', 'cliente_id',
    #                               string='Usuários')

    # cliente_id = fields.Many2one('res.partner', string='Cliente',
    #     # optional:
    #     ondelete='restrict',
    #     context={},
    #     domain=[],
    # )

    @api.model
    def create(self, vals):
        _logger.info('Estou no create do ResPartner, %s', vals)
        company_id = self.env.user.company_id.id
        _logger.info('company_id = %s', company_id)
        vals['company_id'] = company_id
        new_partner = super(ResPartner, self).create(vals)
        return new_partner

    # def write(self, vals):
    #     _logger.info('Estou no write do ResPartner, %s', vals)
    #     res = super(ResPartner, self).write(vals)
    #
    #     return res