from flask import Flask
import os # Importe o módulo 'os'
from pnn import pnn_bp 

app = Flask(__name__) 

app.register_blueprint(pnn_bp) 

# Configurações da aplicação principal

if os.environ.get('FLASK_ENV') == 'development':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['DEBUG'] = True # Adicionado para habilitar o modo debug em desenvolvimento
    # Você também pode definir main_app.debug = True diretamente se preferir

# Se este arquivo for o ponto de entrada para Gunicorn/uWSGI
#application = main_app
