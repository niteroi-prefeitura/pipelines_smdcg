import os
import requests
import pandas as pd
from arcgis.gis import GIS
from arcgis.gis import Item
from dotenv import load_dotenv
from prefect import task, flow
from arcgis.features import FeatureLayer
from datetime import datetime, timedelta

from prefect import flow
from prefect.variables import Variable
from prefect.blocks.system import Secret

load_dotenv()

user_portal = Secret.load("usuario-pmngeo-portal").get()
user_agol = Secret.load("usuario-integrador-agol").get()
gis_variables = Variable.get("gis_portal_variables")
svida_variables = Variable.get("svida_variables")

PORTAL_USERNAME: os.getenv("PORTAL_USERNAME", user_portal["username"])
PORTAL_PASSWORD: os.getenv("PORTAL_PASSWORD", user_portal["password"])


URL_TO_GENERATE_TOKEN: os.getenv("URL_TO_GENERATE_TOKEN", gis_variables["URL_TO_GENERATE_TOKEN"])
URL_GIS_ENTERPRISE: os.getenv("URL_GIS_ENTERPRISE", gis_variables["URL_GIS_ENTERPRISE"])


AGOL_USERNAME: os.getenv("AGOL_USERNAME", user_agol["username"])
AGOL_PASSWORD: os.getenv("AGOL_PASSWORD", user_agol["password"])


LAYER_NAME_PORTAL_HIST_PLUV: os.getenv("LAYER_NAME_PORTAL_HIST_PLUV", svida_variables["LAYER_NAME_PORTAL_HIST_PLUV"])
LAYER_ID_AGOL_SVIDA: os.getenv("LAYER_ID_AGOL_SVIDA", svida_variables["LAYER_ID_AGOL_SVIDA"])


URL_PREVISAO_API: os.getenv("URL_PREVISAO_API", svida_variables["URL_PREVISAO_API"])
URL_PONTOS_APOIO_API: os.getenv("URL_PONTOS_APOIO_API", svida_variables["URL_PONTOS_APOIO_API"])
URL_PLUVIOMETROS_API: os.getenv("URL_PLUVIOMETROS_API", svida_variables["URL_PLUVIOMETROS_API"])
URL_ESTAGIO_ATENC_API: os.getenv("URL_ESTAGIO_ATENC_API", svida_variables["URL_ESTAGIO_ATENC_API"])
URL_SIRENES_API: os.getenv("URL_SIRENES_API", svida_variables["URL_SIRENES_API"])
URL_METEOROLOGIA_API: os.getenv("URL_METEOROLOGIA_API", svida_variables["URL_METEOROLOGIA_API"])
URL_AVISOS_API: os.getenv("URL_AVISOS_API", svida_variables["URL_AVISOS_API"])


# Função para tratar colunas em texto para numéricas


@task
def columsnum(df, coluna):
    df[coluna] = df[coluna].astype(float)
    return df

# Função Previsão


@task
def weather_preview():
    response = requests.get(URL_PREVISAO_API)
    var_dict = response.__dict__
    content = var_dict['_content']
    values = content.decode().split(';')

    # remover coluna extra
    values = values[:-1]

    # Criar DataFrame com validação do número de colunas
    df = pd.DataFrame([values], columns=['tx_hoje', 'tx_amanhã'])

    return df

# PONTOS DE APOIO


@task
def support_places():

    # Acessando a API
    response = requests.get(URL_PONTOS_APOIO_API)
    # Transoformando a resposta em texto
    support_places_str = response.text
    # Separando pontos de apoio em itens de uma lista
    support_places_list = support_places_str.split('\n')
    # Criando a base de dados
    df = pd.DataFrame(columns=['tx_local', 'fl_lat', 'fl_lon', 'tx_endereco'])
    # Contando quantidade de colunas de um df
    qt_col_df = df.shape[1]
    # Tratando dados
    for support_places in support_places_list:
        support_places_txt = str(support_places)
        if len(support_places_txt) > 0:
            support_places_line = support_places_txt.split(';')
            # Testando se o numero de colunas é o mesmo
            if qt_col_df == len(support_places_line):
                # Append no DF
                df.loc[len(df)] = support_places_line
    # Tratando colunas numéricas
    df = columsnum(df, 'fl_lat')
    df = columsnum(df, 'fl_lon')

    return df

