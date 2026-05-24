import pandas as pd
import numpy as np

dengue24 = pd.read_csv('Datasets_Resultantes/denguefinal2024.csv',sep=',',encoding='latin1')
dengue25 = pd.read_csv('Datasets_Resultantes/denguefinal2025.csv', sep=',',encoding='latin1')
zika24 = pd.read_csv('Datasets_Resultantes/final_ZIKABR24.csv', sep=',',encoding='latin1')
zika25 = pd.read_csv('Datasets_Resultantes/final_ZIKABR25.csv', sep=',',encoding='latin1')
chik24 = pd.read_csv('Datasets_Resultantes/final_CHIKBR24.csv', sep=',',encoding='latin1')
chik25 = pd.read_csv('Datasets_Resultantes/final_CHIKBR25.csv', sep=',',encoding='latin1')
febrea = pd.read_csv('Datasets_Resultantes/final_fa_casoshumanos_1994-2025.csv', sep=',',encoding='latin1')

datasets = [dengue24,dengue25,zika24,zika25,chik24,chik25,febrea]

dengue24.columns = ['data','uf','cidade','idade','sexo','raca','hospitalizado','confirmacao','obito','dt_obito']
dengue25.columns = ['tipo','data','uf','cidade','idade','sexo','raca','hospitalizado','confirmacao','obito','dt_obito']
zika24.columns = ['data','uf','cidade','idade','sexo','raca','confirmacao','obito','dt_obito']
zika25.columns = ['data','uf','cidade','idade','sexo','raca','confirmacao','obito','dt_obito']
chik24.columns = ['data','uf','cidade','idade','sexo','raca','hospitalizado','confirmacao','obito','dt_obito']
chik25.columns = ['data','uf','cidade','idade','sexo','raca','hospitalizado','confirmacao','obito','dt_obito']
febrea.columns = ['id','uf','cidade','sexo','idade','data','mes','ano','obito','dt_obito']

dengue24 = dengue24[dengue24['confirmacao'] == 10]
dengue25 = dengue25[dengue25['confirmacao'] == 10]
zika24 = zika24[zika24['confirmacao'] == 1]
zika25 = zika25[zika25['confirmacao'] == 1]
chik24 = chik24[chik24['confirmacao'] == 13]
chik25 = chik25[chik25['confirmacao'] == 13]

dengue24['doenca'] = 'Dengue'
dengue25['doenca'] = 'Dengue'
zika24['doenca'] = 'Zika'
zika25['doenca'] = 'Zika'
chik24['doenca'] = 'chikungunya'
chik25['doenca'] = 'chikungunya'
febrea['doenca'] = 'Febre_Amarela'

dengue24['obito'] = np.where(dengue24['dt_obito'].isnull(),0,1)
dengue25['obito'] = np.where(dengue25['dt_obito'].isnull(),0,1)
zika24['obito'] = np.where(zika24['dt_obito'].isnull(),0,1)
zika25['obito'] = np.where(zika25['dt_obito'].isnull(),0,1)
chik24['obito'] = np.where(chik24['dt_obito'].isnull(),0,1)
chik25['obito'] = np.where(chik25['dt_obito'].isnull(),0,1)
febrea['obito'] = np.where(febrea['dt_obito'].isnull(),0,1)


colunas_finais = ['doenca','data','uf','cidade','idade','sexo','raca','obito','dt_obito']

for df in [dengue24, dengue25, zika24, zika25, chik24, chik25, febrea]:
    
    for col in colunas_finais:
        
        if col not in df.columns:
            df[col] = np.nan


dengue_total = pd.concat([dengue24, dengue25], ignore_index=True)

zika_total = pd.concat([zika24, zika25], ignore_index=True)

chik_total = pd.concat([chik24, chik25], ignore_index=True)


dataset_final = pd.concat([
    dengue_total,
    zika_total,
    chik_total,
    febrea
], ignore_index=True)


dataset_final = dataset_final[colunas_finais]


print(dataset_final.shape)

print(dataset_final.head())

dataset_final.to_csv('dataset_doencas_24-25.csv', index=False, encoding='latin1')