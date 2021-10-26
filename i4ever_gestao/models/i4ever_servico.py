# -*- coding: utf-8 -*-
# Adicionar a Ação Automatizada abaixo em ... => Técnico > Automação > Ações Automatizadas (acaso não exista, instalar app base_automation)
# Nome da Ação: Bloquear Conclusão de Tarefa via draganddrop
# Modelo: Serviços Image4ever
# Ação: Execute Python Code
# Disparo: Na atualização
# Campos de Acionamento: Status
# Código python:
# if record.state in ['concluido'] and not record.is_concluido:
#  raise UserError('Para concluir uma tarefa, favor entrar no modo edição e depois clicar no botão Concluir Tarefa!')

import logging
import pytz
from odoo import models, fields, api
from datetime import timedelta

_logger = logging.getLogger(__name__)

class Servico(models.Model):
    _name = 'i4ever.servico'
    _description = 'Serviços Image4ever'
    _order = 'pedido_id, id'

    pedido_id = fields.Many2one('i4ever.pedido.resumo', string='Pedido', 
        # optional:
        ondelete='set null',
        context={},
        domain=[],
    )
    
    tipo_servico_id = fields.Many2one('i4ever.tipo.servico', string='Serviço', 
        # optional:
        ondelete='set null',
        context={},
        domain=[],
    )

    state = fields.Selection(
            [('aguardando', 'Aguardando'),
             ('a_iniciar', 'A iniciar'),
             ('em_andamento', 'Em andamento'),
             ('concluido', 'Concluído'),
             ('cancelado', 'Cancelado')],
            string="Status Svc",
            default="aguardando",
            group_expand="_expand_groups"
            )
    
    responsavel_id = fields.Many2one('res.users', string='Responsável', 
        ondelete='restrict',
        context={},
        domain=[],
    )

    data_inicio = fields.Date('Data de Início')
    # prazo = fields.Float('Prazo em dias', digits=(4,1))
    prazo = fields.Integer('Prazo em dias')
    # data_prev_inicio - é a data a qual estimamos o início de determinado serviço
    data_prev_inicio = fields.Datetime('Estimativa p/ início')
    # data_prev_conclusao - é a data a qual o sistema gera de forma automática ou o usuário (gestor ou resp. pela tarefa) define.
    data_prev_conclusao = fields.Datetime('Estimativa p/ conclusão')
    data_conclusao = fields.Date('Data da conclusão')
    perc_concluido = fields.Integer('Percentual Concluído')
    sequencial = fields.Integer('Prioridade')
    
    percentual_responsavel = fields.Float('Percentual p/ o Responsável', digits=(5,2), )
    qtde_imagens_processadas = fields.Integer('Qtde de imagens processadas')
    valor_servico = fields.Float('Valor do Serviço', digits=(14,2) )
    comentario = fields.Text('Comentários')
    is_concluido = fields.Boolean('Tarefa Concluída?')
    # Campos relacionados
    data_previsao_entrega = fields.Date(related='pedido_id.data_previsao_entrega', store=True)
    status_pedido = fields.Selection(related='pedido_id.state')
    pedido = fields.Char(related='pedido_id.pedido')
    qtde_total_imagens = fields.Integer(related='pedido_id.qtde_total_imagens')

    @api.model
    def _expand_groups(self, states, domain, order):
        return ['aguardando', 'a_iniciar', 'em_andamento', 'concluido']    

    def name_get(self):
        """ This method is used to customize display name of the record. In this case we are overriding the name_get method """
        result = []
        for record in self:
            # Preciso obter o nome do cliente dado o cliente_id
        #    ClienteObj = self.env['res.partner']
            _logger.info('Pedido = %s', record.pedido_id.pedido)
            _logger.info('record.pedido_id.cliente_id.name = %s', record.pedido_id.cliente_id.name)
        #    domain = [('id', '=', '13')]
        #    cliente = ClienteObj.search(domain)
            rec_name = "%s - %s | %s | %s" % (record.pedido_id.pedido, record.pedido_id.cliente_id.name, record.tipo_servico_id.name, record.state)
            result.append((record.id, rec_name))
        return result        

 #   @api.onchange('is_concluido')
    def avanca_status_pedido(self, servico_id):
    # Ao chamar este método, o serviço foi concluído, assim iremos avançar o status do Pedido
       # _logger.info('Estou em avanca_status_pedido. id Serviço = %s, Pedido = %s, Status(Pedido) = %s, Status(serviço) = %s,'+ 
       #              ', Status relacionado ao serviço corrente = %s', self._origin.id,
       #               self.pedido_id.pedido, self.pedido_id.state, self.state, self.tipo_servico_id.status_pedido)

        _logger.info('Estou em avanca_status_pedido. id Serviço = %s', servico_id)

        # Obtendo serviço...
        #servico = self.env['i4ever.servico'].browse(self._origin.id)
        servico = self.env['i4ever.servico'].browse(servico_id)
        _logger.info('Serviço encontrado id = %s', servico.id)

