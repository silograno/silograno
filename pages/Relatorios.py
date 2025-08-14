import streamlit as st
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Você precisa fazer login para acessar esta página.")
    st.stop()


import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io

st.set_page_config(page_title="Relatórios", layout="wide")
st.title("📊 Relatórios do Controle Silo Grano")

# Caminho do arquivo Excel e aba
caminho_excel = r"C:\Users\arman\Desktop\SAFRAS\CONTROLE_SILO_GRANO_RESTAURADO\SISTEMA - CONTROLE - MILHO - SILO GRANO.xlsx"
aba_excel = "Controle Silo Grano"

# Colunas (índices base 0)
usecols = [0, 1, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

try:
    df = pd.read_excel(caminho_excel, sheet_name=aba_excel, usecols=usecols)

    # Renomear colunas
    df.columns = [
        "Fornecedor",
        "Cliente",
        "Nº Ticket",
        "Data",
        "Placa",
        "Motorista",
        "Entrada (kg)",
        "Saída (kg)",
        "Peso Líq (kg)",
        "Tipo",
        "Desconto Umidade (kg)",
        "Desconto Impureza (kg)",
        "Líquido Seco (kg)",
        "Sacas",
        "Umidade",
        "U.AP",
        "Impureza",
        "I.AP"
    ]

    # Limpar fornecedores inválidos
    df["Fornecedor"] = df["Fornecedor"].astype(str).str.strip()
    df = df[df["Fornecedor"] != "0"]
    df = df[df["Fornecedor"] != ""]
    df = df.dropna(subset=["Fornecedor"])

    # Garantir que números sejam numéricos
    col_quilos = ["Entrada (kg)", "Saída (kg)", "Peso Líq (kg)",
                  "Desconto Umidade (kg)", "Desconto Impureza (kg)",
                  "Líquido Seco (kg)"]
    col_sacas = ["Sacas"]
    col_percent = ["Umidade", "U.AP", "Impureza", "I.AP"]

    for col in col_quilos + col_sacas + col_percent:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Garantir que Data seja do tipo datetime
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

    # ---------------------------
    # SELEÇÃO DE FORNECEDOR
    # ---------------------------
    lista_fornecedores = sorted(df["Fornecedor"].unique())
    fornecedor_selecionado = st.selectbox("Selecione o fornecedor:", ["Todos"] + lista_fornecedores)

    if fornecedor_selecionado != "Todos":
        df_filtrado = df[df["Fornecedor"] == fornecedor_selecionado]
    else:
        df_filtrado = df.copy()

    # ---------------------------
    # FORMATAR OS DADOS
    # ---------------------------
    df_formatado = df_filtrado.copy()

    # Formatar pesos
    for col in col_quilos:
        df_formatado[col] = df_formatado[col].map(lambda x: f"{x:,.0f} kg" if pd.notnull(x) else "")

    # Formatar sacas
    for col in col_sacas:
        df_formatado[col] = df_formatado[col].map(lambda x: f"{x:,.3f} sc" if pd.notnull(x) else "")

    # Formatar porcentagens
    for col in col_percent:
        df_formatado[col] = df_formatado[col].map(lambda x: f"{x:.2f}%" if pd.notnull(x) else "")

    # Formatar data
    df_formatado["Data"] = df_formatado["Data"].dt.strftime("%d/%m/%Y")

    # ---------------------------
    # DETALHAMENTO COMPLETO
    # ---------------------------
    st.subheader("Detalhamento Completo")
    df_sorted = df_formatado.sort_values(["Fornecedor", "Data"])
    st.dataframe(df_sorted, use_container_width=True)

    # ---------------------------
    # FUNÇÃO PARA GERAR PDF
    # ---------------------------
    def gerar_pdf(dados, titulo_relatorio):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=20,
            leftMargin=20,
            topMargin=20,
            bottomMargin=20
        )

        elementos = []
        styles = getSampleStyleSheet()

        # Título
        elementos.append(Paragraph(titulo_relatorio, styles['Title']))
        elementos.append(Spacer(1, 12))

        # Converter DataFrame para lista de listas
        tabela_dados = [list(dados.columns)] + dados.values.tolist()

        tabela = Table(tabela_dados, repeatRows=1)
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#4F81BD")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 0.25, colors.black)
        ]))

        elementos.append(tabela)
        doc.build(elementos)
        buffer.seek(0)
        return buffer

    # ---------------------------
    # BOTÃO PARA GERAR E BAIXAR PDF
    # ---------------------------
    if st.button("📄 Gerar PDF (A4 Paisagem)"):
        pdf_buffer = gerar_pdf(df_sorted, "Relatório de Controle Silo Grano")
        st.download_button(
            label="⬇ Baixar PDF",
            data=pdf_buffer,
            file_name="relatorio_controle_silo_grano.pdf",
            mime="application/pdf"
        )

except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
