# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class ConcluirTarefa(models.TransientModel):
    _name = 'concluir.tarefa'
    
    comentario = fields.Text(string = 'Comentários', required = True)
    is_concluido = fields.Boolean('Tarefa Concluída?')

    def concluir_tarefa(self):

        servico_id = self._context.get('active_id')

        _logger.info('Estou em concluir tarefa, id_servico = %s', servico_id)

        _logger.info('pedido_id = =>>>%s<===', self._context.get('pedido_id'))

        # obter o serviço que teve sua tarefa concluída
        servico = self.env['i4ever.servico'].browse(servico_id)

        if self.is_concluido:  # Alterar o status para concluído
            vals = { 'state': 'concluido', 'is_concluido': self.is_concluido, 'comentario': self.comentario, 
                     'data_conclusao': fields.Date.today() }
        else:
            vals = { 'comentario': self.comentario }

        _logger.info('servico.pedido_id.state = %s', servico.pedido_id.state)

        rtn = servico.write(vals)
        
        # Apenas iremos modificar o status, caso o status do pedido atual seja o mesmo do serviço concluído
        if self.is_concluido and servico.pedido_id.state == servico.tipo_servico_id.status_pedido:
            self.env['i4ever.servico'].avanca_status_pedido(servico_id)

