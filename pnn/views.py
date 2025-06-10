from flask import render_template, request
from datetime import datetime, date

from . import pnn_bp 

from pnn.api_indice import ApiIndice 
from pnn.acd_utils import Utils     

from pnn.configura_debug import *

# def _format_decimal(value, precision=2):
#     if isinstance(value, (int, float)):
#         try:
#             return f"{value:.{precision}f}".replace('.', ',')
#         except (TypeError, ValueError): return str(value)
#     return str(value)


def _format_decimal(value, precision=2):
    if isinstance(value, (int, float)):
        try:
            # 1. Formata o número com separador de milhar (,) e decimal (.)
            #    Ex: 1947.96  -> '1,947.96'
            formatted_string = f'{value:,.{precision}f}'
            
            # 2. Troca os separadores para o padrão brasileiro
            #    Primeiro, troca a vírgula por um placeholder (#)
            #    Depois, troca o ponto por uma vírgula
            #    Finalmente, troca o placeholder por um ponto
            #    '1,947.96' -> '1#947.96' -> '1#947,96' -> '1.947,96'
            return formatted_string.replace(',', '#').replace('.', ',').replace('#', '.')
        except (TypeError, ValueError):
            return str(value) # Retorna como string se houver erro de formatação
    return str(value)

@pnn_bp.route('/') 
def index():
    return render_template('index.html', message="Bem-vindo ao PNN (Blueprint Index)")

