# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class Usuario(models.Model):
    _name = 'helpdesk.usuario'
    _description = 'Usuário helpdesk'

    _inherits = {'res.users': 'cliente_id'}

    cliente_id = fields.Many2one('helpdesk.cliente', required=True, string='Cliente Relacionado',
        # optional:
        ondelete='restrict',
        context={},
        domain=[],
    )
