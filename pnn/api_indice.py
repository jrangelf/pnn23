from pnn.api_utils import get_api
from pnn.acd_constantes import API_INDICE

class ApiIndice:

    base_url = API_INDICE 
               
    @classmethod
    def get_tabela(cls, nome_tabela):
        # retorna uma lista de dicionários com as tuplas da tabela            
        url = cls.base_url + nome_tabela        
        return get_api(url)

    @classmethod
    def get_tabela_mes_ano(cls, nome_tabela, mes, ano):
        # retorna um registro buscado por mes e ano em uma tabela de indice
        url = cls.base_url + f'{nome_tabela}/{mes}/{ano}'        
        return get_api(url)
    

