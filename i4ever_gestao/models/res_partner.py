# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, models

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, vals):
        company_id = self.env.user.company_id.id
        _logger.info('company_id = %s', company_id)
        vals['company_id'] = company_id
        new_partner = super(ResPartner, self).create(vals)
        return new_partner