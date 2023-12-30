# Model Serving API

## Descrição

O ModelServingAPI é uma aplicação Python que utiliza o framework Flask para fornecer previsões com base em um modelo de aprendizado de máquina pré-treinado (LinearRegression) no formato .joblib. Esta aplicação também utiliza um banco de dados SQLite local (arquivo .db) para armazenar identificadores de solicitações e registra as operações em um arquivo de log em formato .txt.

## Pré-requisitos

Os requisitos para executar a aplicação estão inseridos dentro do arquivo environment.yml que pode ser carregado através do genrenciador de pacotes conda.

**OBS.:** O arquivo foi gerado em um sistema MacOs, podendo levar a conflitos em sistemas Windows ou Linux.

Como segunda opção, consultar o arquivo `requirements.txt`

## Configuração

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. **Instale as dependências:**

    ```bash
    conda env create -f environment.yml
    conda activate my_env
    ```

    Isso criará um ambiente Conda chamado `my_env` com as dependências especificadas no arquivo `environment.yml`.

    Ou

    ```bash
    conda create --name my_env --file requirements.txt
    conda activate my_env
    ```

   Isso criará um ambiente Conda chamado `my_env` com base nas especificações no arquivo `requirements.txt`.

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

    Substituia  `-- mode testing` e `-- mode production` para rodar nos demais modos.

    - **OBS.:** Pra rodar em modo produção, tenha certeza de configura um server WSIG como Gunicorn anteriormente.

### Rotas

- **`POST /predict`:** Envie dados de features no corpo da solicitação para obter uma previsão. Exemplo de corpo da solicitação:

    ```json
    {
        "feature_1": 0.5,
        "feature_2": 1.0
    }
    ```

## Banco de Dados

A aplicação utiliza um banco de dados SQLite para armazenar identificadores de solicitações. A tabela identificadores é automaticamente criada se não existir e o ID de cada requisição é incrementado automaticamente.

## Log

As operações da aplicação são registradas em um arquivo de log em formato de texto especificado no arquivo `.env`.

## Contribuindo

Sinta-se à vontade para contribuir!


