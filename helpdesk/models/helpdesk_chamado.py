# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api
from datetime import datetime

_logger = logging.getLogger(__name__)

class HelpdeskChamado(models.Model):
    _name = 'helpdesk.chamado'
    _description = 'Chamado / ocorrência'
    _order = 'id desc'

    data_abertura = fields.Date('Data Abertura', required=True, default=datetime.today())

    company_id = fields.Many2one('res.company', string='Empresa',
        # optional:
        ondelete='restrict',
        context={},
        domain=[],
    )

    cliente_id = fields.Many2one('res.partner', string='Cliente',
        # optional:
        required=True,
        ondelete='restrict',
        context={},
        domain=[],
    )

    atendente_id = fields.Many2one('res.users', string='Atendente',
        # optional:
        required=False,
        ondelete='restrict',
        context={},
        domain=[],
    )

    item_id = fields.Many2one('helpdesk.item', string='Item',
        ondelete='restrict',
        context={},
        domain=[],
    )

    interlocutor = fields.Char('interlocutor', required=False)
    prioridade = fields.Selection([
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('critica', 'Crítica')],
        default="normal",
        string="Prioridade",
        group_expand="_expand_groups"
    )

    tipo_chamado_id = fields.Many2one('helpdesk.tipo.chamado', string='Departamento',
        ondelete='restrict',
        context={},
        domain=[],
    )

    assunto = fields.Char('Assunto', required=True)
    #  atendente_id = fields.Many2one('res.users', string='Atendente',
    #     ondelete='restrict',
    #     context={},
    #     domain=[],
    # )

    status = fields.Selection([
        ('pendente', 'Pendente'), # O chamado foi incluído e ninguém ainda interagiu
        ('em_atendimento', 'Em Andamento'), # Algum atendente está trabalhando no chamado
        ('aguardando_atendente', 'Aguardando Atendente'), # O cliente respondeu e está aguardando o atendente
        ('aguardando_gerente', 'Aguardando Gerente'), # O atendente escalou para o gerente
        ('aguardando_cliente', 'Aguardando Cliente'), # O atendente ou gerente, pediu o aval ao cleinte
        ('resolvido', 'Resolvido'), # Resolvido
        ('rejeitado', 'Rejeitado')], # Rejeitado
        default="pendente",
        string="Status",
        group_expand="_expand_groups"
    )

    data_conclusao = fields.Date('Data Conclusão')

    detalhe_chamado_ids = fields.One2many('helpdesk.detalhe.chamado', "chamado_id", string="Interações")

    # Campo computado com o id da categoria - este campo será utilizado no record rule
    categoria_id = fields.Integer(string='Categoria Id', compute='_categoria_id', store=True, compute_sudo=False)

    @api.depends('item_id')
    def _categoria_id(self):
        _logger.info('Estou no _categoria_id')

        usuario = self.env['res.users']
        for linha in self:
            # lista_usuario = usuario.search([['cliente_id', '=', linha.id]])

            _logger.info('linha.item_id.categoria_id = %s', linha.item_id.categoria_id)
            _logger.info('linha.item_id.categoria_id.id = %s', linha.item_id.categoria_id.id)

            linha.categoria_id = linha.item_id.categoria_id.id


    # Campo computado com o objetivo de exibir o responsável pela interação do chamado.
    responsavel = fields.Char(string='Interlocutor', compute='_responsavel', store=False, compute_sudo=False)

    # Campo computado com o objetivo de obter a empresa a qual o usuário pertence
    # empresa_usuario = fields.Char(string='Empresa Usuário', compute='_empresa_usuario', store=True, compute_sudo=False)
    #
    # def _empresa_usuario(self):
    #     _logger.info('zzz self.env.user = %s', self._uid)
    #     # _logger.info('self.env.user.cliente_id = %s', self._uid)
    #     usuario = self.env['res.users'].browse(self._uid)
    #     _logger.info('Buscou usuário')
    #     _logger.info('usuario.cliente_id = ' + str(usuario.cliente_id))
    #
    #     for linha in self:
    #         _logger.info('linha.cliente_id.id = '+str(linha.cliente_id.id))
    #         if (linha.cliente_id.id == usuario.cliente_id):
    #             linha.empresa_usuario = True
    #         else:
    #             linha.empresa_usuario = False
    #         _logger.info(linha.empresa_usuario)
    #
    #     self.flush
    #     _logger.info('Executou o flush')


    @api.depends('interlocutor')
    def _responsavel(self):

        for linha in self:
            if linha.interlocutor:
                linha.responsavel = linha.interlocutor
            else:
                linha.responsavel = linha.create_uid.name


    @api.model
    def create(self, vals):
        company_id = self.env.user.company_id.id
        _logger.info('>>> company_id = %s', company_id)
        vals['company_id'] = company_id
        new_categoria_item = super(HelpdeskChamado, self).create(vals)
        return new_categoria_item

    def filtrar_chamado_atendente(self):

        # form_id = self.env.ref('helpdesk.helpdesk_chamado_view_tree').id
        form_id = self.env.ref('helpdesk.helpdesk_chamado_action').id

        _logger.info('Estou em filtrar_chamado_atendente, chamando tree!!! XXX - %s', self.env.user.categoria_ids)

        # return {
        #     'name': 'Chamados para o Atendente',
        #     'domain': [('categoria_id', 'in', [c.id for c in self.env.user.categoria_ids])],
        #     'view_type': 'form',
        #     'res_model': 'helpdesk.chamado',
        #     'view_id': form_id,
        #     'view_mode': 'tree',
        #     'type': 'ir.actions.act_window',
        #     # 'target': 'new',
        #     # 'context': {
        #     #        'default_cliente_id': self.env.user.cliente_id,
        #     #        'default_is_cliente': "True",
        #     # },
        # }

        return {
            'name': 'Chamados para o Atendente',
            'domain': [('categoria_id', 'in', [c.id for c in self.env.user.categoria_ids])],
            'context': {'search_default_meus_chamados': 1},
            'view_type': 'form',
            'res_model': 'helpdesk.chamado',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

