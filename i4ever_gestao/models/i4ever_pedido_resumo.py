# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class PedidoResumo(models.Model):
    _name = 'i4ever.pedido.resumo'
    _description = 'Pedido Image4ever - Resumo'

    pedido = fields.Char('Número Pedido', required=True)

    cliente_id = fields.Many2one('res.partner', string='Cliente', 
        # optional:
        ondelete='set null',
        context={},
        domain=[],
    )

    servico_ids = fields.One2many('i4ever.servico', 'pedido_id',
                                  string='Serviços')

    detalhes = fields.Text('Detalhes do Pedido')
    img_orcamento = fields.Binary('Imagem Orçamento')

    state = fields.Selection([
        ('inicio', 'Entrada'),
        ('gerar_amostra', 'Contagem e Amostra'),
        ('aprovar_amostra', 'Aprovação Amostra'),
        ('digitalizacao', 'Digitalização'),
        ('orientacao_recorte', 'O & R'),
        ('revisao_final', 'Qualidade'),
        ('disponibilizar', 'Disponibilização'),
        ('pagamento', 'Pagamento'),
        ('entregar', 'Entrega')], 
        default="inicio", 
        string="Status",
        group_expand="_expand_groups"
        )

    valor_total = fields.Float('Valor Total do Orçamento', digits=(14,2), )
    qtde_total_imagens = fields.Integer('Qtde Imagens')
    data_entrada = fields.Date('Data da Entrada')
    data_previsao_entrega = fields.Date('Dt. Fim')
    valor_digitalizacao = fields.Float('Valor Digitalização', digits=(14,2), )
    valor_frete_orcado = fields.Float('Valor Frete Orçado', digits=(14,2), )
    valor_despesa_estimada = fields.Float('Valor Despesa Estimada', digits=(14,2), )

    local_origem = fields.Selection([
        ('sp', 'SP'),
        ('rj', 'RJ')
        ], string="Origem")

    # Campo computado com o objetivo de exibir o responsável atual pelo serviço de acordo com o status!
    situacao_atual = fields.Char(string='Situação Atual', compute='_situacao_atual', store=False, compute_sudo=False)

    # servico_ids = fields.One2many('i4ever.servico', "pedido_id", string="Serviços")

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (pedido)', 'Número do Pedido deve ser único.')    
    ]

    @api.model
    def _expand_groups(self, states, domain, order):
        return ['inicio', 'gerar_amostra', 'aprovar_amostra', 'digitalizacao', 'orientacao_recorte', 
                'revisao_final', 'disponibilizar', 'pagamento', 'entregar']    

    @api.depends('state', 'pedido')
    def _situacao_atual(self):
        _logger.info('Estou no _responsavel_atual')
        servico = self.env['i4ever.servico']
        for pedido in self:
            # _logger.info('pedido.id = %s', pedido.id)
            lista_servico = servico.search([['pedido_id.id', '=', pedido.id], 
                                                ['tipo_servico_id.status_pedido', '=', pedido.state]])

            situacao_atual = ''
            divisoria = ''

            if len(lista_servico.ids) == 0:
                pedido.situacao_atual = "----------"
            else:
                
                for srv_corrente in lista_servico: 
                    if (srv_corrente.responsavel_id):
                        nome_responsavel = srv_corrente.responsavel_id.name
                    else:
                        nome_responsavel = '???'

                    situacao_atual = situacao_atual + divisoria + (nome_responsavel + " - " + srv_corrente.state + " - " + 
                                    str(srv_corrente.perc_concluido) + "%")
                    divisoria = ' & '
                    _logger.info('Dentro do for...' )
                    
                pedido.situacao_atual = situacao_atual

    def name_get(self):
        """ This method is used to customize display name of the record. In this case we are overriding the name_get method """
        result = []
        # ClienteObj = self.env['res.partner']
        for record in self:
            # Preciso obter o nome do cliente dado o cliente_id
        #    ClienteObj = self.env['res.partner']
            _logger.info('record.cliente_id = %s', record.cliente_id)
            _logger.info('record.cliente_id.name = %s', record.cliente_id.name)
        #    domain = [('id', '=', '13')]
        #    cliente = ClienteObj.search(domain)
            rec_name = "%s - %s" % (record.pedido, record.cliente_id.name)
            result.append((record.id, rec_name))
        return result

    def log_todos_contatos(self):
        modelo_contatos = self.env['res.partner']  # This is an empty recordset of model res.partner
        domain = [('id', '=', '13')]
        contatos = modelo_contatos.search(domain)
        _logger.info('Todos os contatos: %s', contatos)
        _logger.info('Contato: %s', contatos.name)
     #   for ...
        return True

    def cria_servicos(self, id_pedido):
        _logger.info('Estou em cria_servicos. id_pedido = %s', id_pedido)

        tipo_servico = self.env['i4ever.tipo.servico'].search([['is_producao', '=', True]])

        for reg_servico in tipo_servico:
            _logger.info('Nome = %s', reg_servico.name)

            if reg_servico.status_pedido == 'inicio':
                dt_prev_conclusao = fields.Date.today()
            else:
                dt_prev_conclusao = None

            vals = [{ 'pedido_id': id_pedido, 'tipo_servico_id': reg_servico.id, 'state': reg_servico.status_default, 
                      'percentual_responsavel': 100, 'responsavel_id' : reg_servico.responsavel_default_id.id, 
                      'sequencial': reg_servico.sequencial_default, 'data_prev_conclusao': dt_prev_conclusao}]
            self.env['i4ever.servico'].create(vals)
        
        _logger.info('Fim cria_servicos')
        return True

    def lista_tipo_servico(self):
        _logger.info('Estou em listar tipo de serviços')
        qtde_tipo_servico = self.env['i4ever.tipo.servico'].search_count([['is_producao', '=', True]])
        _logger.info('Qtde de registros = %s', qtde_tipo_servico)

       # _logger.info('Usuário = %s', self.uid)

        tipo_servico = self.env['i4ever.tipo.servico'].search([['is_producao', '=', True]])
        for linha in tipo_servico:
            _logger.info('Nome = %s, responsavel_default_id = %s, usuario_id = %s', 
                         linha.name, linha.responsavel_default_id, linha.responsavel_default_id.id)
        return True
    
