import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Oráculo Bet AI", page_icon="⚽", layout="centered")

# --- CSS DARK MODE (ESTILO BET365/SPORTINGBET) ---
st.markdown("""
<style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    .stButton>button {
        background-color: #00ff00; /* Verde Green */
        color: black;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        height: 3em;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #00cc00;
        color: white;
    }
    h1, h2, h3 {
        color: #00ff00;
    }
    .stTextArea textarea {
        background-color: #1e1e1e;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- SEGURANÇA ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Configure a chave API no Secrets!")
    st.stop()

model = genai.GenerativeModel('models/gemini-flash-latest')

# --- LOGIN (Venda o acesso) ---
def check_password():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    if st.session_state["logged_in"]:
        return True

    st.title("⚽ Oráculo Bet AI")
    st.write("Acesso exclusivo para assinantes VIP.")
    
    senha = st.text_input("Chave de Acesso:", type="password")
    if st.button("Entrar no Sistema"):
        if senha == "GREEN123": # Sua senha de venda
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Acesso negado.")
    return False

if not check_password():
    st.stop()

# --- APP PRINCIPAL ---
st.image("https://i.ibb.co/wzkMc1r/soccer-ball-green.png", width=80) # Logo genérica
st.title("Oráculo Bet 🎯")
st.write("A Inteligência Artificial que analisa as probabilidades reais.")

st.markdown("---")

col1, col2 = st.columns(2)
time_casa = col1.text_input("Time da Casa", placeholder="Ex: Flamengo")
time_fora = col2.text_input("Time Visitante", placeholder="Ex: Palmeiras")

infos_extras = st.text_area(
    "Copie e cole estatísticas ou notícias (Opcional):",
    placeholder="Ex: O atacante titular está machucado. O time da casa vem de 3 derrotas...",
    height=100
)

bet_type = st.selectbox("Qual mercado você quer analisar?", 
                        ["Vencedor da Partida (1x2)", "Total de Gols (Over/Under)", "Ambos Marcam", "Escanteios"])

if st.button("🔮 GERAR PALPITE COM IA"):
    if not time_casa or not time_fora:
        st.warning("Preencha os nomes dos times!")
        st.stop()
        
    with st.spinner("Analisando histórico, probabilidades e momento..."):
        try:
            prompt = f"""
            Atue como um analista de dados esportivos profissional e frio.
            Jogo: {time_casa} x {time_fora}.
            Contexto extra: {infos_extras}
            Foco da análise: {bet_type}.
            
            Sua tarefa é encontrar valor matemático. Não seja torcedor.
            
            Gere uma saída assim:
            1. 📊 **Probabilidade Real:** (Dê uma porcentagem para o evento).
            2. 💡 **O Palpite da IA:** (Seja direto: Time X vence, ou Over 2.5 gols).
            3. ⚠️ **Risco:** (Baixo, Médio ou Alto).
            4. 📝 **Justificativa Rápida:** (Em 2 frases, explique o motivo técnico).
            
            Use emojis. Seja confiante mas lembre que é probabilidade.
            """
            
            resposta = model.generate_content(prompt)
            
            st.success("Análise Concluída!")
            
            # Caixa estilizada para o resultado
            st.markdown(f"""
            <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 1px solid #00ff00;">
                {resposta.text}
            </div>
            """, unsafe_allow_html=True)
            
            st.caption("Aviso: Apostas envolvem risco financeiro. Use com responsabilidade.")
            
        except Exception as e:
            st.error(f"Erro: {e}")