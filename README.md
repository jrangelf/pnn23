# Ferramenta de Cálculo de Atualização Monetária (PNN)

## Descrição

Este projeto é uma aplicação web desenvolvida em **Python** com o framework **Flask**, projetada para realizar cálculos complexos de atualização monetária, juros de mora e aplicação da taxa SELIC, seguindo normativas específicas como as do Manual de Cálculos da Justiça Federal (CJF) e a Emenda Constitucional 113/2021.

A aplicação funciona como um módulo de cálculo (`pnn`) que consome dados de uma micro-API externa (`api-indice`), responsável por fornecer os índices de correção e taxas de juros necessários. A arquitetura foi pensada para ser modular e escalável, com os serviços rodando em containers Docker independentes.

O principal caso de uso implementado é o **"PNN 23"**, um cálculo específico para apuração de valores economizados por anistiados políticos.

---

## Funcionalidades Principais

* **Cálculo Detalhado**: Executa a atualização de valores com base em data de arbitramento, data do evento danoso e data de atualização final.
* **Correção Monetária e Juros**: Aplica índices de correção (ex: IPCA-E) e taxas de juros de mora (1%, 0.5%, poupança) em períodos específicos, conforme a legislação.
* **Aplicação da Taxa SELIC**: Calcula e aplica a taxa SELIC sobre o montante atualizado, em conformidade com a EC 113/2021 (a partir de dez/2021).
* **Interface Web Simples**: Formulário intuitivo para inserção dos dados necessários para o cálculo.
* **Relatório para Impressão**: Gera um demonstrativo detalhado do cálculo, formatado para impressão.
* **Arquitetura de Microserviços**: A lógica de cálculo é desacoplada da fonte de dados, que é fornecida por uma API externa, promovendo manutenibilidade e escalabilidade.
* **Containerização com Docker**: A aplicação e seus serviços são totalmente containerizados, garantindo um ambiente de execução consistente e facilitando o deploy.

---

## Tecnologias Utilizadas

* **Backend**: Python 3.8+
* **Framework Web**: Flask
* **Servidor WSGI**: Gunicorn
* **Workers Assíncronos**: Gevent (para alta concorrência)
* **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
* **Comunicação com API**: Biblioteca `requests`
* **Ambiente**: Docker & Docker Compose

---

## Como Executar o Projeto

Este projeto é dividido em dois componentes principais que rodam em containers separados, mas se comunicam através de uma rede Docker:
1.  **Aplicação Flask `pnn`**: A interface web e a lógica de cálculo.
2.  **API de Índices `api-indice`**: O microserviço que fornece os dados.

### Pré-requisitos

* Docker instalado
* Docker Compose instalado

### Passos para a Execução

1.  **Crie a Rede Docker Externa**: Como os serviços estão em `docker-compose.yml` separados, eles precisam de uma rede compartilhada para se comunicarem.
    ```bash
    docker network create siscalc
    ```

2.  **Inicie a API de Índices**: Navegue até o diretório do projeto `api-indice` e inicie os serviços (a API e seu banco de dados).
    ```bash
    # No diretório do projeto api-indice
    docker-compose up -d --build
    ```
    Certifique-se de que o serviço da API esteja configurado no `docker-compose.yml` com um alias de rede para que possa ser encontrado pelo nome `api-indice`:
    ```yaml
    services:
      api:
        container_name: api-indice
        networks:
          siscalc:
            aliases:
              - api-indice
    ```

3.  **Inicie a Aplicação PNN**: Navegue até o diretório do projeto `pnn` e inicie o serviço.
    ```bash
    # No diretório do projeto pnn
    docker-compose up -d --build
    ```

4.  **Acesse a Aplicação**: Após os containers serem iniciados, acesse a aplicação no seu navegador:
    * **Página Inicial**: `http://localhost:8008`
    * **Calculadora PNN23**: `http://localhost:8008/pnn23`

---

## Estrutura do Projeto (Módulo PNN)

```
pnn/
|-- pnn/                     # Pacote principal da aplicação Flask (Blueprint)
|   |-- __init__.py          # Define o Blueprint 'pnn'
|   |-- views.py             # Contém as rotas e a lógica das views (ex: /pnn23)
|   |-- functions.py         # Módulo para funções utilitárias (ex: ApiIndice, Utils)
|   |-- templates/           # Contém os arquivos HTML (templates Jinja2)
|   |   |-- index.html
|   |   |-- pnn23.html
|   |-- static/              # Contém os arquivos estáticos
|   |   |-- js/
|   |   |   |-- pnn_calc_scripts.js
|-- wsgi.py                  # Ponto de entrada para o servidor Gunicorn
|-- Dockerfile               # Define como construir a imagem Docker da aplicação
|-- docker-compose.yml       # Orquestra a execução do container da aplicação
|-- requirements.txt         # Lista de dependências Python
```

---


