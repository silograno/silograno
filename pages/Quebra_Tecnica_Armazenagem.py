import streamlit as st
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Você precisa fazer login para acessar esta página.")
    st.stop()


import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da página
st.set_page_config(page_title="Quebra Técnica e Armazenagem", layout="wide")
st.title("📉 Quebra Técnica e Armazenagem")

# Caminho e aba
caminho_excel = r"C:\Users\arman\Desktop\SAFRAS\CONTROLE_SILO_GRANO_RESTAURADO\SISTEMA - CONTROLE - MILHO - SILO GRANO.xlsx"
aba_excel = "QUEBRA TECNICA - ARMAZENAGEM"  # sem acento

# Percentual fixo
PERCENTUAL_QUEBRA = 0.00015  # 0,015%

try:
    if not os.path.exists(caminho_excel):
        st.error("❌ Planilha não encontrada no caminho especificado.")
    else:
        # Ler colunas: Fornecedor (A), Data Inicial (B), Data Base (D), Peso Líquido (F)
        df = pd.read_excel(
            caminho_excel,
            sheet_name=aba_excel,
            usecols=[0, 1, 3, 5],
            header=0
        )

        # Renomear
        df.columns = ["Fornecedor", "Data Inicial", "Data Base", "Peso Líquido (kg)"]

        # Garantir tipos
        df["Data Inicial"] = pd.to_datetime(df["Data Inicial"], errors="coerce")
        df["Data Base"] = pd.to_datetime(df["Data Base"], errors="coerce")
        df["Peso Líquido (kg)"] = pd.to_numeric(df["Peso Líquido (kg)"], errors="coerce")

        # Seleção do fornecedor
        fornecedor_sel = st.selectbox("Selecione o Fornecedor:", df["Fornecedor"].dropna().unique())

        # Filtrar dados
        dados_forn = df[df["Fornecedor"] == fornecedor_sel].iloc[0]

        # Layout dividido
        col_esq, col_dir = st.columns([2, 1])

        # Coluna esquerda → dados do fornecedor
        with col_esq:
            st.subheader("📋 Informações do Fornecedor")
            st.metric("Data Inicial", dados_forn["Data Inicial"].strftime("%d/%m/%Y") if pd.notna(dados_forn["Data Inicial"]) else "-")
            st.metric("Data Base", dados_forn["Data Base"].strftime("%d/%m/%Y") if pd.notna(dados_forn["Data Base"]) else "-")
            st.metric("Peso Líquido (kg)", f"{dados_forn['Peso Líquido (kg)']:,.2f}" if pd.notna(dados_forn["Peso Líquido (kg)"]) else "-")

        # Coluna direita → cálculo
        with col_dir:
            st.subheader("⚙️ Calcular Quebra Técnica")
            data_calc = st.date_input("Data de Cálculo", datetime.today().date())

            dias_diferenca = None
            if pd.notna(dados_forn["Data Base"]):
                dias_diferenca = (data_calc - dados_forn["Data Base"].date()).days
                st.write(f"📅 Diferença de dias: **{dias_diferenca}**")

            if st.button("Calcular"):
                if dias_diferenca is not None and pd.notna(dados_forn["Peso Líquido (kg)"]):
                    quebra_kg = dados_forn["Peso Líquido (kg)"] * PERCENTUAL_QUEBRA * dias_diferenca
                    st.success(f"💡 Quebra Técnica: **{quebra_kg:,.2f} kg**")
                else:
                    st.warning("⚠️ Preencha corretamente as datas e verifique o peso líquido.")

except Exception as e:
    st.error(f"Erro ao processar dados: {e}")
