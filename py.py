import pandas as pd
import numpy as np

dataset_doencas = pd.read_csv('Datasus\Datasets_tratados\doencas.csv',index_col=False)

fa = dataset_doencas[dataset_doencas['doenca'] == 'Febre_Amarela']
resto = dataset_doencas[dataset_doencas['doenca'] != 'Febre_Amarela']

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

final = pd.concat([resto,fa],ignore_index=True)
final.to_csv('doencas1.csv',index=False)
