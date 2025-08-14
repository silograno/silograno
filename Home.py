import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import os

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(page_title="Controle Silo Grano", page_icon="🌙", layout="wide")

# =========================
# USUÁRIO E SENHA (padrão)
# =========================
USUARIO_CORRETO = "adm.silo"
SENHA_CORRETA = "salmos23@18"

# =========================
# INICIAR SESSION STATE
# =========================
if "logado" not in st.session_state:
    st.session_state.logado = False

# =========================
# TELA DE LOGIN
# =========================
def tela_login():
    logo_path = "data/logo_trio_sem_fundo_2.PNG"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.image(logo, use_container_width=True)
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🌙 Controle Silo Grano</h1>", unsafe_allow_html=True)
    st.write("")  

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos!")

# =========================
# TELA PRINCIPAL (SISTEMA)
# =========================
def tela_sistema():
    # ---- FUNÇÕES DE FORMATAÇÃO ----
    def format_sacas(valor):
        return f"{valor:,.0f} sc".replace(",", ".")

    def format_reais(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # ---- LOGO E CABEÇALHO ----
    logo_path = "data/logo_trio_sem_fundo_2.PNG"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo, use_container_width=True)
            st.markdown("<h1 style='text-align: center; color: #2E86C1;'>📊 Controle</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size:18px; color: #555;'>Visualização de dados do sistema</p>", unsafe_allow_html=True)

    # ---- SELEÇÃO DE PRODUTO ----
    produto = st.selectbox("Selecione o Produto:", ["Milho", "Soja", "Sorgo", "Milheto", "Gado"])

    # Caminhos relativos (dentro da pasta 'data')
    caminhos_planilhas = {
        "Milho": "data/CONTROLE_SILO_MILHO.xlsx",
        "Soja": "data/CONTROLE_SILO_SOJA.xlsx",
        "Sorgo": "data/CONTROLE_SILO_SORGO.xlsx",
        "Milheto": "data/CONTROLE_SILO_MILHETO.xlsx",
        "Gado": "data/CONTROLE_SILO_GADO.xlsx"
    }

    caminho_excel = caminhos_planilhas.get(produto)

    # ---- PROCESSAMENTO DOS DADOS ----
    if not os.path.exists(caminho_excel):
        st.error("Planilha para o produto selecionado não encontrada. Verifique se ela está na pasta 'data'.")
    else:
        try:
            # Aba Financeiro
            aba_financeiro = "Financeiro"
            df_financeiro = pd.read_excel(caminho_excel, sheet_name=aba_financeiro, usecols="A:H")
            df_financeiro = df_financeiro.rename(columns={
                df_financeiro.columns[0]: "Fornecedor",
                df_financeiro.columns[2]: "Entrada (sacas)",
                df_financeiro.columns[4]: "Saída (sacas)",
                df_financeiro.columns[6]: "Saldo (sacas)",
                df_financeiro.columns[7]: "Receita (R$)"
            })
            df_financeiro = df_financeiro.dropna(subset=["Fornecedor"])

            # Totais
            total_entrada = df_financeiro["Entrada (sacas)"].sum()
            total_saida = df_financeiro["Saída (sacas)"].sum()
            total_saldo = df_financeiro["Saldo (sacas)"].sum()
            total_receita = df_financeiro["Receita (R$)"].sum()

            # Resumo Financeiro
            st.markdown("### 📌 Resumo Financeiro")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Entrada (sacas)", format_sacas(total_entrada))
            col2.metric("Total Saída (sacas)", format_sacas(total_saida))
            col3.metric("Saldo Total (sacas)", format_sacas(total_saldo))
            col4.metric("Receita Total (R$)", format_reais(total_receita))

        except Exception as e:
            st.error(f"Erro ao processar dados: {e}")

# =========================
# EXECUÇÃO
# =========================
if not st.session_state.logado:
    tela_login()
else:
    tela_sistema()
