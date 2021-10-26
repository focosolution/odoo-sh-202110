# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class CriarUsuario(models.TransientModel):
    _name = 'temp.tratar.usuario'

    name = fields.Char('Nome Usuário', required=True)
    login = fields.Char('Login', required=True)
    cliente_id = fields.Integer('Cliente', required=False)

    def criar_usuario(self):

        ### Dando permissão para o usuário no grupo cliente ###

        # Obtendo a categoria
        categoria = self.env['ir.module.category'].search([['name', '=', "FSHelpdesk"]])
        if self.ensure_one():
            _logger.info('Encontrou a categoria %s', categoria.id)

        # Obtendo o grupo
        grupo = self.env['res.groups'].search([['category_id', '=', categoria.id], ['name', '=', "Admin"]])

        if self.ensure_one():
            _logger.info('Encontrou o grupo %s', grupo.id)

        # Obtendo o cliente corrente
        res_partner_id = self._context.get('active_id')

        _logger.info('Estou em criar_usuario, res_partner_id = %s', res_partner_id)

        vals = [{'name': self.name, 'login': self.login, 'cliente_id': res_partner_id}] #, 'groups_id': grupo.id}]
        usuario = self.env['res.users'].create(vals)

        _logger.info('Criado usuario... %s', usuario.id)

        # Agora fazendo o write para salvar o groups_id
        # vals = [{'groups_id': [[usuario.id, False, [grupo.id]]]}]
        # usuario.write(vals)



        # vals = [{'cliente_ids': [[res_partner_id, False, [usuario.id]]]}]
        # vals = [{'name': self.name+'xxx'}]
        # usuario.write(vals)

        # res = super(CriarUsuario, self).write(vals)
        #
        # _logger.info('Alterado usuario... %s', usuario)

        # return rtn

        # if (self.is_cliente):
        #     interlocutor = self.interlocutor
        # else:
        #     interlocutor = None
        #
        # vals = [{'chamado_id': chamado.id, 'texto': self.texto, 'interlocutor': interlocutor}]
        # detalhe_chamado = self.env['helpdesk.detalhe.chamado'].create(vals)
        #
        # _logger.info('Criado detalhe chamado... %s', detalhe_chamado.id)


