# Model Serving API

## Descrição

O ModelServingFlaskAPI é uma aplicação Python que utiliza o framework Flask e WSGI web-server Gunicorn para fornecer previsões com base em um modelo de aprendizado de máquina pré-treinado no formato .joblib. Esta aplicação utiliza um banco de dados SQLite local (arquivo .sqlite3) para armazenar informações das requisições, interagindo por meio de SQLAlchemy como ORM. A aplicação também registra os logs do server em um arquivo em formato .txt.

## Pré-requisitos

Os requisitos para executar a aplicação estão inseridos dentro do arquivo `environment.yml `environment.yml que pode ser carregado através do genrenciador de pacotes conda.

**OBS.:** O arquivo foi gerado em OS UNIX, podendo levar a conflitos em sistemas Windows.

Como segunda opção, consultar o arquivo `requirements.txt`.

## Configuração

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/michelhilg/model-serving-flaskAPI.git
    cd model-serving-flaskAPI
    ```

2. **Instale as dependências:**

    ```bash
    conda env create -f environment.yml
    conda activate flaskapi
    ```

    Isso criará um ambiente Conda chamado `flaskapi` com as dependências especificadas no arquivo `environment.yml`.

    Ou

    ```bash
    conda create --name flaskapi python=3.8
    conda activate flaskapi
    pip install -r requirements.txt
    ```

   Isso criará um ambiente Conda chamado `flaskapi` com base nas especificações no arquivo `requirements.txt`.

   **OBS.:** Caso encontre problemas, vale a pena conferir a incompatibilidade de OS.

3. **Crie um arquivo de ambiente (`.env`) com as seguintes variáveis:**

    ```dotenv
    # Production Mode
    MODEL_PATH_PRODUCTION = "model_path_here.joblib"                
    DATABASE_PATH_PRODUCTION = "database_path_here.db"    
    DESIRED_TIMEZONE_PRODUCTION = "timezone_here"      
    LOG_FILE_PATH_PRODUCTION = "log_path_here.txt"  

    # Testing Variables
    MODEL_PATH_TESTING = "model_path_here.joblib"                
    DATABASE_PATH_TESTING = "database_path_here.db"    
    DESIRED_TIMEZONE_TESTING = "timezone_here"      
    LOG_FILE_PATH_TESTING = "log_path_here.txt"  

    # Development Variables
    MODEL_PATH_DEVELOPMENT = "model_path_here.joblib"                
    DATABASE_PATH_DEVELOPMENT = "database_path_here.db"    
    DESIRED_TIMEZONE_DEVELOPMENT = "timezone_here"      
    LOG_FILE_PATH_DEVELOPMENT = "log_path_here.txt" 
    ```

   Certifique-se de ajustar os caminhos de acordo com a localização dos seus arquivos. O arquivo pode ser criado utilizando-se como base o arquivo .env.template.
   
   Essa aplicação possuí um arquivo `config.py` o qual carrega as informações definidas dentro do `.env` para cada modo ambiente de execução definido acima.

   Para os arquivos `db.sqlite3`, `modelo.joblib` e `log.txt`, você pode usar a estrutura de pastas recomendada se preferir.

4. **Modelo**

    Certifique-se de disponibilizar o modelo de machine learning adequado para aplicação, seguindo requisitos essenciais:

    - Formato: `.joblib`
    - Versão scikit-learn: `1.0.1`

    Arquitetura testada foi a LinearRegression, porém outras arquiteturas que recebam duas features de entrada também são compatíveis.

## Uso

- **Para iniciar a API em modo `development`, execute o seguinte comando:**

    ```bash
    python app.py --mode development
    ```

    A API estará acessível em [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

    Substituia  `-- mode testing` para rodar no modo de teste.

- **Para iniciar a API em modo `production`, execute o seguinte comando:**

    Esse aplicativo usa o server built-in do Flask por estar em modo desenvolvimento, em modo produção é recomendado o uso de um server WSIG como `Gunicorn` com comando abaixo:

    ```bash
    gunicorn --preload -w 4 -b 0.0.0.0:8000 "main:create_app('producon')”
    ```

    Em que:

    - `w` = Número de workers.
    - `b` = IP e porta do server.

### Documentação

Você pode acessar as informações da API, como métodos definidos, acessando [http://127.0.0.1:5000/](http://127.0.0.1:5000/) via `Swagger`.

### Rotas

- **`POST /prediction/results`:** Envie dados de features no corpo da solicitação para obter uma previsão. Exemplo de corpo da solicitação:

    ```json
    {
        "feature_1": 0.5,
        "feature_2": 1.0
    }
    ```

    Para testar essa aplicação você pode usar ferramentas como o `Postman`, ótimo para teste de APIs.

## Banco de Dados

A aplicação utiliza um banco de dados SQLite para armazenar os dados das solicitações à API via SQLAlchemy. O arquivo de banco de dados e tabela `prediction` são automaticamente criados se não existir. O `id` de cada requisição é incrementado automaticamente. Para requisições realizadas com sucesso os valores de `feature_1`, `feature_2` e `predicao` também são gravados.

Lembre-se de configurar o caminho de sua database no arquivo de ambiente `.env`.

## Log

As operações da aplicação são registradas em um arquivo de log em formato de texto especificado no arquivo `.env`.

## Contribuindo

Sinta-se à vontade para contribuir!


