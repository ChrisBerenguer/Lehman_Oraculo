# =============================================================================
# Oráculo – Copiloto Executivo de Inteligência Organizacional
# Fundação Lemann · Front-end de Alta Fidelidade (dados mockados)
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import os


# ──────────────────────────────────────────────────────────────────────────────
# 1. CONFIGURAÇÃO DA PÁGINA
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Oráculo · Fundação Lemann",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# 2. CSS – DESIGN SYSTEM FUNDAÇÃO LEMANN
# ──────────────────────────────────────────────────────────────────────────────
FL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Cabin:ital,wght@0,400;0,600;0,700;1,400&display=swap');

:root {
  --fl-navy:       #052B47;
  --fl-navy-mid:   #0C436B;
  --fl-navy-deep:  #083050;
  --fl-navy-text:  #011B2E;
  --fl-lime:       #B2C530;
  --fl-teal:       #00A180;
  --fl-pink:       #DA7680;
  --fl-white:      #FFFFFF;
  --fl-grey:       #f5f7fa;
  --fl-grey-mid:   #e2e8f0;
  --fl-grey-text:  #6b8399;
  --shadow-sm:     0 2px 8px rgba(5,43,71,.08);
  --shadow-md:     0 4px 20px rgba(5,43,71,.12);
  --radius:        12px;
}

html, body, [class*="css"] {
  font-family: 'Cabin', sans-serif !important;
  color: var(--fl-navy-text);
}

.main .block-container {
  padding: 1.5rem 2rem 3rem !important;
}

header[data-testid="stHeader"] {
  visibility: hidden;
}
header[data-testid="stHeader"] button[data-testid="stSidebarCollapse"] {
  visibility: visible;
  color: var(--fl-navy) !important;
}

section[data-testid="stSidebar"] > div:first-child {
  background: var(--fl-navy) !important;
}
section[data-testid="stSidebar"] * { color: var(--fl-white) !important; }

.fl-page-title {
  font-family: 'Montserrat', sans-serif !important;
  font-size: 1.7em; font-weight: 800; color: var(--fl-navy);
  margin-bottom: 4px;
}
.fl-page-subtitle {
  font-family: 'Cabin', sans-serif;
  font-size: .95em; color: var(--fl-grey-text); margin-bottom: 28px;
}

.kpi-grid { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 32px; }
.kpi-card {
  flex: 1; min-width: 160px;
  background: var(--fl-white); border-radius: var(--radius);
  padding: 22px 24px; box-shadow: var(--shadow-sm);
  border-left: 4px solid var(--fl-lime);
}
.kpi-card.risk { border-left-color: var(--fl-pink); }
.kpi-card.teal { border-left-color: var(--fl-teal); }
.kpi-card.navy { border-left-color: var(--fl-navy-mid); }
.kpi-label { font-size:.72em; font-weight:700; text-transform:uppercase; color:var(--fl-grey-text); margin-bottom:8px; }
.kpi-value { font-family:'Montserrat',sans-serif; font-size:2em; font-weight:800; color:var(--fl-navy); }
.kpi-delta { font-size:.78em; margin-top:6px; color:var(--fl-teal); font-weight:600; }
.kpi-delta.neg { color:var(--fl-pink); }

.fl-card {
  background: var(--fl-white); border-radius: var(--radius);
  padding: 24px; box-shadow: var(--shadow-sm);
  margin-bottom: 16px;
}

