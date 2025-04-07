import os
import json
import requests
import pandas as pd
from prefect import flow
from arcgis.gis import GIS
from dotenv import load_dotenv
from datetime import timedelta
from prefect import flow, task
from prefect.variables import Variable
from prefect.blocks.system import Secret

load_dotenv()
user_agol = Secret.load("usuario-integrador-agol").get()
smdcg_variables = Variable.get("smdcg_variables")
gis_variables = Variable.get("gis_portal_variables")

AGOL_USERNAME_TO_NCQ = os.getenv("AGOL_USERNAME_TO_NCQ") or user_agol["username"]
AGOL_PASSWORD_TO_NCQ = os.getenv("AGOL_PASSWORD_TO_NCQ") or user_agol["password"]
LAYER_ID_AGOL_METEOROLOGIA = os.getenv("LAYER_ID_AGOL_METEOROLOGIA") or smdcg_variables["LAYER_ID_AGOL_METEOROLOGIA"]

URL_GIS_ENTERPRISE_GEONITEROI = os.getenv("URL_GIS_ENTERPRISE_GEONITEROI") or gis_variables["URL_GIS_ENTERPRISE_GEONITEROI"]
URL_RISCO_FOGO_API = os.getenv("URL_RISCO_FOGO_API") or smdcg_variables["URL_RISCO_FOGO_API"]
URL_METEOROLOGIA_API = os.getenv("URL_METEOROLOGIA_API") or smdcg_variables["URL_METEOROLOGIA_API"]

@task
def connect_agol():
    try:
        # Função para atualizar os valores da camada existente
        url = URL_GIS_ENTERPRISE_GEONITEROI
        usr = AGOL_USERNAME_TO_NCQ
        pwd = AGOL_PASSWORD_TO_NCQ
        gis = GIS(url, usr, pwd, verify_cert=False)
        layer_id = LAYER_ID_AGOL_METEOROLOGIA

        # Localize a Feature Layer onde os dados estão armazenados (insira o seu Item ID)
        item = gis.content.get(layer_id)

        # Utiliza a primeira camada
        layer = item.layers[0]
        return layer
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erro ao conectar ao agol: {e}")
    
@task
def get_api_risco():
    try:
        response_risk = requests.get(URL_RISCO_FOGO_API)
        var_dict_risk = response_risk.__dict__
        content_risk = var_dict_risk['_content']

        # Utiliza o Json para transformar em dataframe
        obj1 = json.loads(content_risk)
        dfe0 = pd.DataFrame(obj1)
        dfe1 = pd.concat([dfe0.drop(['fields'], axis=1),
                        dfe0['fields'].apply(pd.Series)], axis=1)

        dfe1 = dfe1[dfe1['data_final'].isnull()]

        return dfe1
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erro ao consultar api risco: {e}")

@task
def get_api_meteorologia():
    try:
        response_weather = requests.get(URL_METEOROLOGIA_API)
        var_dict_weather = response_weather.__dict__
        content_weather = var_dict_weather['_content']

        # Divide a string content_weather em colunas
        values = content_weather.decode().split(';')  # decode de bytes para string

        # Ignora os 3 primieros e o último valor
        values = values[3:-1]

        # Cria o DataFrame com os valores restantes
        dft = pd.DataFrame([values], columns=['temperatura',
                        'umidade', 'vento', 'velocidade do vento', 'data'])
        
        return dft
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erro ao consultar api meteorologia: {e}")



@flow(name="Fluxo risco de incêndio", log_prints=True)
def fire_risk_flow():
    try:
        # Chamar dados api_risco
        df_risco = get_api_risco()
    
        # Chamar dados api_meteorologica
        dft = get_api_meteorologia()

        df_risco.reset_index(drop=True, inplace=True)
        dft.reset_index(drop=True, inplace=True)

        # Adiciona os campos 'grav' e 'data_inicial' e seus valores
        dft['grav'] = df_risco['grav']
        dft['data_inicial'] = df_risco['data_inicial']

        # Converte 'data' e 'data_inicial' em objetos datetime
        dft['data'] = pd.to_datetime(dft['data'])
        dft['data_inicial'] = pd.to_datetime(dft['data_inicial'])

        # Adiciona 3 h em 'data' e 'data_inicial'
        dft['data'] = dft['data'] + timedelta(hours=3)
        dft['data_inicial'] = dft['data_inicial'] + timedelta(hours=3)

        # Converte as colunas de 'data' e 'data_inicial' em millisegundos, timestamp
        dft['data'] = dft['data'].apply(lambda x: int(x.timestamp() * 1000))
        dft['data_inicial'] = dft['data_inicial'].apply(
            lambda x: int(x.timestamp() * 1000))

        # Cria um geojson com os dados do dataframe dft
        geojson_features = []

        for index, row in dft.iterrows():
            feature = {
                "attributes": {
                    "temperatura": row['temperatura'],
                    "umidade": row['umidade'],
                    "vento": row['vento'],
                    "velocidade": row['velocidade do vento'],
                    "risco": row['grav'],
                    "inicial_risco": row['data_inicial'],
                    "data": row['data']
                }
            }

            # Adicionar a feature à lista
            geojson_features.append(feature)

        layer = connect_agol()

        features = geojson_features

        for feature in features:
            # Constrói a expressão SQL para encontrar a feature correspondente
            sql_expression = "objectid = 1"  # Atualiza apenas a linha com objectid 1

            # Cria um dicionário com os campos da Feature Layer e os valores correspondentes do GeoJSON
            values_to_update = {
                "temperatura": feature['attributes']['temperatura'],
                "umidade": feature['attributes']['umidade'],
                "vento": feature['attributes']['vento'],
                "velocidade": feature['attributes']['velocidade'],
                "risco": feature['attributes']['risco'],
                "inicial_risco": feature['attributes']['inicial_risco'],
                "data": feature['attributes']['data']
            }

            # Cria a lista de expressões para atualizar todos os campos de uma vez
            calc_expressions = [{"field": field_name, "value": value}
                                for field_name, value in values_to_update.items()]

            # Realiza a atualização de todos os campos
            layer.calculate(
                where=sql_expression,
                calc_expression=calc_expressions
            )

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erro ao executar fluxo: {e}")


if __name__ == "__main__":
    fire_risk_flow()
