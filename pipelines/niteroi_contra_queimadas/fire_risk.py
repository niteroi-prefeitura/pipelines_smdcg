import os
import json
import requests
import pandas as pd
from prefect import flow
from arcgis.gis import GIS
from dotenv import load_dotenv
from prefect import flow, task
from prefect.variables import Variable
from prefect.blocks.system import Secret

load_dotenv()
user_agol = Secret.load("usuario-integrador-agol").get()
smdcg_variables = Variable.get("smdcg_variables")
gis_variables = Variable.get("gis_portal_variables")

AGOL_USERNAME_TO_NCQ = os.getenv("AGOL_USERNAME_TO_NCQ") or user_agol["username"]
AGOL_PASSWORD_TO_NCQ = os.getenv("AGOL_PASSWORD_TO_NCQ") or user_agol["password"]
LAYER_ID_AGOL_METEOROLOGIA = (
    os.getenv("LAYER_ID_AGOL_METEOROLOGIA")
    or smdcg_variables["LAYER_ID_AGOL_METEOROLOGIA"]
)

URL_GIS_ENTERPRISE_GEONITEROI = (
    os.getenv("URL_GIS_ENTERPRISE_GEONITEROI")
    or gis_variables["URL_GIS_ENTERPRISE_GEONITEROI"]
)
URL_RISCO_FOGO_API = (
    os.getenv("URL_RISCO_FOGO_API") or smdcg_variables["URL_RISCO_FOGO_API"]
)
URL_METEOROLOGIA_API = (
    os.getenv("URL_METEOROLOGIA_API") or smdcg_variables["URL_METEOROLOGIA_API"]
)


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
        content_risk = var_dict_risk["_content"]

        # Utiliza o Json para transformar em dataframe
        obj1 = json.loads(content_risk)
        dfe0 = pd.DataFrame(obj1)
        dfe1 = pd.concat(
            [dfe0.drop(["fields"], axis=1), dfe0["fields"].apply(pd.Series)], axis=1
        )

        dfe1 = dfe1[dfe1["data_final"].isnull()]

        return dfe1
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erro ao consultar api risco: {e}")


@task
def get_api_meteorologia():
    try:
        response_weather = requests.get(URL_METEOROLOGIA_API)
        var_dict_weather = response_weather.__dict__
        content_weather = var_dict_weather["_content"]

        # Divide a string content_weather em colunas
        decode = content_weather.decode()  # decode de bytes para string

        rows = [line.split(";") for line in decode.strip().split("\n")]

        # Criando um dataframe
        dft = pd.DataFrame(
            rows,
            columns=[
                "Local",
                "Latitude",
                "Longitude",
                "temperatura",
                "umidade",
                "vento",
                "velocidade do vento",
                "data",
                "Velocidade_vento_2",
            ],
        )

        dft = dft.drop(columns=["Local", "Latitude", "Longitude", "Velocidade_vento_2"])

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
        dft["grav"] = df_risco["grav"]
        dft["data_inicial"] = df_risco["data_inicial"]

        dft["data"] = pd.to_datetime(dft["data"], dayfirst=True)
        dft["data_inicial"] = pd.to_datetime(dft["data_inicial"])
        dft["data"] = dft["data"].dt.tz_localize("America/Sao_Paulo")
        dft["data_inicial"] = dft["data_inicial"].dt.tz_convert("America/Sao_Paulo")

        dft["data"] = dft["data"].apply(lambda x: int(x.timestamp() * 1000))

        geojson_features = []

        for index, row in dft.iterrows():
            feature = {
                "attributes": {
                    "temperatura": row["temperatura"],
                    "umidade": row["umidade"],
                    "vento": row["vento"],
                    "velocidade": row["velocidade do vento"],
                    "risco": row["grav"],
                    "inicial_risco": row["data_inicial"],
                    "data": row["data"],
                }
            }
            geojson_features.append(feature)

        layer = connect_agol()

        to_update = geojson_features[0]["attributes"]

        calc_expressions = [
            {"field": field_name, "value": value}
            for field_name, value in to_update.items()
        ]

        resp = layer.calculate(where="objectid=1", calc_expression=calc_expressions)

        print(resp)

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erro ao executar fluxo: {e}")


if __name__ == "__main__":
    fire_risk_flow()
