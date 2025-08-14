import streamlit as st
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Você precisa fazer login para acessar esta página.")
    st.stop()


import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Estoque/Financeiro", layout="wide")
st.title("📦 Estoque / Financeiro")

# Caminho do Excel principal
caminho_excel = r"C:\Users\arman\Desktop\SAFRAS\CONTROLE_SILO_GRANO_RESTAURADO\SISTEMA - CONTROLE - MILHO - SILO GRANO.xlsx"

# Funções de formatação
def format_sacas(valor):
    return f"{valor:,.0f} sc".replace(",", ".")

def format_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Verifica se o arquivo existe
if not os.path.exists(caminho_excel):
    st.error(f"Arquivo não encontrado: {caminho_excel}")
else:
    try:
        # ------------------------
        # 1️⃣ Leitura da aba Financeiro
        # ------------------------
        aba_financeiro = "Financeiro"
        df_financeiro = pd.read_excel(caminho_excel, sheet_name=aba_financeiro, usecols="A:H")

        # Renomeia colunas relevantes
        df_financeiro = df_financeiro.rename(columns={
            df_financeiro.columns[0]: "Fornecedor",
            df_financeiro.columns[2]: "Entrada (sc)",
            df_financeiro.columns[4]: "Saída (sc)",
            df_financeiro.columns[6]: "Saldo (sc)",
            df_financeiro.columns[7]: "Receita (R$)"
        })

        # Remove linhas sem fornecedor
        df_financeiro = df_financeiro.dropna(subset=["Fornecedor"])

        # Converte valores numéricos
        df_financeiro["Entrada (sc)"] = pd.to_numeric(df_financeiro["Entrada (sc)"], errors="coerce").fillna(0)
        df_financeiro["Saída (sc)"] = pd.to_numeric(df_financeiro["Saída (sc)"], errors="coerce").fillna(0)
        df_financeiro["Saldo (sc)"] = pd.to_numeric(df_financeiro["Saldo (sc)"], errors="coerce").fillna(0)
        df_financeiro["Receita (R$)"] = pd.to_numeric(df_financeiro["Receita (R$)"], errors="coerce").fillna(0)

        # ------------------------
        # 2️⃣ Formatação para exibição
        # ------------------------
        df_financeiro["Entrada (sc)"] = df_financeiro["Entrada (sc)"].apply(format_sacas)
        df_financeiro["Saída (sc)"] = df_financeiro["Saída (sc)"].apply(format_sacas)
        df_financeiro["Saldo (sc)"] = df_financeiro["Saldo (sc)"].apply(format_sacas)
        df_financeiro["Receita (R$)"] = df_financeiro["Receita (R$)"].apply(format_reais)

        # ------------------------
        # 3️⃣ Exibe tabela
        # ------------------------
        st.subheader("📊 Estoque Atual / Fornecedor")
        st.dataframe(df_financeiro[["Fornecedor", "Entrada (sc)", "Saída (sc)", "Saldo (sc)", "Receita (R$)"]],
                     use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao processar dados: {e}")
