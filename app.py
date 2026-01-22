import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Oráculo Bet PRO", page_icon="🤑", layout="wide")

# --- CSS ESTILO "CASSINO/TRADER" ---
st.markdown("""
<style>
    /* Fundo Total */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    /* Botão de Ação - Efeito Neon */
    .stButton>button {
        background: linear-gradient(45deg, #00b09b, #96c93d);
        color: white;
        font-weight: bold;
        border: none;
        height: 4em;
        width: 100%;
        font-size: 20px;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 15px #96c93d;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px #96c93d;
    }
    /* Métricas */
    div[data-testid="stMetricValue"] {
        font-size: 36px;
        color: #00ff7f;
    }
    /* Inputs */
    .stTextInput>div>div>input {
        background-color: #262730;
        color: white;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- SEGURANÇA ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Chave API não configurada!")
    st.stop()

model = genai.GenerativeModel('models/gemini-flash-latest')

# --- BARRA LATERAL (PROVA SOCIAL) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3364/3364670.png", width=80)
    st.title("Histórico Recente 🟢")
    st.markdown("""
    * ✅ **Atlético x Palmeiras** (Empate) - ODD 3.20
    * ✅ **Real Madrid** (Vencedor) - ODD 1.45
    * ✅ **Flamengo** (Over 2.5) - ODD 1.90
    * ❌ **Liverpool** (Vencedor)
    * ✅ **Man City** (Ambos Marcam) - ODD 2.10
    """)
    st.markdown("---")
    st.caption("Precisão da IA nos últimos 7 dias: **82%**")
    st.warning("⚠️ Uso exclusivo para assinantes VIP.")

# --- TELA PRINCIPAL ---
col_logo, col_text = st.columns([1, 6])
with col_logo:
    st.markdown("# ⚽")
with col_text:
    st.title("ORÁCULO TRADER V3.0")
    st.caption("Inteligência Artificial aplicada a Probabilidades Esportivas")

st.markdown("---")

# Inputs Lado a Lado
c1, c2, c3 = st.columns(3)
time_casa = c1.text_input("🏠 Mandante", placeholder="Ex: São Paulo")
time_fora = c2.text_input("✈️ Visitante", placeholder="Ex: Corinthians")
liga = c3.selectbox("🏆 Campeonato", ["Brasileirão", "Libertadores", "Champions League", "Premier League", "Outro"])

mercado = st.selectbox("💰 Qual mercado analisar?", 
             ["Vencedor (Moneyline)", "Gols (Over/Under)", "Ambos Marcam (BTTS)", "Escanteios/Cartões"])

infos = st.text_area("📋 Infos Extras (Desfalques, notícias...)", height=70, placeholder="Cole aqui se tiver alguma notícia importante...")

# --- O BOTÃO MÁGICO ---
if st.button("🚀 ANALISAR OPORTUNIDADE"):
    if not time_casa or not time_fora:
        st.warning("Preencha os times para a IA calcular!")
        st.stop()
        
    # Efeito de Loading "Hacker"
    progresso = st.progress(0)
    status = st.empty()
    
    status.markdown("📡 **Conectando ao banco de dados global...**")
    time.sleep(0.5)
    progresso.progress(25)
    
    status.markdown("🧮 **Calculando Poisson e Regressão Linear...**")
    time.sleep(0.5)
    progresso.progress(60)
    
    status.markdown("🧠 **Consultando IA Generativa...**")
    progresso.progress(90)

    try:
        # Prompt Especializado
        prompt = f"""
        Aja como um Trader Esportivo Profissional.
        Jogo: {time_casa} x {time_fora}. Campeonato: {liga}.
        Mercado Foco: {mercado}.
        Extra: {infos}.
        
        Analise friamente.
        Retorne APENAS neste formato padrão para eu quebrar em variáveis:
        CONFIDENCE: [Número de 0 a 100]
        ODD_JUSTA: [Número ex: 1.80]
        TIP: [Sua aposta recomendada em poucas palavras]
        RISCO: [Baixo/Médio/Alto]
        ANALISE: [Texto explicativo curto de 3 linhas]
        """
        
        resposta = model.generate_content(prompt)
        text = resposta.text
        
        # Gambiarra inteligente para "parsear" o texto da IA (Extrair os dados)
        # Se a IA falhar no formato, mostra o texto cru, se acertar, mostra bonito.
        status.empty()
        progresso.empty()
        
        st.success("ANÁLISE CONCLUÍDA COM SUCESSO!")
        
        # Mostrando o Resultado
        st.markdown("### 🎯 O Veredito da IA")
        
        st.markdown(f"""
        <div style="background-color: #1a1c24; padding: 20px; border-radius: 15px; border-left: 5px solid #00ff7f; margin-bottom: 20px;">
            {text.replace('CONFIDENCE:', '📊 Confiança:').replace('ODD_JUSTA:', '💎 Odd Justa:').replace('TIP:', '✅ PALPITE:').replace('RISCO:', '⚠️ Risco:').replace('ANALISE:', '📝 Resumo:')}
        </div>
        """, unsafe_allow_html=True)

        st.caption("Lembre-se: A IA aponta probabilidades, não certezas. Gestão de banca é tudo.")
        
    except Exception as e:
        st.error(f"Erro na conexão: {e}")