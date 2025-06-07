from datetime import datetime


class Utils:
   
    @classmethod
    def montar_tabela_juros_pnep(cls, dados:list, data_atualizacao: str, data_citacao: str, data_str: str):
        """
            Complementa as colunas D e E das tabelas de juros do PNEP, retornando o valor dos juros acumulados
            para uma determinada data.
            
            Args:
                dados (list): Lista de dicionários com as chaves correspondentes as colunas da tabela de juros.
                data_atualizacao (str): Data no formato 'DD/MM/YYYY'
                data_citacao (str): Data no formato 'DD/MM/YYYY'
                data_str (str): Data no formato 'DD/MM/YYYY'.
                
            Returns:
                float or None: Valor de 'coluna_e' (juros acumulados) se encontrado, caso contrário, retorna None.
            """
        
        # funcao auxiliar para buscar o índice dado uma data específica
        def buscar_coluna_e(lista, data_str):
            """
            Busca na lista de dicionarios completa o item com a data correspondente e retorna o valor de 'coluna_e'.
            
            Args:
                dados (list): Lista de dicionários com as chaves 'data_dt' e 'coluna_e'.
                data_str (str): Data no formato 'DD/MM/YYYY'.
                
            Returns:
                float or None: Valor de 'coluna_e' se encontrado, caso contrário, retorna None.
            """
            try:
                data_buscada = datetime.strptime(data_str, '%d/%m/%Y')
                
                for item in lista:
                    if item['data_dt'].date() == data_buscada.date():
                        return item['coluna_e']
                
                return None  # Data não encontrada
            
            except ValueError as e:
                print("Erro ao converter data:", e)
                return None
            
        # Função auxiliar para buscar valor por data
        def buscar_valor_por_data(dados, data_alvo):
            for item in dados:
                if item['data_dt'] == data_alvo:
                    return item['juros_acumulados']
            return None       
        
        data_atualizacao_dt = datetime.strptime(data_atualizacao, '%d/%m/%Y')
        data_citacao_dt = datetime.strptime(data_citacao, '%d/%m/%Y')

        for item in dados:
            item['data_dt'] = datetime.strptime(item['data'], '%d/%m/%Y')

        dados.sort(key=lambda x: x['data_dt'])

        coluna_e_anterior = 0.0

        for i, item in enumerate(dados):
            data_linha_dt = item['data_dt']

            # coluna D
            if data_linha_dt <= data_citacao_dt:
                coluna_d = 0.0
            else:
                coluna_d = item['juros_acumulados']

            # coluna E
            if coluna_d == 0:
                valor_citacao = buscar_valor_por_data(dados, data_citacao_dt)
                valor_atualizacao = buscar_valor_por_data(dados, data_atualizacao_dt)

                if valor_citacao is not None and valor_atualizacao is not None:
                    coluna_e = valor_atualizacao - valor_citacao 
                else:
                    coluna_e = 0.0
            else:
                coluna_e = coluna_e_anterior - item['juros_mensal']

            # Atualiza o dicionário com valores calculados
            item['coluna_d'] = round(coluna_d, 6)
            item['coluna_e'] = round(coluna_e, 6)
            del item['data']
            del item['id']  # Remove 'id'

            # Reordena o dicionário
            reordered_item = {
                'data_dt': item['data_dt'],
                'juros_mensal': item['juros_mensal'],
                'juros_acumulados': item['juros_acumulados'],
                'coluna_d': item['coluna_d'],
                'coluna_e': item['coluna_e']
            }

            # Substitui no lugar original
            dados[i] = reordered_item

            # Atualiza o valor anterior para próxima iteração
            coluna_e_anterior = coluna_e

        # Resultado final (sem 'id' ou 'data_dt')
        resultado_final = dados

        valor = buscar_coluna_e(resultado_final, data_str)
        return valor





