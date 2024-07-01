import os
import pandas as pd
import sqlite3
from datetime import datetime
import streamlit as st
# from streamlit_feedback import streamlit_feedback
# import pyperclip
from pycpfcnpj import cpf

from functions import display_chat, display_interaction
from save_conversations import conectar_mongo, inserir_cliente, inserir_mensagem

# from streamlit_copy_to_clipboard import st_copy_button



# app.py

import streamlit as st
from functions import CustomerChat

def main():
    """
    Função principal que instancia a classe CustomerChat
    e chama o método para exibir a interface do chat.
    """
    chat = CustomerChat()
    chat.display_chat_interface()

if __name__ == "__main__":
    # Executa a função principal
    main()



st.set_page_config(
    page_title="NegociaAI Santander",
    # page_icon="🦙",
    page_icon="./images/santander-icon.png",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None)


# Título da aplicação
st.title("NegociaAI Santander")
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

# st.sidebar.title("Histórico de Chats")
# st.sidebar.write("---")


# col1, col2, col3 = st.sidebar.columns([4, 1, 1])

# Campo de texto para buscar conversas por CPF
# texto_buscar_conversa = st.sidebar.text_input(
#         label='Buscar Conversa por CPF',
#         placeholder="CPF do cliente",
#         value=st.session_state['search_query'],
#         key=f"input_{st.session_state['reset_key']}",
#         on_change=lambda: st.session_state.update({'search_query': st.session_state[f"input_{st.session_state['reset_key']}"]})
#     )


# Faz a busca da conversa pelo CPF
# def buscar_conversa(texto_buscar_conversa):
    
#     st.session_state['messages'] = []

#     # Verifica se há texto para buscar
#     if texto_buscar_conversa != "":
    
#         # Valida se o CPF é válido
#         if not texto_buscar_conversa.isdigit():
#             st.session_state['messages'].append(
#                 {
#                     "type": "error",
#                     "content": "Ops... Esse campo só aceita números. Por favor, insira um CPF válido."
#                 }
#             )
#             # st.sidebar.error("Ops... Esse campo só aceita números. Por favor, insira um CPF válido.")
    
#         # Verifica se existe conversa com esse CPF
#         elif texto_buscar_conversa not in cpfs:
#             st.session_state['messages'].append(
#                 {
#                     "type": "error",
#                     "content": "Não encontrei nenhuma conversa com esse CPF. Por favor, insira um CPF válido."
#                 }
#             )
#             # st.sidebar.error("Não encontrei nenhuma conversa com esse CPF. Por favor, insira um CPF válido.")
    
#         # Faz a busca da conversa
#         else:
#             # Função que faz a busca da conversa...
#             st.session_state['messages'].append(
#                 {
#                     "type": "info",
#                     "content": "Conversa encontrada"
#                 }
#             )
#             # st.sidebar.write("Conversa encontrada")
#     else:
#         st.session_state['messages'] = []


# col1, col2 = st.sidebar.columns([0.5, 0.5])
# with col1:
#     botao_buscar = st.button(
#         label="Buscar",
#         key="buscar",
#         type="primary",
#     )

# with col2:
#     botao_limpar = st.button(
#     label="Limpar",
#     key="limpar",
#     type="secondary",
# )

# botao_limpar = st.sidebar.button(
#     label="Limpar",
#     key="limpar2",
#     type="secondary",
# )

if botao_buscar and texto_buscar_conversa != "":
    buscar_conversa(texto_buscar_conversa)
else: 
    st.session_state['messages'] = []

# Limpa o campo de texto e as mensagens
# if botao_limpar:
#     clear_all()
#     st.experimental_rerun()


# Exibir as mensagens armazenadas
for message in st.session_state['messages']:
    if message["type"] == "error":
        st.sidebar.error(message["content"])
    else:
        st.sidebar.write(message["content"])


# =============================================================================






# Inicialização das variáveis de sessão
# if "chat" not in st.session_state:
#     st.session_state.chat = []
# if "chat_count" not in st.session_state:
#     st.session_state.chat = []
# if "estado_botao_enviar" not in st.session_state:
#     st.session_state["estado_botao_enviar"] = 0
# if "interaction_count" not in st.session_state:
#     st.session_state.interaction_count = 0
# if "customer_messages" not in st.session_state:
#     st.session_state.customer_messages = []
# if "bot_suggestions" not in st.session_state:
#     st.session_state.bot_suggestions = []
# if "user_ratings" not in st.session_state:
#     st.session_state.user_ratings = []
# if "user_responses" not in st.session_state:
#     st.session_state.user_responses = []



# 42006925890

###########################
# Funcionalidade: Inserir CPF antes de começar o chat

# Definindo uma chave para o estado da sessão
# if 'input_visibility' not in st.session_state:
#     st.session_state.input_visibility = True

# if 'input_visibility_assunto' not in st.session_state:
#     st.session_state.input_visibility_assunto = True

# # Valida o CPF
# def valida_cpf(cpf_cliente):
#     return cpf.validate(cpf_cliente)

# # Função para esconder o input
# def inserir_cpf():
#     cpf = st.session_state.cpf_temp
#     if valida_cpf(cpf):
#         st.session_state.input_visibility = False
#         st.session_state.cpf_cliente = cpf

# if st.session_state.input_visibility:
#     # Deixando o campo do CPF menor para melhor disposição na página
#     col1, col2, col3 = st.columns([1, 1, 1])
#     with col1: campo_cpf = st.text_input("Insira o CPF do cliente:", key='cpf_temp', help="Insira um CPF válido com 11 dígitos.") #, on_change=inserir_cpf)
#     with col2: st.empty()
#     with col3: st.empty()
#     botao_inserir = st.button("Inserir", on_click=inserir_cpf, key="inserir_cpf")
#     if botao_inserir: #or campo_cpf:
#         if not campo_cpf.isdigit():
#             st.error("CPF inválido. Insira somente números.")
#         else:
#             if len(campo_cpf) != 11:
#                 st.error("O CPF precisa ter exatamente 11 dígitos. Complete com zeros à esquerda, se necessário.")
#             else:
#                 st.error("CPF inválido. Verifique e tente novamente.")