#    @api.onchange('state')
#    def altera_status_servico(self):
#        # Iremos alterar o status do novo serviço a ser executado para "a_iniciar"
#        _logger.info('Estou em altera_status_servico. Pedido = %s, state = %s', self.pedido, self.state)
#
#        self.env['i4ever.servico'].inicia_status_servico(self.pedido, self.state)

    # sobreescrevendo método write com o objetivo de tratar o início de um novo serviço / tarefa
    def write(self, vals):
        _logger.info('Estou no write, vals = %s', vals)

        state = vals.get('state')
        _logger.info('Parâmetro state = %s', state)

        rtn = super(PedidoResumo, self).write(vals)

        if state:
            _logger.info('O status foi alterado... novo status = %s ... chamando inicia_status_servico', self.state)
            self.env['i4ever.servico'].inicia_status_servico(self.pedido, self.state)

        return rtn

    # sobreescrevendo método create com o objetivo de tratar o início de um novo serviço / tarefa
    @api.model
    def create(self, vals):
        _logger.info('Estou no create, vals = %s', vals)

        # Verficando se o pedido já existe
        pedido_corrente = vals.get('pedido')

        _logger.info('Pedido corrente (antes)', pedido_corrente)

        qtde_pedido = self.env['i4ever.pedido.resumo'].search_count([['pedido', '=', pedido_corrente]])

        if qtde_pedido > 0:  # Encontrou
            pedido_corrente = pedido_corrente + "-copia"

        _logger.info('Pedido corrente (depois)', pedido_corrente)
        vals['pedido'] = pedido_corrente

        rtn = super(PedidoResumo, self).create(vals)

        _logger.info('rtn.id = %s', rtn.id)

        self.env['i4ever.pedido.resumo'].cria_servicos(rtn.id)

        return rtn

    def gerar_svc_pagamento(self):
        selected_ids = self.env.context.get('active_ids', [])
        selected_records = self.env['i4ever.pedido.resumo'].browse(selected_ids)

        _logger.info('Total de elementos...  %s', len(selected_records))
        _logger.info('Elementos...  %s', selected_records)

        for pedido in selected_records:

            tipo_servico = self.env['i4ever.tipo.servico'].search([['status_pedido', '=', 'pagamento']])

            vals = [{ 'pedido_id': pedido.id, 'tipo_servico_id': tipo_servico.id, 'state': tipo_servico.status_default, 
                      'percentual_responsavel': 100, 'responsavel_id' : tipo_servico.responsavel_default_id.id, 
                      'sequencial': tipo_servico.sequencial_default}]
            self.env['i4ever.servico'].create(vals)
        
        _logger.info('Fim gerar_svc_pagamento')
        return True



#        for linha in servico:
#            _logger.info('Antes... Status = %s', linha.state)

     #   vals = [{ 'state': 'a_iniciar', }]
     #   vals = [{ 'qtde_imagens_processadas': 100, }]
     #   servico.write(vals)

#        for linha in servico:
#            _logger.info('Depois... Status = %s', linha.state)


       # self.env['res.partner'].search([['is_company', '=', True], ['customer', '=', True]])