@pnn_bp.route('/pnn23', methods=['GET', 'POST']) 
def pnn23():    
    TAB_INDICE = 't202_tabela_pnep'
    TAB_JUROS = 't310_juros_pnn'
    TAB_SELIC = 'selic_acumulada'
    DATA_CITACAO = '01/01/1960'
    DATA_ATUALIZACAO = '01/12/2021'

    data_hoje_obj = datetime.now()
    mes_hoje = data_hoje_obj.month
    ano_hoje = data_hoje_obj.year

    # Variáveis para o contexto, usando os nomes originais que o template espera
    # 'valores_list_for_template' é uma lista que será passada como 'valores' para o template
    valores_list_for_template = ["dummy_csrf"] + [""] * 9 
    
    # 'resultado_dict_for_template' conterá os resultados calculados e formatados
    resultado_dict_for_template = {} 
    
    
    str_dt_atualizacao = "" 
    str_mesano = ""         
    str_valor = ""          
    str_dt_danoso = ""      
    
    if request.method == 'POST':        
        processo_form = request.form.get('processo', '')
        competencia_form = request.form.get('competencia', '')
        exequente_form = request.form.get('exequente', '')
        executado_form = request.form.get('executado', '')
        dt_atual_str_form = request.form.get('atualizacao', '')
        bt_juros_str_form = request.form.get('aplicar_juros', 'off')
        dt_danoso_str_form = request.form.get('data_inicio', '')
        dt_arbitra_str_form = request.form.get('data_atualizar', '')        
        valor_str_input = request.form.get('valor', '0') 
        
        valores_list_for_template = [
            "csrf",
            processo_form,
            competencia_form,
            exequente_form,
            executado_form,
            dt_atual_str_form,
            bt_juros_str_form,
            dt_danoso_str_form,
            dt_arbitra_str_form,
            valor_str_input 
        ]
        
        str_valor = valor_str_input
        
        dados_tabela_juros = ApiIndice.get_tabela(TAB_JUROS)

        ano_danoso, mes_danoso = None, None
        if dt_danoso_str_form:
            try:
                ano_danoso_parts, mes_danoso_parts = dt_danoso_str_form.split('-')
                ano_danoso, mes_danoso = int(ano_danoso_parts), int(mes_danoso_parts)
                str_dt_danoso = f'{mes_danoso:02d}/{ano_danoso}' 
            except ValueError: pass

        ano_atualiza, mes_atualiza = None, None
        if dt_atual_str_form:
            try:
                ano_atualiza_parts, mes_atualiza_parts = dt_atual_str_form.split('-')
                ano_atualiza, mes_atualiza = int(ano_atualiza_parts), int(mes_atualiza_parts)
                str_dt_atualizacao = f'{mes_atualiza:02d}/{ano_atualiza}' 
            except ValueError: pass

        ano_arbitra, mes_arbitra = None, None
        if dt_arbitra_str_form:
            try:
                ano_arbitra_parts, mes_arbitra_parts = dt_arbitra_str_form.split('-')
                ano_arbitra, mes_arbitra = int(ano_arbitra_parts), int(mes_arbitra_parts)
                str_mesano = f'{mes_arbitra:02d}/{ano_arbitra}' 
            except ValueError: pass
        
        data_de_hoje_date_obj = date(ano_hoje, mes_hoje, 1)
        data_arbitramento_obj = date(ano_arbitra, mes_arbitra, 1) if ano_arbitra and mes_arbitra else None
        data_atualizacao_obj = date(ano_atualiza, mes_atualiza, 1) if ano_atualiza and mes_atualiza else None

        selic = 0.0
        if ano_atualiza and data_atualizacao_obj and data_arbitramento_obj:
            if ano_atualiza > 2021:
                try:
                    parte1 = ApiIndice.get_tabela_mes_ano(TAB_SELIC, str(mes_atualiza), str(ano_atualiza))['selic_acumulada']
                    parte2 = ApiIndice.get_tabela_mes_ano(TAB_SELIC, '12', '2021')['selic_acumulada']
                    selic = parte1 - parte2
                except (TypeError, KeyError): selic = 0.0
                if data_atualizacao_obj == data_de_hoje_date_obj and ano_arbitra > 2021:
                    try:
                        parte1 = ApiIndice.get_tabela_mes_ano(TAB_SELIC, str(mes_atualiza), str(ano_atualiza))['selic_acumulada']
                        parte2 = ApiIndice.get_tabela_mes_ano(TAB_SELIC, str(mes_arbitra), str(ano_arbitra))['selic_acumulada']
                        selic = parte1 - parte2
                    except (TypeError, KeyError): selic = 0.0
                if data_atualizacao_obj < data_de_hoje_date_obj: 
                    try:
                        parte1 = ApiIndice.get_tabela_mes_ano(TAB_SELIC, str(mes_atualiza), str(ano_atualiza))['selic_acumulada']
                        parte2 = ApiIndice.get_tabela_mes_ano(TAB_SELIC, str(mes_arbitra), str(ano_arbitra))['selic_acumulada']
                        selic = parte1 - parte2
                    except (TypeError, KeyError): pass # Mantém o valor anterior de selic se houver erro
                if ano_arbitra > 2021 and data_atualizacao_obj < data_de_hoje_date_obj:
                    try:
                        parte1 = ApiIndice.get_tabela_mes_ano(TAB_SELIC, str(mes_atualiza), str(ano_atualiza))['selic_acumulada']
                        parte2 = ApiIndice.get_tabela_mes_ano(TAB_SELIC, str(mes_arbitra), str(ano_arbitra))['selic_acumulada']
                        selic = parte1 - parte2
                    except (TypeError, KeyError): selic = 0.0
            
        if selic < 0: selic = 0.0

        juros = 0.0
        if bt_juros_str_form == 'on':
            if mes_danoso and ano_danoso:
                data_evento_danoso_fmt = f'01/{mes_danoso:02d}/{ano_danoso}'                
                try:
                    juros_raw = Utils.montar_tabela_juros_pnep(dados_tabela_juros, DATA_ATUALIZACAO, DATA_CITACAO, data_evento_danoso_fmt)
                    juros = juros_raw if juros_raw and juros_raw >= 0 else 0.0
                except Exception: juros = 0.0
        
        indice = 1.0
        if ano_arbitra and data_arbitramento_obj:
            if ano_arbitra > 2021:
                indice = 1.0
            else:
                try: indice_data = ApiIndice.get_tabela_mes_ano(TAB_INDICE, str(mes_arbitra), str(ano_arbitra)); indice = indice_data['indice_correcao']
                except (TypeError, KeyError): indice = 1.0
            if data_arbitramento_obj < date(1964, 10, 1):
                try: indice_data = ApiIndice.get_tabela_mes_ano(TAB_INDICE, '10', '1964'); indice = indice_data['indice_correcao']
                except (TypeError, KeyError): indice = 1.0
        
        valor_float = 0.0
        try: valor_float = float(valor_str_input.replace(".", "").replace(",", "."))
        except ValueError: pass

        valor_principal_calc = valor_float # Nome da variável para o cálculo
        corrigido_calc = valor_principal_calc * indice
        valor_juros_calc = corrigido_calc * juros
        subtotal_calc = corrigido_calc + valor_juros_calc
        valor_selic_calc = selic * subtotal_calc
        total_final_calc = valor_selic_calc + subtotal_calc

        # Preenche 'resultado_dict_for_template' com os valores calculados e FORMATADOS
        resultado_dict_for_template['valor'] = _format_decimal(valor_principal_calc, 2)
        resultado_dict_for_template['iam'] = _format_decimal(indice, 8)
        resultado_dict_for_template['corrigido'] = _format_decimal(corrigido_calc, 2)
        resultado_dict_for_template['juros'] = _format_decimal(juros * 100, 4)
        resultado_dict_for_template['valor_juros'] = _format_decimal(valor_juros_calc, 2)
        resultado_dict_for_template['subtotal'] = _format_decimal(subtotal_calc, 2)
        resultado_dict_for_template['selic'] = _format_decimal(selic * 100, 2)
        resultado_dict_for_template['valor_selic'] = _format_decimal(valor_selic_calc, 2)
        resultado_dict_for_template['total'] = _format_decimal(total_final_calc, 2)
    
    # Monta o contexto final com os nomes exatos de chaves que o template espera
    context_to_render = {
        'valores': valores_list_for_template,
        'resultado': resultado_dict_for_template,
        'dt_atualizacao': str_dt_atualizacao,
        'dt_mesano': str_mesano,
        'str_valor': str_valor, # O valor original do input do formulário
        'dt_danoso': str_dt_danoso
    }
    return render_template('pnn23.html', **context_to_render)