# Função dos pluviômetros


@task
def pluv_treatment():

    response_pluv = requests.get(URL_PLUVIOMETROS_API)

    # Estruturando o DataFrame de pluv.
    df = pd.DataFrame(columns=['fl_lat', 'fl_lon', 'tx_estacao', 'tx_cidade',
                               'dt_data', 'fl_ppnow', 'fl_pp1h', 'fl_pp4h', 'fl_pp24h', 'fl_pp96h',
                               'fl_pp30d', 'tx_atraso', 'tx_orgao'])

    # Coletando as informações em texto
    pluv_str = response_pluv.text

    # Separando em lista
    pluv_list = pluv_str.split('\n')

    # Colocando itens no Dataframe
    for pluv in pluv_list:
        line_pluv_str = str(pluv)
        if len(line_pluv_str) > 0:
            line_list = line_pluv_str.split(';')
            qt_col_df = df.shape[1]
            if qt_col_df == len(line_list):
                df.loc[len(df)] = line_list

    # Tratando colunas numéricas
    list_col = ['fl_lat', 'fl_lon', 'fl_ppnow', 'fl_pp1h',
                'fl_pp4h', 'fl_pp24h', 'fl_pp96h', 'fl_pp30d']
    for col in list_col:
        df = columsnum(df, col)

    # Filtrando para manter apenas os registros mais recentes por estação
    df = df.sort_values(by='dt_data', ascending=True).drop_duplicates(
        subset=['tx_estacao'], keep='first')

    # Resetando o índice do DataFrame
    df = df.reset_index(drop=True)

    return df

# Função para gerar token e conectar tabela de histotico de pluv no Portal


@task
def portal_conection():
    # Dados de autenticação
    token_url = URL_TO_GENERATE_TOKEN
    params = {
        "username": PORTAL_USERNAME,
        "password": PORTAL_PASSWORD,
        "referer": URL_GIS_ENTERPRISE,
        "f": "json",
    }

    # Requisição para gerar o token
    response = requests.post(token_url, data=params)

    # Verificar a resposta
    if response.status_code == 200:
        token_info = response.json()
        print(f"Token gerado: {token_info['token']}")
    else:
        print(f"Erro ao gerar token: {response.text}")

    ### Sobe os dados para a Camada ###

    # Função para atualizar os valores da camada existente
    url = f"{URL_GIS_ENTERPRISE}/portal"
    token = token_info['token']

    # Conectar ao portal com o token
    gis = GIS(url, token=token)

    layer_name = LAYER_NAME_PORTAL_HIST_PLUV
    item = 0
    # Access the feature layer
    pluv_hist = FeatureLayer(
        f"https://sig.niteroi.rj.gov.br/server/rest/services/{layer_name}/FeatureServer/{item}")

    return pluv_hist

# Função para processar e atualizar a camada de pluviômetros


