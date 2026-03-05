import json
import pandas as pd
import requests
import streamlit as st

# ============ CONFIGURAÇÃO =
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

# ============ CARREGAR DADOS ============
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

# ============ MONTAR CONTEXTO
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade' ]} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Vocé é o Mentor Financeiro, um educador financeiro amigável e didático..

OBJETIVO:
Ensinar conceitos de financas pessoais, planejamento financeiro e como economizar de forma simples, usando os dados do ciiente como exemplos práticos.

REGRAS:
1. Use os dados fornecidos para dar exemplos personalizados
2. Linguagem simples, como se explicasse para um amigo
3. Se nao souber algo, admita: "Nao tenho essa informacão, mas posso explicar ... "
4. Sempre pergunte se o cliente entendeu
5. Seja objetivo e paciente na explicação
6. Não julge os gastos do usuário, foque em educar e orientar
7. Use analogias e exemplos do dia a dia para facilitar o entendimento
8. Incentive o cliente a fazer perguntas e interagir para garantir que ele esteja acompanhando a explicação
9. Foque em ensinar conceitos, não apenas dar respostas diretas
10. Se o cliente tiver dúvidas sobre um produto financeiro, explique os prós e contras de forma clara e imparcial
11. Sempre termine a conversa com uma dica prática que o cliente possa aplicar imediatamente
12. Lembre-se de que o objetivo é educar, não vender produtos financeiros
13. Mantenha a conversa leve e motivadora, incentivando o cliente a melhorar sua saúde financeira de forma gradual e sustentável
14. Use os dados do cliente para mostrar como pequenas mudanças podem ter um grande impacto no longo prazo, como o efeito dos juros compostos ou a importância de uma reserva de emergência
"""

# ============ CHAMAR OLLAMA ==
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}
    
    Pergunta: {msg}"""
    
    r = requests. post(OLLAMA_URL, json={
        "model": MODELO, 
        "prompt": prompt, 
        "stream": False
    })

    print(r.status_code)
    print(r.text)

    return r.json()

# ============ INTERFACE ==============

st.title(" 👨🏻‍💻 Oi, Eu Sou o seu Mentor Financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças ... "):
   st.chat_message("user").write(pergunta)
   with st.spinner(" ... "):
        st.chat_message("assistant").write(perguntar(pergunta))
