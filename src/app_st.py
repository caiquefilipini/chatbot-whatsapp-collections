import streamlit as st
from streamlit_feedback import streamlit_feedback
import pyperclip
from pycpfcnpj import cpf

from functions import display_chat


# from streamlit_copy_to_clipboard import st_copy_button

st.set_page_config(
    page_title="IA Santander Recuperações",
    # page_icon="🦙",
    page_icon="../images/santander-icon.png",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None)


# Título da aplicação
st.title("IA Santander Recuperações")
st.write("---")

# st.header('Cabeçalho')
# st.subheader('Subcabeçalho')
# st.write('Texto simples')

# Inicializando o estado se não estiver presente


# States
# Histórico dos chats, Histórico das conversas, CPFs


# Funcionalidades:
# Interação chat
# Novo chat
# Buscar chats por CPF
# Salvar dados em database
# Ler dados do cliente


# Possíveis melhorias:
# Excluir chat?
# Corrigir feedbacks
# Operador pode ter acesso a histórico? Se não, porque?
# Mostrar resumo?


if 'search_query' not in st.session_state:
    st.session_state['search_query'] = ""
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'reset_key' not in st.session_state:
    st.session_state['reset_key'] = 0

def clear_all():
    st.session_state['search_query'] = ""
    st.session_state['messages'] = []
    st.session_state['reset_key'] += 1

# Lista de CPFs para buscar conversas
cpfs = list()
cpfs.append("12345678901")

if st.sidebar.button("Novo Chat"):
    # Função para criar um novo chat
    pass

st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("---")

st.sidebar.title("Histórico de Chats")
# st.sidebar.write("---")


# Campo de texto para buscar conversas por CPF
texto_buscar_conversa = st.sidebar.text_input(
    label='Buscar Conversa por CPF',
    placeholder="CPF do cliente",
    value=st.session_state['search_query'],
    key=f"input_{st.session_state['reset_key']}",
    on_change=lambda: st.session_state.update({'search_query': st.session_state[f"input_{st.session_state['reset_key']}"]})
)

# Faz a busca da conversa pelo CPF
def buscar_conversa(texto_buscar_conversa):
    
    st.session_state['messages'] = []

    # Verifica se há texto para buscar
    if texto_buscar_conversa != "":
    
        # Valida se o CPF é válido
        if not texto_buscar_conversa.isdigit():
            st.session_state['messages'].append(
                {
                    "type": "error",
                    "content": "Ops... Esse campo só aceita números. Por favor, insira um CPF válido."
                }
            )
            # st.sidebar.error("Ops... Esse campo só aceita números. Por favor, insira um CPF válido.")
    
        # Verifica se existe conversa com esse CPF
        elif texto_buscar_conversa not in cpfs:
            st.session_state['messages'].append(
                {
                    "type": "error",
                    "content": "Não encontrei nenhuma conversa com esse CPF. Por favor, insira um CPF válido."
                }
            )
            # st.sidebar.error("Não encontrei nenhuma conversa com esse CPF. Por favor, insira um CPF válido.")
    
        # Faz a busca da conversa
        else:
            # Função que faz a busca da conversa...
            st.session_state['messages'].append(
                {
                    "type": "info",
                    "content": "Conversa encontrada"
                }
            )
            # st.sidebar.write("Conversa encontrada")
    else:
        st.session_state['messages'] = []


col1, col2 = st.sidebar.columns([0.5, 0.5])
with col1:
    botao_buscar = st.button(
        label="Buscar",
        key="buscar",
    )

with col2:
    botao_limpar = st.button(
    label="Limpar",
    key="limpar",
)

if botao_buscar and texto_buscar_conversa != "":
    buscar_conversa(texto_buscar_conversa)
else: 
    st.session_state['messages'] = []

# Limpa o campo de texto e as mensagens
if botao_limpar:
    clear_all()
    st.experimental_rerun()


# Exibir as mensagens armazenadas
for message in st.session_state['messages']:
    if message["type"] == "error":
        st.sidebar.error(message["content"])
    else:
        st.sidebar.write(message["content"])


# =============================================================================






# Inicialização das variáveis de sessão
if "chat" not in st.session_state:
    st.session_state.chat = []
if "chat_count" not in st.session_state:
    st.session_state.chat = []
if "estado_botao_enviar" not in st.session_state:
    st.session_state["estado_botao_enviar"] = 0
if "interaction_count" not in st.session_state:
    st.session_state.interaction_count = 0
if "customer_messages" not in st.session_state:
    st.session_state.customer_messages = []
if "bot_suggestions" not in st.session_state:
    st.session_state.bot_suggestions = []
if "user_ratings" not in st.session_state:
    st.session_state.user_ratings = []
if "user_responses" not in st.session_state:
    st.session_state.user_responses = []





###########################
# Funcionalidade: Inserir CPF antes de começar o chat

# Definindo uma chave para o estado da sessão
if 'input_visibility' not in st.session_state:
    st.session_state.input_visibility = True


if 'input_visibility_assunto' not in st.session_state:
    st.session_state.input_visibility_assunto = True

# Valida o CPF
def valida_cpf(cpf_cliente):
    return cpf.validate(cpf_cliente)


# st.session_state.assunto_temp = "" 

# Função para esconder o input
def inserir_cpf():
    cpf = st.session_state.cpf_temp
    if valida_cpf(cpf):
        st.session_state.input_visibility = False
        st.session_state.cpf_cliente = cpf

# 42006925890

if st.session_state.input_visibility:
    # Deixando o campo do CPF menor para melhor disposição na página
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1: campo_cpf = st.text_input("Insira o CPF do cliente:", key='cpf_temp', on_change=inserir_cpf)
    with col2: st.empty()
    with col3: st.empty()
    botao_inserir = st.button("Inserir", on_click=inserir_cpf())
    if botao_inserir or campo_cpf:
        st.error("CPF inválido. Tente novamente.")
        
        # st.error("Insira um assunto.")


def inserir_assunto():
    st.session_state.input_visibility_assunto = False
    st.session_state.assunto = st.session_state.assunto_temp


# Exibindo o valor registrado
if 'cpf_cliente' in st.session_state:
    if st.session_state.input_visibility_assunto:
        cpf_inserido = st.write("CPF do cliente:", st.session_state.cpf_cliente, key='cpf_cliente')
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1: assunto = st.selectbox("Selecione o assunto:", ["", "Negociação", "Boleto", "Reclamação"], key='assunto_temp')
        with col2: st.empty()
        with col3: st.empty()
        botao_inserir_assunto = st.button("Inserir assunto", on_click=inserir_assunto(), key='inserir_assunto')


    cpf_inserido = st.write("CPF do cliente:", st.session_state.cpf_cliente, key='cpf_cliente')
    assunto_inserido = st.write("Assunto:", st.session_state.assunto, key='assunto_cliente')
    st.write("---")
    # Carregar informações relevantes sobre o cliente

    # if cpf_encontrado:
    #     st.write("Cliente encontrado.") # Busca no banco de dados
    # else:
    #     st.write("Cliente não encontrado.") # Abre campos para inserir informações do cliente manualmente

    # Somente mostrar a função de chat se tiver algum CPF inserido.
    
    st.write("Informações sobre o cliente:")
    st.write("- Valor da dívida:")
    st.write("- Dias em atraso:")
    st.write("---")
    
    display_chat()


############################
# Funcionalidade: Somente mostrar a função de chat se tiver algum CPF inserido.

