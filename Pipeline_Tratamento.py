import numpy as np
import pandas as pd
 
dataset_doencas = pd.read_csv('doencas.csv',index_col=False)

# Separação entre febre amarela e as outras doenças: Os datasets tem configurações diferentes.
fa = dataset_doencas[dataset_doencas['doenca'] == 'Febre_Amarela']
resto = dataset_doencas[dataset_doencas['doenca'] != 'Febre_Amarela']

# Transformar cidades e ufs (códigos) em nomes.

url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios" # Tabela do ibge com codigos e nomes das cidades.
municipios = pd.read_json(url)

municipios = municipios[['id', 'nome']]
municipios.columns = ['cidade', 'nome_municipio']

municipios['cidade'] = municipios['cidade'] // 10
resto['cidade'] = pd.to_numeric(resto['cidade'],errors='coerce')
municipios['cidade'] = pd.to_numeric(municipios['cidade'],errors='coerce')

resto = resto.merge(municipios,on='cidade',how='left')
fa['cidade'] = fa['cidade'].str.title()

resto['cidade'] = resto['nome_municipio']
resto.drop('nome_municipio',axis=1)

ufs = {
    11: 'RO',
    12: 'AC',
    13: 'AM',
    14: 'RR',
    15: 'PA',
    16: 'AP',
    17: 'TO',
    21: 'MA',
    22: 'PI',
    23: 'CE',
    24: 'RN',
    25: 'PB',
    26: 'PE',
    27: 'AL',
    28: 'SE',
    29: 'BA',
    31: 'MG',
    32: 'ES',
    33: 'RJ',
    35: 'SP',
    41: 'PR',
    42: 'SC',
    43: 'RS',
    50: 'MS',
    51: 'MT',
    52: 'GO',
    53: 'DF'
}

resto['uf'] = pd.to_numeric(resto['uf'], errors='coerce')
resto['uf'] = resto['uf'].map(ufs)

# Padronizar datas
fa['data'] = pd.to_datetime(fa['data'],errors='coerce',dayfirst=True)

# Idade
def converter_idade(valor):

    valor = str(valor).zfill(4)

    tipo = valor[0]

    idade = int(valor[1:])

    if tipo == '4':
        return idade

    elif tipo == '3':
        return idade / 12

    elif tipo == '2':
        return idade / 365

    elif tipo == '1':
        return idade / (365 * 24)

    else:
        return np.nan


resto['idade'] = resto['idade'].apply(converter_idade)

def converter_raca(raca):
    if pd.notna(raca):
        raca = str(int(raca))
    if raca == '1':
        return 'branca'
    elif raca == '2':
        return 'preta'
    elif raca == '3':
        return 'amarela'
    elif raca == '4':
        return 'parda'
    elif raca == '5':
        return 'indígena'
    else:
        return 'PNI'

resto['raca'] = resto['raca'].apply(converter_raca)

final = pd.concat([resto,fa],ignore_index=True)

final['data'] = pd.to_datetime(
    final['data'],
    errors='coerce',
    format='mixed'
)

final['dt_obito'] = pd.to_datetime(
    final['dt_obito'],
    errors='coerce',
    format='mixed'
)

final.to_csv('doencas.csv',index=False)