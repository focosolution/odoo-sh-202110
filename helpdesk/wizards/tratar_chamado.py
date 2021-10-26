# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class CriarChamado(models.TransientModel):
    _name = 'temp.tratar.chamado'

    data_abertura = fields.Date('Data Abertura', required=True, default=fields.Date.today())

    cliente_id = fields.Many2one('res.partner', string='Cliente',
        # optional:
        required=True,
        ondelete='restrict',
        context={},
        domain=[],
    )

    # cliente_id_default = fields.Integer(string='Cliente Default', compute='_cliente_default', store=False, compute_sudo=False)
    #
    # def _cliente_default(self):
    #     _logger.info('Estou no _cliente_default')
    #
    #     for linha in self:
    #         linha.cliente_id_default = 9

    item_id = fields.Many2one('helpdesk.item', string='Item',
        ondelete='restrict',
        context={},
        domain=[],
        required=True,
    )

    interlocutor = fields.Char('Interlocutor', required=False)
    prioridade = fields.Selection([
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('critica', 'Crítica')],
        default="normal",
        string="Prioridade",
        required=True,
        group_expand="_expand_groups"
    )

    tipo_chamado_id = fields.Many2one('helpdesk.tipo.chamado', string='Departamento',
        ondelete='restrict',
        context={},
        domain=[],
        required=True,
    )

    assunto = fields.Char('Assunto', required=True)

    is_cliente = fields.Boolean('Interação Cliente', default="True", help="É o cliente quem está interagindo com o chamado?")
    texto = fields.Text('Texto', required=True)

    # temp_cliente = fields.Integer()

    def gravar_chamado(self):

        _logger.info('Estou em gravar_chamado, self.data_abertura = %s', self.data_abertura)

        self.inserir_chamado()

        _logger.info('chamando return')

        # form_id = self.env.ref('helpdesk.helpdesk_chamado_view_tree').id
        # _logger.info('Estou em criar_chamdo, Chamando o return...')
        #
        # return {
        #     'name': 'Listar chamado',
        #     'domain': [],
        #     'view_type': 'form',
        #     'res_model': 'helpdesk.chamado',
        #     'view_id': form_id,
        #     'view_mode': 'tree',
        #     'type': 'ir.actions.act_window',
        # }

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def gravar_chamado_cliente(self):

        self.inserir_chamado()

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def inserir_chamado(self):

        _logger.info('Estou em inserir_chamdo, self.data_abertura = %s', self.data_abertura)

        vals = [{'data_abertura': self.data_abertura, 'cliente_id': self.cliente_id.id, 'item_id': self.item_id.id,
                 'interlocutor': self.interlocutor, 'prioridade': self.prioridade, 'tipo_chamado_id': self.tipo_chamado_id.id,
                 'assunto': self.assunto}]
        chamado = self.env['helpdesk.chamado'].create(vals)

        _logger.info('Criando detalhe chamado... %s', chamado.id)

        if (self.is_cliente):
            interlocutor = self.interlocutor
        else:
            interlocutor = None

        vals = [{'chamado_id': chamado.id, 'texto': self.texto, 'interlocutor': interlocutor}]
        detalhe_chamado = self.env['helpdesk.detalhe.chamado'].create(vals)

        _logger.info('Criado detalhe chamado, retornando ... %s', detalhe_chamado.id)

        return

    def criar_chamdo_cliente(self):

        form_id = self.env.ref('helpdesk.helpdesk_criar_chamado_cliente_form').id

        _logger.info('Estou em criar_chamdo_cliente, chamando formulário!!! - %s', self.env.user.cliente_id)

        return {
            'name': 'Criação de chamado pelo cliente',
            'domain': [],
            'view_type': 'form',
            'res_model': 'temp.tratar.chamado',
            'view_id': form_id,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                   'default_cliente_id': self.env.user.cliente_id,
                   'default_is_cliente': "True",
            },
        }