@task
def update_pluv(layer, df, id_column, fl_columns, geometry_cols, history_table):
    """
    Atualiza uma camada do ArcGIS apenas com os registros alterados e
    registra essas mudanças em uma lista para posterior armazenamento na tabela de histórico.

    Args:
        layer: FeatureLayer do ArcGIS a ser atualizado.
        df: DataFrame com os dados novos.
        id_column: Coluna de identificação única (ex: 'tx_estacao').
        fl_columns: Lista de colunas a serem verificadas para mudanças (ex: colunas 'fl_*').
        geometry_cols: Colunas de coordenadas (ex: ['fl_lat', 'fl_lon']).
        history_table: Camada do ArcGIS onde serão adicionados os registros alterados.

    Returns:
        Lista de mudanças (registros alterados) para adicionar ao histórico.
    """

    # Função para ajustar a data no formato do histórico
    def adjust_date_for_history(date_str):
        # Assumindo que a entrada é no formato BR
        original_date = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
        adjusted_date = original_date + timedelta(hours=3)  # Adiciona 3 horas
        # Formato esperado no histórico
        return adjusted_date.strftime("%m/%d/%Y %H:%M")

    # Consulta na camada do ArcGIS
    existing_features = layer.query(
        out_fields=[id_column] + fl_columns, return_geometry=True).features

    # Convertendo os dados da camada para um DataFrame
    if existing_features:
        existing_data = pd.DataFrame([
            {**feat.attributes, "geometry": feat.geometry}
            for feat in existing_features
        ])
    else:
        existing_data = pd.DataFrame()

    # Se a camada estiver vazia, adicionamos todos os registros do df
    if existing_data.empty:
        print("A camada está vazia. Adicionando todos os registros do DataFrame.")
        new_records = [
            {
                "attributes": {
                    **{col: row[col] for col in [id_column] + fl_columns},
                    "dt_data": row["dt_data"]
                },
                "geometry": {
                    "x": float(row[geometry_cols[1]]),
                    "y": float(row[geometry_cols[0]]),
                    "spatialReference": {"wkid": 4326},
                }
            }
            for _, row in df.iterrows()
        ]
        result = layer.edit_features(adds=new_records)
        print(f"Novos registros adicionados à camada: {result}")
        return

    # Inicializar listas
    changed_records = []
    new_records = []
    history_records = []

    for _, row in df.iterrows():
        estacao_id = row[id_column]

        # Verificar se a estação já existe no existing_data
        matching_records = existing_data[existing_data[id_column]
                                         == estacao_id]

        # Criar dicionário de atributos
        attributes = {
            **{col: row[col] for col in fl_columns},
            "tx_estacao": estacao_id,
            "dt_data": row["dt_data"]
        }

        # Definir geometria
        geometry = {
            "x": float(row[geometry_cols[1]]),
            "y": float(row[geometry_cols[0]]),
            "spatialReference": {"wkid": 4326},
        }

        if not matching_records.empty:
            # Comparar o campo de data
            existing_date = matching_records.iloc[0]["dt_data"]
            if existing_date != row["dt_data"]:
                # Adicionar ao histórico se a data mudou
                history_attributes = attributes.copy()
                history_attributes["dt_data"] = adjust_date_for_history(
                    row["dt_data"])
                history_records.append({
                    "attributes": history_attributes
                })

            # Atualizar todos os registros encontrados para a estação
            for _, matching_row in matching_records.iterrows():
                object_id = matching_row["OBJECTID"]
                changed_records.append({
                    "attributes": {**attributes, "OBJECTID": object_id},
                    "geometry": geometry
                })
        else:
            # Adicionar como novo registro se não encontrado
            new_records.append({
                "attributes": attributes,
                "geometry": geometry
            })

    # Adicionar registros ao histórico somente para fl_now > 0
    filtered_history_records = [
        record for record in history_records if record["attributes"]["fl_ppnow"] > 0
    ]

    # Atualizar registros existentes na camada
    if changed_records:
        try:
            result = layer.edit_features(updates=changed_records)
            print(f"Registros atualizados: {result}")
        except Exception as e:
            print(f"Erro ao atualizar registros: {e}")

    # Adicionar novos registros à camada
    if new_records:
        try:
            result = layer.edit_features(adds=new_records)
            print(f"Novos registros adicionados: {result}")
        except Exception as e:
            print(f"Erro ao adicionar novos registros: {e}")

    # Adicionar registros ao histórico
    if filtered_history_records:
        try:
            result = history_table.edit_features(adds=filtered_history_records)
            print(f"Registros adicionados ao histórico: {result}")
        except Exception as e:
            print(f"Erro ao adicionar ao histórico: {e}")
    else:
        print("Nenhum registro adicionado ao histórico.")

    return {
        "changed_records": changed_records,
        "new_records": new_records,
        "history_records": history_records
    }

# ESTAGIO DE ATENCAO


@task
def attention_stage(now):
    # Acessando API
    response_atenc = requests.get(URL_ESTAGIO_ATENC_API)

    # Coletando as informações em texto
    pluv_str = response_atenc.text

    # Tratando o texto
    pluv_str = pluv_str.replace("\n", "")

    # Coletando data e hora
    data = now

    # Etruturando df
    df = pd.DataFrame({'tx_estagio': [pluv_str], 'dt_data': [data]})

    return df