#        if is_concluido:
#            _logger.info('Concluído = True ...    ')
#            vals = { 'state': 'concluido'}
#            rtn = servico.write(vals)
#        else:
#            vals = { 'state': 'aguardando'}
#            rtn = servico.write(vals)
#            return

        # Percorrendo a lista de tipo de serviço para obter o próximo status
        status_corrente = servico.pedido_id.state
        tipo_servico = self.env['i4ever.tipo.servico'].search([['is_producao', '=', True]])
        proximo_status = ''
        encontrou = False
        _logger.info('status_corrente = %s', status_corrente)

        for reg_servico in tipo_servico:

            _logger.info('Nome = %s, status = %s', reg_servico.name, reg_servico.status_pedido)

            if encontrou:
                proximo_status = reg_servico.status_pedido
                _logger.info('proximo_status = %s', proximo_status)
                # Buscar o Pedido em questão e fazer o Update
                ###_logger.info('Chamando browse - %s', self.pedido_id.id)
                _logger.info('Chamando browse - %s', servico.pedido_id.id)
                ###pedido = self.env['i4ever.pedido.resumo'].browse(self.pedido_id.id)
                pedido = self.env['i4ever.pedido.resumo'].browse(servico.pedido_id.id)
                _logger.info('Pedido encontrado %s', pedido)
                
                vals = { 'state': proximo_status}
                rtn = pedido.write(vals)

                # Chamando método para já atualizar o status do próximo serviço para "a iniciar"
                _logger.info('Chamando inicia_status_servico, servico.pedido_id.pedido = %s, servico.pedido_id.state = %s',
                             servico.pedido_id.pedido, servico.pedido_id.state)
                ###self.env['i4ever.servico'].inicia_status_servico(self.pedido_id.pedido, self.pedido_id.state)
                self.env['i4ever.servico'].inicia_status_servico(servico.pedido_id.pedido, servico.pedido_id.state)
        
                _logger.info('Retornou ... %s', rtn)
                break

            if reg_servico.status_pedido == status_corrente:
                _logger.info('Encontrou!')
                encontrou = True
            

    def inicia_status_servico(self, param_pedido, param_state):

        _logger.info('Estou em inicia_status_servico... param_pedido = %s, param_state = %s', param_pedido, param_state)

        # Identificando o item de serviço que terá o seu status alterado.
        lista_servico = self.env['i4ever.servico'].search([['pedido_id.pedido', '=', param_pedido], 
                                                     ['tipo_servico_id.status_pedido', '=', param_state]])
                                             #        ['state', '=', 'aguardando']])

        # Tratando os n serviços encontrados...
        for servico in lista_servico:
            if servico.state == 'aguardando':
                vals = { 'state': 'a_iniciar', 'is_concluido': False}
                rtn = servico.write(vals)

            _logger.info('servico.pedido_id.state = %s', servico.pedido_id.state)

            # Dando um tratamento especial para o caso do serviço "Contagem e Amostra" e "Disponibilização"
            if servico.pedido_id.state == 'gerar_amostra' or servico.pedido_id.state == 'disponibilizar':
                dt_prev_conclusao = fields.Date.today()
                vals = { 'data_prev_conclusao': self.env['i4ever.servico'].proximo_dia_util(dt_prev_conclusao)}
                rtn = servico.write(vals)

        _logger.info('Retornou ... ')

    def proximo_dia_util(self, dt):

        dt = dt + timedelta(1)

        _logger.info('weekday = %s', dt.weekday())

        dias_add = 0

        if dt.weekday() == 5: # sábado, soma 2
            dias_add = 2
        if dt.weekday() == 6: # domingo, soma 1
            dias_add = 1

        _logger.info('dias_add = %s', dias_add)

        dt_retorno = (dt + timedelta(dias_add))

        _logger.info('retornando... dt_retorno = %s', dt_retorno)

        return dt_retorno

    # def concluir_tarefa(self):
    #     _logger.info('Estou em concluir tarefa, id = %s', self.id)

    #     # self.state = 'concluido'
        
    #     action_vals = {
    #         'type':'ir.actions.act_window',
    #         'name':'Conclusão da Tarefa',
    #         'view_mode':'form',
    #         'view_type':'form',
    #         'target':'new',
    #         'res_model':'i4ever.servico',
    #         'res_id': self.id,
    #         'flags': {'initial_mode': 'edit'},
    #         'views': [(self.env.ref('i4ever_gestao.i4ever_servico_fltrado_comentario_form').id, 'form')],
    #         'view_id': self.env.ref('i4ever_gestao.i4ever_servico_fltrado_comentario_form').id
    #     }

    #     return action_vals

    # O método abaixo serve para definirmos o conteúdo default para determinados campos
    @api.model
    def default_get(self, fields):

        _logger.info('Estou no default_get')

        res = super(Servico, self).default_get(fields)
     #   res['state'] = 'concluido'
        return res

    def write(self, vals):
        _logger.info('Estou no write, vals = %s', vals)

        is_concluido = vals.get('is_concluido')
        state = vals.get('state')
     #   _logger.info('Parâmetro is_concluido = %s', is_concluido)

        if state == 'em_andamento': # Este é o novo status...
            if not self.data_inicio:  # Nunca teve data de início!
                vals['data_inicio'] = fields.Date.today()

        # Verficando se o usuário arrastou para concluído, ou seja, não foi através do botão "Concluir Tarefa"
        # if state == 'concluido' and not is_concluido: 
        #     _logger.info('Retornando para o status corrente... %s', self.state)
        #     vals['state'] = self.state

        _logger.info('self.state = %s', self.state)

        if state != 'concluido' and self.state != 'concluido':
            vals['is_concluido'] = False
            vals['data_conclusao'] = ""

        rtn = super(Servico, self).write(vals)
        return rtn

 #       if self.is_concluido:
 #           _logger.info('Concluído = True ...    ')
 #           if self.state == 'concluido':
 #               self.env['i4ever.servico'].avanca_status_pedido()
 #               values['state'] = 'concluido'
 #               _logger.info('Passando status para Concluído...    ')
 #           else:
 #               values['is_concluido'] = False
 #               _logger.info('Concluído = False ...    ')

        # Caso o serviço tenha sido concluído, iremos chamar avanca_status_pedido para avançar o status do serviço seguinte...

    def gerar_cronograma(self):
        selected_ids = self.env.context.get('active_ids', [])
        selected_records = self.env['i4ever.servico'].browse(selected_ids)

        _logger.info('Total de elementos...  %s', len(selected_records))
        _logger.info('Elementos...  %s', selected_records)

        nova_data_prev_inicio = self.env['i4ever.servico'].proximo_dia_util(fields.datetime.now())

        _logger.info('nova_data_prev_inicio (now) = %s', nova_data_prev_inicio.strftime("%c"))

        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.use.tz)

        nova_data_prev_inicio = pytz.utc.localize(nova_data_prev_inicio).astimezone(user_tz)

        _logger.info('nova_data_prev_inicio (now com tz do usuário) = %s', nova_data_prev_inicio.strftime("%c"))

        nova_data_prev_inicio = fields.datetime(fields.datetime.today().year, fields.datetime.today().month, 
                                                fields.datetime.today().day, 10)

        _logger.info('nova_data_prev_inicio = %s', nova_data_prev_inicio.strftime("%c"))
        _logger.info('nova_data_prev_inicio = %s', nova_data_prev_inicio)

        primeiro = True

        for servico in selected_records:

            if servico.prazo == 0:
                continue

            if primeiro:
                if servico.data_prev_inicio:
                    data_inicio = servico.data_prev_inicio
                else:
                    data_inicio = fields.datetime.today()
                
                nova_data_prev_inicio = fields.datetime(data_inicio.year, data_inicio.month, 
                                                        data_inicio.day, 13) # Iniciando às 13hs UTC!!!
                _logger.info('primeiro... nova_data_prev_inicio = %s', nova_data_prev_inicio)

                primeiro = False

            else:
                nova_data_prev_inicio = self.env['i4ever.servico'].proximo_dia_util(nova_data_prev_conclusao)
                _logger.info('nova_data_prev_inicio (1) = %s', nova_data_prev_inicio)
                nova_data_prev_inicio = fields.datetime(nova_data_prev_inicio.year, nova_data_prev_inicio.month, 
                                                        nova_data_prev_inicio.day, 13)
                _logger.info('nova_data_prev_inicio (2) = %s', nova_data_prev_inicio)

            # Obtendo a data de conclusão...
            nova_data_prev_conclusao = self.env['i4ever.servico'].obter_data_fim(servico.prazo, nova_data_prev_inicio)

            # nova_data_prev_conclusao = self.env['i4ever.servico'].proximo_dia_util(nova_data_prev_inicio + timedelta(servico.prazo-1))
            _logger.info('nova_data_prev_conclusao (1) = %s', nova_data_prev_conclusao)
            nova_data_prev_conclusao = fields.datetime(nova_data_prev_conclusao.year, nova_data_prev_conclusao.month, 
                                            nova_data_prev_conclusao.day, 18) # Finalizando às 18hs UTC!!!
            _logger.info('nova_data_prev_conclusao (2) = %s', nova_data_prev_conclusao)

            # salvando...
            vals = { 'data_prev_inicio': nova_data_prev_inicio, 'data_prev_conclusao': nova_data_prev_conclusao }
            servico.write(vals)                

    def obter_data_fim(self, prazo, dt_corrente):
        dt_fim = dt_corrente
        for x in range(1, prazo):
            dt_fim = self.env['i4ever.servico'].proximo_dia_util(dt_fim)
        return dt_fim


    def limpar_estimativa(self):
        _logger.info('Estou em limpar estimativas')

        selected_ids = self.env.context.get('active_ids', [])
        selected_records = self.env['i4ever.servico'].browse(selected_ids)

        for servico in selected_records:
            vals = { 'data_prev_inicio': "", 'data_prev_conclusao': "" }
            servico.write(vals)                
    