#         # st.error("O CPF precisa ter exatamente 11 dígitos. Complete com zeros à esquerda, se necessário.")

# if 'input_visibility_assunto' not in st.session_state:
#     st.session_state.input_visibility_assunto = True

# def _inserir_assunto():
#     assunto = st.session_state.assunto_temp
#     if assunto != "":
#         st.session_state.input_visibility_assunto = False
#         st.session_state.assunto = st.session_state.assunto_temp



# Exibindo o valor registrado
# if 'cpf_cliente' in st.session_state:
#     st.session_state.dt_hr_ini = datetime.now().strftime("%d/%m/%Y %H:%M")
#     st.write(f"Data e hora de início do chat: {st.session_state.dt_hr_ini}")
#     st.write("CPF do cliente:", st.session_state.cpf_cliente)
    
#     # Selecionar o assunto da conversa
#     if st.session_state.input_visibility_assunto:
#         # Exibe o campo para inserir o assunto e o botão para inserir
#         col1, col2, col3 = st.columns([1, 1, 1])
#         with col1: assunto = st.selectbox("Selecione o assunto:", ["", "Negociação", "Boleto", "Reclamação"], key='assunto_temp')
#         with col2: st.empty()
#         with col3: st.empty()
#         botao_inserir_assunto = st.button("Inserir assunto", on_click=_inserir_assunto, key="inserir_assunto")
#         if botao_inserir_assunto:
#             st.error("Insira um assunto válido.")

#     # Somente insere o assunto se o botão for clicado e o assunto for selecionado
#     if "assunto" in st.session_state:
#         st.write("Assunto:", st.session_state.assunto)
#         st.write("---")


# =============================================================================


# if 'cpf_encontrado' not in st.session_state:
#     st.session_state.cpf_encontrado = False

# # st.write(os.getcwd())
# # st.write(os.path.exists("./data/"))

# if "assunto" in st.session_state:
#     # Especificar o caminho para o diretório onde o banco de dados está localizado
#     path = "./data/" # Sempre parte da raíz do projeto
    
#     # Especificar o valor do CPF como uma string entre aspas simples
#     cpf_value = st.session_state.cpf_cliente
#     query = f"SELECT * FROM customer_database_table WHERE cpf = '{cpf_value}'"

    
#     # if 
#     # Buscar o cliente no banco de dados
#     with sqlite3.connect(os.path.join(path, 'customer_database.sqlite')) as conn:
#         # Executar a consulta SQL e ler o resultado em um DataFrame do pandas
#         consulta_cliente = pd.read_sql_query(query, conn)


#     cliente_dados = {
#         "nome": consulta_cliente["nome"][0],
#         "segmento": consulta_cliente["segmento"][0],
#         "qtd_cont": consulta_cliente["qtd_cont"][0],
#         "vlr_total_div": consulta_cliente["vlr_total_div"][0],
#         "max_dias_atraso": consulta_cliente["max_dias_atraso"][0]
#     }

#     st.subheader("Informações do cliente:")
#     st.write("- Nome:", cliente_dados["nome"])
#     st.write("- Segmento:", cliente_dados["segmento"])
#     st.write(f"- Quantidade de contratos: {cliente_dados["qtd_cont"]}")
#     st.write(f"- Valor total da dívida: {cliente_dados["vlr_total_div"]}")
#     st.write(f"- Máximo dias em atraso: {cliente_dados["max_dias_atraso"]}")
#     st.write("---")
    
#     st.session_state.cpf_encontrado = True


#     # Armazena dados da conversa no banco de dados
#     cpf = st.session_state.cpf_cliente
#     assunto = st.session_state.assunto
#     dt_hr_ini = st.session_state.dt_hr_ini

#     # st.write(cpf, assunto, dt_hr_ini, cliente_dados)
#     inserir_cliente(cpf, assunto, dt_hr_ini)#, cliente_dados)


    # =============================================================================


# Somente mostrar a função de chat se tiver algum CPF inserido.
if st.session_state.cpf_encontrado:
    display_chat() # a função de armazenar os dados da conversa vai aqui dentro
    display_interaction()



# else:
#     st.write("CPF não encontrado na base de dados. Faça o atendimento ao cliente sem o auxílio da IA")


# Salva dados da mensagem no banco de dados
# assunto = "Status do Pedido"
# dt_hr_ini = "2024-06-01 12:42"
# mensagem1 = {
#     "data_msg": "2024-06-01",
#     "hora_msg": "12h42",
#     "mensagem_cliente": "bom dia",
#     "sugestao_ia": "bom dia, sr.",
#     "resposta_final": "bom dia, sr. Carlos",
#     "rating": "4. Boa Resposta"
# }

# mensagem2 = {
#     "data_msg": "2024-06-01",
#     "hora_msg": "14h15",
#     "mensagem_cliente": "qual o status do meu pedido?",
#     "sugestao_ia": "Seu pedido está a caminho.",
#     "resposta_final": "Seu pedido está a caminho e deve chegar até o fim do dia.",
#     "rating": "5. Excelente"
# }

# # Passo 2: Appendar o primeiro bloco de mensagem
# inserir_mensagem(cpf, assunto, dt_hr_ini, mensagem1)

# # Passo 3: Appendar o segundo bloco de mensagem
# inserir_mensagem(cpf, assunto, dt_hr_ini, mensagem2)