# SIRENES


@task
def sirens():
    # Acessando API
    response_sirens = requests.get(URL_SIRENES_API)

    # Estruturando o DataFrame das sirenes.
    df = pd.DataFrame(columns=['fl_lat', 'fl_lon', 'tx_sirene', 'tx_cidade',
                               'tx_campo1', 'tx_status', 'tx_campo2'])

    # Coletando as informações em texto
    sirens_str = response_sirens.text

    # Separando em lista
    sirens_list = sirens_str.split('\n')

    # Colocando itens no Dataframe
    for siren in sirens_list:
        siren_line_str = str(siren)
        if len(siren_line_str) > 0:
            line_list = siren_line_str.split(';')
            qt_col_df = df.shape[1]
            if qt_col_df == len(line_list):
                df.loc[len(df)] = line_list

    # Tratando colunas numéricas
    df = columsnum(df, 'fl_lat')
    df = columsnum(df, 'fl_lon')

    return df

# RADAR METEOROLÓGICO


@task
def meteorology():
    # Acessando API
    response_meteoro = requests.get(URL_METEOROLOGIA_API)

    # Estruturando o DataFrame meteorológico.
    df = pd.DataFrame(columns=['tx_nome', 'fl_lat', 'fl_lon', 'fl_temp',
                               'fl_umidade', 'tx_dir_vento', 'fl_velvento', 'dt_campo1', 'tx_campo2'])

    # Coletando as informações em texto
    meteoro_str = response_meteoro.text

    # dividindo as colunas
    meteoro_list = meteoro_str.split(';')

    # Armazenando o numero de colunas no DF para comparar com a lista ++++APLICAR PROS OUTROS +++
    qt_col_df = df.shape[1]
    if qt_col_df == len(meteoro_list):
        # Anexando informações na base de dados
        df.loc[len(df)] = meteoro_list

    # Tratando colunas numéricas
    df = columsnum(df, 'fl_lat')
    df = columsnum(df, 'fl_lon')

    return df

# AVISOS


@task
def alerts():
    # Acessando API
    response_alerts = requests.get(URL_AVISOS_API)
    alerts_dict = response_alerts.__dict__
    values = alerts_dict['_content']

    # Decodificando para string e dividindo em colunas.
    values = values.decode().split(';')

    # Estruturando df
    df = pd.DataFrame([values], columns=['tx_titulo',
                      'tx_descrip', 'tx_titulo1', 'tx_nivel'])
    df['tx_nivel'] = df['tx_nivel'].str.strip()

    return df

# Função GIS


