# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class HelpdeskTipoChamado(models.Model):
    _name = 'helpdesk.tipo.chamado'
    _description = 'Tipo de Chamado'
    _order = 'sequencial'

    name = fields.Char('Departamento', required=True)
    sequencial = fields.Integer('Sequencial', required=True)
    company_id = fields.Many2one('res.company', string='Empresa',
        # optional:
        ondelete='restrict',
        context={},
        domain=[],
    )

    @api.model
    def create(self, vals):
        company_id = self.env.user.company_id.id
        _logger.info('>>> company_id = %s', company_id)
        vals['company_id'] = company_id
        new_categoria_item = super(HelpdeskTipoChamado, self).create(vals)
        return new_categoria_item
