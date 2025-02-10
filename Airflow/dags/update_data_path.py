import json
import re
from datetime import datetime

def get_current_date():
    """Retorna a data atual no formato YYYY-MM-DD."""
    return datetime.today().strftime('%Y-%m-%d')

def update_data_path():
    """Atualiza qualquer data antiga no JSON para a data atual."""
    input_filename = "/opt/airflow/dags/csv_load_files_def.json"  # Arquivo base
    current_date = get_current_date()
    
    # Padrão regex para encontrar datas no formato YYYY-MM-DD
    date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}|\(data_path\)")

    # Ler o JSON original
    with open(input_filename, 'r') as file:
        json_data = json.load(file)

    # Atualizar os caminhos
    for item in json_data:
        item["path"] = date_pattern.sub(current_date, item["path"])  # Substitui qualquer data pela data atual

    # Sobrescrever o arquivo original
    with open(input_filename, 'w') as file:
        json.dump(json_data, file, indent=2)

    print(f"Arquivo atualizado com a data {current_date}")
    return json_data  # Retorna os dados atualizados para validação, se necessário

update_data_path()
