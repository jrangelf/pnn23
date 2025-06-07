# /app/pnn/__init__.py
from flask import Blueprint

# 1. DEFINA o Blueprint primeiro
pnn_bp = Blueprint(
    'pnn',  # Nome do Blueprint (usado em url_for, ex: 'pnn.nome_da_view')
    __name__,
    template_folder='templates',  # Pasta de templates para este Blueprint
    static_folder='static',       # Pasta de arquivos estáticos para este Blueprint
    static_url_path='/pnn/static' # Opcional: Define um URL base para os arquivos estáticos do blueprint
                                  # Se não definido, usará /static e pode colidir com o static da app principal
                                  # Se sua pasta static está em /app/pnn/static, esta linha é útil.
)

# 2. IMPORTE as views DEPOIS que o Blueprint (pnn_bp) foi definido
# O '.' significa "do pacote atual" (ou seja, da pasta 'pnn')
from . import views