
# Indicium Code Challenger

#### Autor: Lucas Litrento

Projeto realizado para execução da proposta de EL do desafio Lighthouse Indicium.

### Tecnologias Utilizadas:

- Airflow
- Meltano
- Docker
- Postgres

### Objetivos gerais

Extrair dados de duas fontes diferetes, a primeira de um banco Postgres estático, a segunda de um arquivo CSV. Após isso, armazenar os arquivos localmente em pastas de acordo com a fonte dos dados (CSV e Postgres). Dentro de ambas as pastas, serão geradas novas pastas com a data da extração dos dados. Por fim, realizar o carregamento desses dados extraídos previamente para um novo banco Postgres.

### Realização

- Construção de um docker-compose para o airflow e os dois bancos Postgres (fonte e destino);
- Utilização do Meltano e dos seguintes módulos:
```
- tap-postgres
- tap-csv
- target-postgres
- target-csv
```
- Utilização de Docker para gerenciar contêiners e isolar execuções;

# Estruras de Diretórios e Arquivos
```
.────────────────────────────────────────────────────────
├── Airflow
│   ├── airflow-data
│   ├── config
│   ├── csv
│   ├── dags
│   │   ├── csv_load_files_def.json
│   │   ├── meltano_EL_dag.py
│   │   └── update_data_path.py
│   ├── data
│   │   ├── northwind.sql
│   │   └── order_details.csv
│   ├── docker-compose.yaml
│   ├── logs
│   ├── output
│   ├── plugins
│   └── postgres
├── meltano
│   ├── csv_load_files_def.json
│   ├── data_extraction
│   ├── Dockerfile
│   ├── files_def.json
│   ├── load
│   ├── meltano.yml
│   ├── plugins
│   │   ├── custom
│   │   │   └── target-csv-main
│   │   ├── extractors
│   │   └── loaders
│   ├── README.md
│   ├── requirements.txt
├── Makefile
├── query.sql
└── README.md
└────────────────────────────────────────────────────────
```

## Instalação

### Nota:
```
- Necessário que o docker e o docker-compose já estejam devidamente instalados;
- Execução recomendada em um ambiente com Python 3.10;
```

- Instale o make para execução do Makefile.

```
  sudo apt update && sudo apt install make -y
```

- O Makefile é composto por três comandos:

```
start_project:
    Realiza um build da imagem do Meltano e executa o docker-compose up para o Airflow e bancos Postgres
```
```
run_project:
    Executa o docker-compose up sem realizar o build da imagem do Meltano
```
```
stop_project
    Executa o docker-compose down
```

## Informações

- Customização do target-csv para a criação de pastas com a data atual, seguindo o modelo proposto, alteração na config 'output_path';
- Utilização de TaskGroup na dag para separação das tasks de extract e load;
- Utilização de 'depends_on_past' para que as tasks seguintes dependam da execução da task anterior;
- arquivo query.sql com a consulta para validação do carregamento pro Postgres;
- Schedule da dag definido para @daily(execução diária);
- Pastas de saída na task de extração: 
```
./Airflow/csv
./Airflow/postgres
```
## Utilização 

### Atualização de path

O primeiro passo é abrir a DAG 'meltano_EL_run_dag' e alterar a variável 'path_airflow_folder'(linha 18) com o path local da pasta Airflow

É possível escrever o caminho diretamente ou abrir um terminal dentro da pasta ./Airflow e digitar o seguinte comando:
```
pwd
```
Ele retornará algo similar à:

```
/home/usuario/pasta_1/pasta_2/indicium_code_challenger/Airflow
```

Adicione o path à variável:

```
path_airflow_folder = "/home/usuario/pasta_1/pasta_2/indicium_code_challenger/Airflow"
```
### Execução do Projeto
Navegue até a pasta principal do projeto:

```
.────────────────────
├── Airflow
├── meltano
├── Makefile
├── query.sql
└── README.md
└────────────────────
```

Abra um terminal (ou via VSCode) e execute um dos comandos abaixo:

Para a primeira execução do projeto:
```
make start_project
```
Para demais execuções:
```
make run_project
```
Aguarde alguns instantes para que os contâiners estejam executando.

É possível também verificar o status dos contâiners com o comando abaixo:

```
docker ps
```
Observe se estão como (healthy):
```
STATUS:
Up 2 minutes (healthy) 
```

Acesse a interface do Airflow digitando o endereço no seu navegador:

```
localhost:8080
```
#### Credenciais de Login:
Usuário: airflow

Senha: airflow

Selecione a dag meltano_EL_run_dag e abra para executar manualmente.
