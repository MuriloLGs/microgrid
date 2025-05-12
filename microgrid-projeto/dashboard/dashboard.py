import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

st.set_page_config(page_title="Microgrid - Comunidade", layout="wide")

def gerar_dados_simulados(num_residencias=10):
    POTENCIA_PAINEL_KW = 5.0
    CAPACIDADE_BATERIA_KWH = 10.0

    comunidade = []
    for i in range(num_residencias):
        residencia = {
            "id": i + 1,
            "geracao": round(random.uniform(2.0, POTENCIA_PAINEL_KW), 2),
            "consumo": round(random.uniform(1.0, 6.0), 2),
            "bateria": round(random.uniform(2.0, CAPACIDADE_BATERIA_KWH), 2),
        }
        comunidade.append(residencia)

    gerado = sum(r["geracao"] for r in comunidade)
    consumido = sum(r["consumo"] for r in comunidade)
    armazenado = sum(r["bateria"] for r in comunidade)

    alerta = "Consumo excede geração + bateria!" if consumido > gerado + armazenado else "Operação normal"

    return {
        "timestamp": datetime.now().isoformat(),
        "residencias": comunidade,
        "totais": {
            "geracao_total_kwh": round(gerado, 2),
            "consumo_total_kwh": round(consumido, 2),
            "bateria_total_kwh": round(armazenado, 2)
        },
        "alerta": alerta
    }

st.title("Monitoramento de Energia - Microgrid Comunitária")

dados = gerar_dados_simulados()

st.markdown(f"**Atualizado em:** `{dados['timestamp']}`")
totais = dados['totais']

col1, col2, col3 = st.columns(3)
col1.metric("Total Gerado (kWh)", totais['geracao_total_kwh'])
col2.metric("Total Consumido (kWh)", totais['consumo_total_kwh'])
col3.metric("Total Armazenado (kWh)", totais['bateria_total_kwh'])

if "excede" in dados['alerta'].lower():
    st.warning(dados['alerta'])
else:
    st.success(dados['alerta'])

df = pd.DataFrame(dados['residencias'])

st.subheader("Histórico de Energia das Residências (Simulação Atual)")
fig = px.bar(
    df,
    x="id",
    y=["geracao", "consumo", "bateria"],
    barmode="group",
    labels={"value": "kWh", "id": "Residência"},
    title="Geração, Consumo e Armazenamento de Energia por Residência"
)
st.plotly_chart(fig, use_container_width=True)
