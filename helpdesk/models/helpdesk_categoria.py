# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class HelpdeskCategoria(models.Model):
    _name = 'helpdesk.categoria'
    _description = 'Categoria de Helpdesk para definir cada item'
    _order = 'name'

    name = fields.Char('Categoria', required=True, index=True)
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
        new_categoria_item = super(HelpdeskCategoria, self).create(vals)
        return new_categoria_item
