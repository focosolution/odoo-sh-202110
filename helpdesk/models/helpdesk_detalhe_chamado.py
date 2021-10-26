# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class HelpdeskDetalheChamado(models.Model):
    _name = 'helpdesk.detalhe.chamado'
    _description = 'Detalhe do Chamado'
    _order = 'id desc'

    chamado_id = fields.Many2one('helpdesk.chamado', string='Chamado',
                                 # optional:
                                 ondelete='restrict',
                                 context={},
                                 domain=[],
                                 )

    interlocutor = fields.Char('interlocutor', required=False)
    texto = fields.Text('Texto')

    # Campo computado com o objetivo de exibir o responsável pela interação do chamado.
    responsavel = fields.Char(string='Interlocutor', compute='_responsavel', store=False, compute_sudo=False)

    @api.depends('interlocutor')
    def _responsavel(self):
        _logger.info('Estou no _responsavel')

        # responsavel = self.env['i4ever.servico']
        for linha in self:
            if linha.interlocutor:
                linha.responsavel = linha.interlocutor
            else:
                linha.responsavel = linha.create_uid.name