.badge { display:inline-block; padding:3px 10px; border-radius:20px; font-size:.72em; font-weight:700; }
.badge-ok { background: rgba(0,161,128,.12); color: var(--fl-teal); }
.badge-warn { background: rgba(178,197,48,.15); color: #7a8f00; }
.badge-risk { background: rgba(218,118,128,.15); color: #c03040; }

.chat-msg { display:flex; gap:12px; margin-bottom:16px; }
.chat-avatar { width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; }
.avatar-user { background:var(--fl-navy); color:var(--fl-lime); }
.avatar-bot { background:var(--fl-lime); color:var(--fl-navy); }
.chat-bubble { max-width:80%; padding:14px 18px; border-radius:16px; font-size:.92em; line-height:1.6; box-shadow: var(--shadow-sm); }
.bubble-user { background:var(--fl-navy); color:var(--fl-white); }
.bubble-bot { background:var(--fl-white); border:1px solid var(--fl-grey-mid); }

.fl-table { width:100%; border-collapse:collapse; font-size:.85em; }
.fl-table th { background:var(--fl-navy); color:var(--fl-white); padding:12px 14px; text-align:left; }
.fl-table td { padding:12px 14px; border-bottom:1px solid var(--fl-grey-mid); }

.prog-bar-bg { background:var(--fl-grey-mid); border-radius:4px; height:8px; width:100%; }
.prog-bar-fill { background:var(--fl-teal); height:8px; border-radius:4px; }
.prog-bar-fill.warn { background:var(--fl-lime); }
.prog-bar-fill.risk { background:var(--fl-pink); }

.insight-card { flex:1; min-width:200px; background:var(--fl-white); border-radius:var(--radius); padding:20px; box-shadow:var(--shadow-sm); border-top:3px solid var(--fl-lime); }

/* Customização do Botão de Sair na Sidebar */
[data-testid="stSidebar"] button {
  background-color: var(--fl-lime) !important;
  color: var(--fl-navy) !important;
  border: 1px solid var(--fl-lime) !important;
  font-weight: 700 !important;
  transition: all 0.3s ease !important;
}

[data-testid="stSidebar"] button:hover {
  background-color: var(--fl-white) !important;
  color: var(--fl-navy) !important;
  border-color: var(--fl-white) !important;
}

/* Cor preta para o texto selecionado nos selectboxes da sidebar */
[data-testid="stSidebar"] [data-baseweb="select"] * {
  color: #000000 !important;
}
</style>
"""
st.markdown(FL_CSS, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# 3. DADOS MOCKADOS
# ──────────────────────────────────────────────────────────────────────────────
def load_mock_data():
    iniciativas = pd.DataFrame([
        {"Iniciativa": "Alfabetização em Rede", "Frente": "Educação Pública", "Status": "Em dia", "Conclusão": 82, "Responsável": "Ana Paula M."},
        {"Iniciativa": "Líderes do Amanhã", "Frente": "Lideranças", "Status": "Atenção", "Conclusão": 51, "Responsável": "Renata Souza"},
        {"Iniciativa": "Conectividade Escolar", "Frente": "Educação Pública", "Status": "Em risco", "Conclusão": 34, "Responsável": "Juliana Costa"},
    ])
    recursos = pd.DataFrame({
        "Frente": ["Educação Pública", "Lideranças", "Ecossistema", "Operações"],
        "Valor (R$ M)": [18.4, 14.7, 8.1, 4.2],
    })
    status_counts = {"Em dia": 18, "Atenção": 7, "Em risco": 3}
    return {"iniciativas": iniciativas, "recursos": recursos, "status_counts": status_counts}

MOCK = load_mock_data()

MOCK_RESPONSES = {
    "Status das iniciativas": {
        "answer": "O status geral das iniciativas é positivo, com 73% das metas atingidas.",
        "sources": ["Relatório Q1-2025", "Planilha de Metas"]
    }
}

# ──────────────────────────────────────────────────────────────────────────────
# 4. SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Inserindo o logo no topo com caminho absoluto relativo ao app.py
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "fundacaoLemann-branco-300x105_55944460b060.png")
        st.image(logo_path, use_container_width=True)
        st.markdown("### Oráculo")
        page = st.radio("Navegação", ["Chat Inteligente", "Dashboard Executiva"])
        
        # Seletor de Período com default Q1 2025
        periodos = ["Q1 2025", "Q2 2025"]
        st.selectbox("Período", periodos, index=0)

        # Botão de Sair mocado (ilustrativo)
        st.markdown("<br><br>", unsafe_allow_html=True) # Espaçamento
        if st.button("Sair", use_container_width=True):
            pass 
    return page

# ──────────────────────────────────────────────────────────────────────────────
# 5. PÁGINAS
# ──────────────────────────────────────────────────────────────────────────────
def render_chat_page():
    st.markdown("<div class='fl-page-title'>Chat Inteligente</div>", unsafe_allow_html=True)
    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    
    for msg in st.session_state.chat_history:
        cls = "user" if msg["role"] == "user" else "bot"
        st.markdown(f"<div class='chat-msg'><div class='chat-avatar avatar-{cls}'>{'U' if cls=='user' else 'O'}</div><div class='chat-bubble bubble-{cls}'>{msg['content']}</div></div>", unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Pergunta", placeholder="Como estamos em educação?")
        if st.form_submit_button("Enviar") and user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": f"Analisando dados... {MOCK_RESPONSES['Status das iniciativas']['answer']}"})
            st.rerun()

def render_dashboard_page():
    st.markdown("<div class='fl-page-title'>Dashboard Executiva</div>", unsafe_allow_html=True)
    
    # KPIs
    st.markdown("""
    <div class='kpi-grid'>
      <div class='kpi-card'><div class='kpi-label'>Metas Atingidas</div><div class='kpi-value'>73%</div><div class='kpi-delta'>+4pp</div></div>
      <div class='kpi-card teal'><div class='kpi-label'>Andamento</div><div class='kpi-value'>28</div><div class='kpi-delta'>Estável</div></div>
      <div class='kpi-card risk'><div class='kpi-label'>Em Risco</div><div class='kpi-value'>5</div><div class='kpi-delta neg'>-1</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Gráfico
    fig = px.bar(MOCK["recursos"], x="Frente", y="Valor (R$ M)", color="Frente", color_discrete_sequence=["#052B47", "#00A180", "#B2C530", "#DA7680"])
    st.plotly_chart(fig, use_container_width=True)

    # Tabela
    st.table(MOCK["iniciativas"])




# ──────────────────────────────────────────────────────────────────────────────
# 6. MAIN
# ──────────────────────────────────────────────────────────────────────────────
def main():
    page = render_sidebar()
    if "Chat" in page: render_chat_page()
    else: render_dashboard_page()

if __name__ == "__main__": main()
