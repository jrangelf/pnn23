import requests

def get_api(url):
    """Faz uma requisição GET e retorna os dados da API"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API de índices em '{url}' : {e}")
        return None