@task
def gis_function(df_pluv, df_attention_stage, df_support_place, df_weather_preview, df_sirens, df_meteoro, df_alerts, now, pluv_hist):

    # Conectando ao Agol
    url = "https://www.arcgis.com"
    usr = AGOL_USERNAME
    pwd = AGOL_PASSWORD
    gis = GIS(url, usr, pwd)

    # listar layers
    layer_id = LAYER_ID_AGOL_SVIDA
    portal_item = Item(gis, layer_id)

    layers = portal_item.layers
    tables = portal_item.tables

    pluv = layers[0]
    support_places = layers[1]
    weather_radar = layers[2]
    sirens = layers[3]
    alerts = tables[3]
    attention_stage = tables[1]
    weather_preview = tables[0]

    def process_layer(layer, df, geometry_cols, attr_cols, spatial_ref=4326):
        existing_features = layer.query(out_fields=["OBJECTID"]).features
        delete_oids = [feat.attributes["OBJECTID"]
                       for feat in existing_features]

        features_to_add = []
        for _, row in df.iterrows():
            geometry = {
                "x": row[geometry_cols[0]],
                "y": row[geometry_cols[1]],
                "spatialReference": {"wkid": spatial_ref},
            }
            attributes = {col: row[col] if pd.notna(
                row[col]) else None for col in attr_cols}
            features_to_add.append(
                {"geometry": geometry, "attributes": attributes})

        add_result = layer.edit_features(adds=features_to_add)

        if delete_oids:
            layer.delete_features(deletes=",".join(map(str, delete_oids)))

        return add_result

    def process_table(layer, df, attr_cols):
        # Coleta OBJECTIDs existentes
        existing_features = layer.query(out_fields=["OBJECTID"]).features
        delete_oids = [feat.attributes["OBJECTID"]
                       for feat in existing_features]

        # Constrói lista de features a adicionar
        features_to_add = []
        for _, row in df.iterrows():
            attributes = {col: row[col] if pd.notna(
                row[col]) else None for col in attr_cols}
            features_to_add.append({"attributes": attributes})

        # Realiza a adição
        add_result = layer.edit_features(adds=features_to_add)

        # Remove antigos
        if delete_oids:
            layer.delete_features(deletes=",".join(map(str, delete_oids)))

        return add_result

    # Atualizando os dados de pluviômetros com `update_pluv`
    update_pluv(
        layer=pluv,
        df=df_pluv,
        id_column="tx_estacao",
        fl_columns=['tx_estacao', 'tx_cidade', 'dt_data', 'fl_ppnow', 'fl_pp1h', 'fl_pp4h',
                    'fl_pp24h', 'fl_pp96h', 'fl_pp30d', 'tx_atraso', 'tx_orgao'],
        geometry_cols=["fl_lat", "fl_lon"],
        history_table=pluv_hist,
    )

    process_layer(support_places, df_support_place, ["fl_lon", "fl_lat"],
                  ['tx_local', 'tx_endereco'])

    process_layer(weather_radar, df_meteoro, ["fl_lon", "fl_lat"],
                  ['tx_nome', 'fl_temp', 'fl_umidade', 'tx_dir_vento',
                   'fl_velvento', 'dt_campo1', 'tx_campo2'])

    process_layer(sirens, df_sirens, ["fl_lon", "fl_lat"],
                  ['tx_sirene', 'tx_cidade', 'tx_campo1', 'tx_status', 'tx_campo2'])

    process_table(alerts, df_alerts, [
                  'tx_titulo', 'tx_descrip', 'tx_titulo1', 'tx_nivel'])

    process_table(attention_stage, df_attention_stage,
                  ['tx_estagio', 'dt_data'])

    process_table(weather_preview, df_weather_preview,
                  ['tx_hoje', 'tx_amanhã'])

# Função principal


@flow(name="fluxo-svida-smdcg")
def svida_integration_flow():
    now = datetime.now()
    apk = []
    erros = []

    processos = {
        "Pluviômetros": pluv_treatment,
        "Estágio de Atenção": lambda: attention_stage(now),
        "Pontos de Apoio": support_places,
        "Previsão": weather_preview,
        "Sirenes": sirens,
        "Radar Meteorológico": meteorology,
        "Avisos": alerts,
    }

    results = {}
    for name, function in processos.items():
        try:
            results[name] = function()
        except Exception as e:
            print(f"Erro ao carregaro df - {name}: {str(e)}")
            apk.append(name)
            erros.append(e)
        else:
            print(f"{name} carregado com sucesso")

    try:
        # Conectar ao Portal e obter o pluv_hist
        pluv_hist = portal_conection()
    except Exception as e:
        print(f"Erro ao conectar ao Portal: {str(e)}")
        apk.append("Conexão Portal")
        erros.append(e)
    else:
        print("Conexão ao Portal realizada com sucesso")

    try:
        gis_function(
            results.get("Pluviômetros"),
            results.get("Estágio de Atenção"),
            results.get("Pontos de Apoio"),
            results.get("Previsão"),
            results.get("Sirenes"),
            results.get("Radar Meteorológico"),
            results.get("Avisos"),
            now,
            pluv_hist=pluv_hist
        )
    except Exception as e:
        print(f"Erro na integração GIS: {str(e)}")
        apk.append("GIS")
        erros.append(e)
    else:
        print("Feições e tabelas atualizadas com sucesso")


if __name__ == "__main__":
    svida_integration_flow()
