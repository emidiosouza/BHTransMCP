import json
from typing import List, Dict

with open(
    file='src/docs/linhas-codigo.json',
    mode='r'
) as f:
    data = json.load(f)

bus_list: List[List] = data.get('records', [])

for bus_info in bus_list:
    print(bus_info)

# Dicionário final
nested_lookup: Dict[str, Dict[int, Dict[str, str]]] = {}


for row in bus_list:
    if len(row) >= 3:
        codigo = row[1]        # Ex: '425'
        prefixo_completo = row[2]  # Ex: '5507A-01'
        descricao = row[3]

        if '-' not in prefixo_completo:
            continue  # ignora formatos inesperados

        prefixo_base, sufixo = prefixo_completo.split('-', 1)

        if prefixo_base not in nested_lookup:
            nested_lookup[prefixo_base] = {}
        dict_out = {
            'id': codigo,
            'description': descricao
        }
        nested_lookup[prefixo_base][sufixo] = dict_out

# Salvar em JSON
with open('src/docs/linhas-por-prefixo.json', 'w') as f_out:
    json.dump(nested_lookup, f_out, ensure_ascii=False, indent=2)