class InteragirChamado(models.TransientModel):
    _name = 'temp.interagir.chamado'

    texto = fields.Text('Texto', required=True)

    status = fields.Selection([
        ('pendente', 'Pendente'),
        ('em_atendimento', 'Em Andamento'),
        ('aguardando_atendente', 'Aguardando Atendente'),
        ('aguardando_gerente', 'Aguardando Gerente'),
        ('aguardando_cliente', 'Aguardando Cliente'),
        ('resolvido', 'Resolvido'),
        ('rejeitado', 'Rejeitado')],
        string="Novo Status",
        group_expand="_expand_groups"
    )


    atendente_id = fields.Many2one('res.users', string='Atendente',
        # optional:
        required=False,
        ondelete='restrict',
        context={},
        domain=[('is_atendente','=',True)],
    )

    def interagir_chamado(self):

        chamado_id = self._context.get('active_id')

        vals = [{'chamado_id': chamado_id, 'texto': self.texto}]
        detalhe_chamado = self.env['helpdesk.detalhe.chamado'].create(vals)

        _logger.info('interagir_chamdo ...  %s', detalhe_chamado.id)

        # self.env['temp.interagir.chamado'].atualiza_status(chamado_id, self.status)

        _logger.info('self.env.user.id = %s', self.env.user.id)

        self.atualiza_status(chamado_id, self.status, self.env.user.id)

    def atualiza_status(self, chamado_id, novo_status, user_id):
        # obter o chamado para atualizar seu status
        chamado = self.env['helpdesk.chamado'].browse(chamado_id)

        _logger.info('chamado.status = %s', chamado.status)
        _logger.info('novo_status = %s', novo_status)

        vals = {}

        if chamado.status != novo_status:
            vals['status'] = novo_status

        if novo_status == 'pendente':
            vals['atendente_id'] = None
        else:
            vals['atendente_id'] = user_id

        _logger.info('Estou no write, vals = %s', vals)

        rtn = chamado.write(vals)

        return rtn

    def designar_chamado(self):

        _logger.info('Estou em designar_chamado, atendente = %s', self.atendente_id.id)
        chamado_id = self._context.get('active_id')
        chamado = self.env['helpdesk.chamado'].browse(chamado_id)

        # vals = [{'atendente_id': self.atendente_id.id}]

        # vals = {}
        # vals['atendente_id'] = self.atendente_id.id
        vals = {'atendente_id': self.atendente_id.id, 'status': 'aguardando_atendente'}

        _logger.info('Vai chamar write')
        rtn = chamado.write(vals)


class InteragirChamadoCliente(models.TransientModel):
    _name = 'temp.interagir.chamado.cliente'

    interlocutor = fields.Char('Interlocutor', required=True)
    texto = fields.Text('Texto', required=True)

    status = fields.Selection([
        ('pendente', 'Pendente'),
        ('em_atendimento', 'Em Atendimento'),
        ('aguardando_cliente', 'Aguardando Cliente'),
        ('resolvido', 'Resolvido'),
        ('rejeitado', 'Rejeitado')],
        string="Novo Status",
        group_expand="_expand_groups"
    )

    def interagir_chamado_cliente(self):
        chamado_id = self._context.get('active_id')

        vals = [{'chamado_id': chamado_id, 'interlocutor': self.interlocutor, 'texto': self.texto}]
        detalhe_chamado = self.env['helpdesk.detalhe.chamado'].create(vals)

        _logger.info('InteragirChamadoCliente ...  %s', detalhe_chamado.id)


class InteragirChamadoUsuCliente(models.TransientModel):
    _name = 'temp.interagir.chamado.usu.cliente'

    texto = fields.Text('Texto', required=True)

    def interagir_chamado_usu_cliente(self):
        chamado_id = self._context.get('active_id')

        vals = [{'chamado_id': chamado_id, 'texto': self.texto}]
        detalhe_chamado = self.env['helpdesk.detalhe.chamado'].create(vals)

        _logger.info('InteragirChamadoUsuCliente ...  %s', detalhe_chamado.id)

        # Alterando o Status do Chamado para "Aguardando Atendente"
        chamado = self.env['helpdesk.chamado'].browse(chamado_id)

        _logger.info('chamado.status (corrente) = %s', chamado.status)

        vals = {'status': 'aguardando_atendente'}

        _logger.info('Estou no write, vals = %s', vals)

        chamado.write(vals)


