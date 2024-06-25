import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
import torch

# Carregar o modelo e o tokenizador
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForCausalLM.from_pretrained("distilgpt2")

# Configurar o pipeline do Hugging Face
device = 0 if torch.cuda.is_available() else -1  # 0 para GPU, -1 para CPU
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)

# Definir o template do prompt com LangChain
template = PromptTemplate(
    input_variables=["question"],
    template="Você é um assistente útil. Responda à pergunta: {question}"
)

# Criar a cadeia LLM usando HuggingFacePipeline
llm_pipeline = HuggingFacePipeline(pipeline=pipe)
chain = template | llm_pipeline

# Função para gerar a resposta usando LangChain
def generate_response(user_input):
    # Gerar resposta usando o pipeline diretamente para depuração
    response = pipe(user_input, max_length=100, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    generated_text = response[0]['generated_text']
    return generated_text

# Variáveis para armazenar estado da conversa
conversation_history = []

# Função principal do chatbot
def chatbot_flow(client_message, user_rating=None, user_message=None):
    global conversation_history
    
    if client_message:
        # Etapa 2: O bot sugere uma resposta
        bot_suggestion = generate_response(client_message)
        conversation_history.append({'Client': client_message, 'Bot Suggestion': bot_suggestion})
        return bot_suggestion, gr.update(visible=True), gr.update(visible(True)), gr.update(visible(False))
    
    if user_rating is not None and user_message:
        # Registrar a avaliação e a mensagem do usuário
        conversation_history[-1]['User Rating'] = user_rating
        conversation_history[-1]['User Message'] = user_message
        
        # Abrir o campo para a próxima mensagem do cliente
        return "", gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)
    
    return "", gr.update(visible=False), gr.update(visible(False)), gr.update(visible(False))

# Interface do Gradio
with gr.Blocks() as demo:
    gr.Markdown("## ChatGPT Simulator")
    
    with gr.Row():
        client_input = gr.Textbox(label="Mensagem do Cliente", interactive=True)
    
    bot_suggestion_output = gr.Textbox(label="Sugestão do Bot", interactive=False, visible=False)
    rating = gr.Slider(1, 5, step=1, label="Avalie a Sugestão", interactive=True, visible=False)
    user_message_input = gr.Textbox(label="Sua Mensagem ao Cliente", interactive=True, visible=False)
    
    with gr.Row():
        client_submit = gr.Button("Enviar Mensagem do Cliente")
        rating_submit = gr.Button("Avaliar e Enviar Resposta", visible=False)
    
    client_submit.click(fn=chatbot_flow, inputs=[client_input], outputs=[bot_suggestion_output, rating, user_message_input, client_input])
    rating_submit.click(fn=chatbot_flow, inputs=[rating, user_message_input], outputs=[bot_suggestion_output, rating, user_message_input, client_input])

if __name__ == "__main__":
    demo.launch()


####################################################################################################


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

####################################################################################################


import streamlit as st

# Persistent storage for conversation history
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Function to handle the chat process
def handle_chat():
    user_message = st.text_input("Please enter your message:", key="user_input")
    if user_message:
        # Simple constant response for demonstration
        bot_response = "Hello! I'm your friendly bot."
        st.session_state['history'].append({"user": user_message, "bot": bot_response})

        # Display bot response
        st.write(f"Bot: {bot_response}")

        # Rating input
        rating = st.slider("Please rate the response from 1 to 5:", 1, 5, key="rating")
        st.session_state['history'].append({"rating": rating})

# Display chat history
def display_history():
    for chat in st.session_state['history']:
        if 'user' in chat:
            st.text_area("User said:", value=chat['user'], height=50, disabled=True)
            st.text_area("Bot replied:", value=chat['bot'], height=50, disabled=True)
        if 'rating' in chat:
            st.write(f"Rating given: {chat['rating']}")

# Layout
st.title("Chatbot Interaction")
handle_chat()
display_history()


####################################################################################################




