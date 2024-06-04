import streamlit as st
import openai
from langchain import LLMChain, PromptTemplate

# Configurar a chave da API da OpenAI
openai.api_key = 'YOUR_API_KEY'

# Configurar a página do Streamlit
st.set_page_config(
    page_title="ChatGPT Simulator",
    page_icon=":robot_face:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título do App
st.title("ChatGPT Simulator")

# Definir o template do prompt
template = PromptTemplate(
    template="Você é um assistente útil. Responda à pergunta: {question}",
    input_variables=["question"]
)

# Criar a cadeia LLM
chain = LLMChain(llm='openai', prompt=template)

# Caixa de texto para a entrada do usuário
user_input = st.text_input("Faça uma pergunta ao ChatGPT")

# Área de exibição da resposta
if user_input:
    st.write("### Resposta do ChatGPT:")
    # Gerar a resposta usando LangChain
    response = chain.run(question=user_input)
    st.write(response)
else:
    st.write("Digite uma pergunta e pressione Enter para receber uma resposta.")

# Rodar o aplicativo com: streamlit run chatgpt_simulator.py

# Title of the app
st.title('Gen AI Santander Recuperações')

# Função para simular uma resposta do chatbot
def generate_response(user_input):
    return f"Você disse: {user_input}. Esta é uma resposta simulada."

# Caixa de texto para entrada do usuário
user_input = st.text_input("Sua pergunta:")

# Botão para enviar a pergunta
if st.button("Enviar"):
    if user_input:
        # Gera a resposta do chatbot
        response = generate_response(user_input)
        # Exibe a resposta
        st.write(f"Resposta: {response}")
    else:
        st.write("Por favor, digite uma pergunta.")

########## SIDEBAR ##########

# Botão para iniciar um novo chat
if st.sidebar.button("Iniciar Novo Chat"):
    st.session_state['novo_chat'] = True

# Histórico de conversas na barra lateral
st.sidebar.title("Histórico de Conversas")
st.sidebar.write("Aqui você pode ver suas conversas anteriores.")

# Text input
# user_input = st.text_input('Gen AI Santander Recuperações')

# Slider
# slider_value = st.slider('Select a number:', 0, 100, 50)

# Display the user's input
# st.write('You entered:', user_input)
# st.write('Slider value:', slider_value)

# import streamlit as st
# from database import create_table, save_conversation, load_conversations

# Função para simular uma resposta do chatbot
# def generate_response(user_input):
#     return f"Você disse: {user_input}. Esta é uma resposta simulada."

# Inicializar o banco de dados e carregar conversas
# create_table()
# conversations = load_conversations()

# Inicializar o histórico de conversas e o CPF se não existirem na sessão
# if 'chat_histories' not in st.session_state:
#     st.session_state['chat_histories'] = conversations
# if 'current_cpf' not in st.session_state:
#     st.session_state['current_cpf'] = None
# if 'ratings' not in st.session_state:
#     st.session_state['ratings'] = {cpf: conv['ratings'] for cpf, conv in conversations.items()}

# Função para iniciar um novo chat
# def iniciar_novo_chat():
#     cpf = st.text_input("Digite o CPF do cliente:", key='cpf_input')
#     if cpf:
#         st.session_state['current_cpf'] = cpf
#         if cpf not in st.session_state['chat_histories']:
#             st.session_state['chat_histories'][cpf] = []
#         if cpf not in st.session_state['ratings']:
#             st.session_state['ratings'][cpf] = []
#         st.success("Novo chat iniciado.")
#         st.session_state['novo_chat'] = False

########## SIDEBAR ##########

# Botão para iniciar um novo chat
# if st.sidebar.button("Iniciar Novo Chat"):
#     st.session_state['novo_chat'] = True

# Histórico de conversas na barra lateral
# st.sidebar.title("Histórico de Conversas")
# st.sidebar.write("Aqui você pode ver suas conversas anteriores.")


# Função para iniciar um novo chat
# def iniciar_novo_chat():
#     cpf = st.text_input("Digite o CPF do cliente:")
#     if cpf:
#         st.session_state['current_cpf'] = cpf
#         if cpf not in st.session_state['chat_histories']:
#             st.session_state['chat_histories'][cpf] = []
#         if cpf not in st.session_state['ratings']:
#             st.session_state['ratings'][cpf] = []
#         st.success("Novo chat iniciado.")
#         st.session_state['novo_chat'] = False


# if st.session_state.get('novo_chat', False):
#     iniciar_novo_chat()

# Exibir histórico de CPFs na barra lateral
# for cpf in st.session_state['chat_histories']:
#     with st.sidebar.expander(f"CPF: {cpf}"):
#         for i, (user_msg, bot_msg) in enumerate(st.session_state['chat_histories'][cpf]):
#             st.write(f"Pergunta {i+1}: {user_msg}")
#             st.write(f"Resposta {i+1}: {bot_msg}")
#             if len(st.session_state['ratings'][cpf]) > i:
#                 st.write(f"Avaliação {i+1}: {st.session_state['ratings'][cpf][i]} estrelas")

# st.title("Chatbot Santander Recuperações")
# st.write("Digite sua pergunta abaixo e receba uma resposta simulada.")

# Mostrar o CPF atual se houver
# if st.session_state['current_cpf']:
#     st.write(f"CPF do Cliente: {st.session_state['current_cpf']}")

# Caixa de texto para entrada do usuário
# user_input = st.text_input("Sua pergunta:")

# Botão para enviar a pergunta
# if st.button("Enviar"):
#     if user_input:
#         if st.session_state['current_cpf']:
#             # Gera a resposta do chatbot
#             response = generate_response(user_input)
#             # Salva a pergunta e a resposta no histórico do CPF atual
#             st.session_state['chat_histories'][st.session_state['current_cpf']].append((user_input, response))
#             st.session_state['ratings'][st.session_state['current_cpf']].append(None)  # Placeholder para a avaliação
#             # Salva a conversa no banco de dados
#             save_conversation(st.session_state['current_cpf'], st.session_state['chat_histories'][st.session_state['current_cpf']], st.session_state['ratings'][st.session_state['current_cpf']])
#             # Exibe a resposta
#             st.write(f"Resposta: {response}")
#         else:
#             st.write("Por favor, inicie um novo chat inserindo o CPF.")
#     else:
#         st.write("Por favor, digite uma pergunta.")

# Exibir a conversa atual e permitir avaliações
# st.subheader("Conversa Atual")
# if st.session_state['current_cpf']:
#     for i, (user_msg, bot_msg) in enumerate(st.session_state['chat_histories'][st.session_state['current_cpf']]):
#         st.write(f"Você: {user_msg}")
#         st.write(f"Chatbot: {bot_msg}")
#         # Permitir avaliação da resposta
#         rating = st.radio(f"Avalie a resposta {i+1}:", [1, 2, 3, 4, 5], key=f'rating_{i}')
#         st.session_state['ratings'][st.session_state['current_cpf']][i] = rating

# Remova a execução direta do Streamlit



