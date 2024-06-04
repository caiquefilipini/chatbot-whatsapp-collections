import streamlit as st
from streamlit_feedback import streamlit_feedback

st.set_page_config(
    page_title="IA Santander Recuperações",
    # page_icon="🦙",
    page_icon="../images/santander-icon.png",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None)


# Título da aplicação
st.title("IA Santander Recuperações")




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



# Inicialização do chat
# if "messages" not in st.session_state.keys(): # Initialize the chat messages history
#     st.session_state.messages = [
#         {"role": "assistant", "content": "Ask me a question about Streamlit's open-source Python library!"}
#     ]



# feedback = streamlit_feedback(
#     feedback_type="faces",  # Apply the selected feedback style
    
#     optional_text_label="[Optional] Please provide an explanation",
#     key="feedback",

# )
# feedback

# if prompt := st.chat_input("Insira aqui a mensagem do cliente"): # Prompt for user input and save to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})


# if 'botao_enviar' not in st.session_state:
#     st.session_state['botao_enviar'] = 1
# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []
# if 'reset_key' not in st.session_state:
#     st.session_state['reset_key'] = 0



# Função para exibir uma nova interação
def display_interaction():
    st.session_state.interaction_count += 1
    # st.write(f"--- Interacção {st.session_state.interaction_count} ---")


# Função para exibir uma nova interação
def display_feedback_interaction():
    st.session_state.interaction_count_feedback += 1
    st.write(f"--- Interacção {st.session_state.interaction_count_feedback} ---")

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

# Entrada da mensagem do cliente
# st.write(f"Passo 1. Insira a mensagem que o cliente enviou:")
# texto = st.write(f"Passo 1. Insira a mensagem que o cliente enviou:")

# Colocar na mesma formatação de st.write
# customer_message = st.text_input(label=f"Passo 1. Insira a mensagem que o cliente enviou:", key=f"customer_message_{st.session_state.interaction_count}")
# botao_enviar = st.button("Enviar", key=f"botao_enviar_{st.session_state.interaction_count}")

customer_message = st.text_input(label=f"Passo 1. Insira a mensagem que o cliente enviou:", key=f"customer_message_{st.session_state.interaction_count}")
# botao_enviar = st.button("Enviar", key=f"botao_enviar_{st.session_state.interaction_count}")




# Função que recebe a mensagem do cliente e retorna uma sugestão de resposta da IA
def bot_response(customer_message):
    if customer_message == "a":
        resposta = "Resposta padrão (igual a a)."
    else:
        resposta = "Resposta padrão (diferente de a)."
    return resposta





# if "interaction_count_feedback" not in st.session_state:
#     st.session_state.interaction_count_feedback = 0


# if 'feedback_corrected' not in st.session_state:
#     st.session_state.feedback_corrected = False

# if customer_message and botao_enviar:
#     st.session_state["estado_botao_enviar"] = 1
#     st.session_state["customer_messages"].append(customer_message)

# condicional_mensagem_cliente = customer_message and st.session_state["estado_botao_enviar"] > 0
# st.write(f"{verificar}")


# Exibe sugestões de resposta do bot e permite a avaliação
if customer_message:
    st.session_state.customer_messages.append(customer_message) # Salva a mensagem do cliente
    bot_suggestion = bot_response(customer_message) # Sugestão de resposta do bot
    st.session_state.bot_suggestions.append(bot_suggestion) # Salva a sugestão do bot
    st.write(f"Sugestão da IA: {bot_suggestion}") # Exibe a sugestão do bot

# Criar botão copiar


    # Avaliação da sugestão do bot
    # st.write(f"Passo 2. Avalie a sugestão da IA:")

    # Define componentes de feedback para o usuário avaliar a sugestão do bot
    # feedback = streamlit_feedback(
    #     feedback_type="faces",  # Aplica o estilo de feedback selecionado
    #     optional_text_label="[Opcional] Explique o motivo da sua nota",
    #     key=f"feedback+{st.session_state.interaction_count}",
    #     align="flex-start"
    # )


    feedback = st.radio(
        "Passo 2. Avalie a sugestão da IA:",
        ('Muito ruim', 'Ruim', 'Neutro', 'Bom', 'Muito bom'),
        key="feedback", 
    )

    if feedback:
        st.session_state.user_ratings.append(feedback) # Salva o feedback do usuário
        user_response = st.text_input("Passo 3. Insira a mensagem que você vai enviar ao cliente:", bot_suggestion, key=f"user_response")
        st.session_state.user_responses.append(user_response) # Salva a resposta do usuário

    #     if st.button("Corrigir Feedback", key=f"corrigir_feedback_{st.session_state.interaction_count}"):
    #         st.session_state.user_ratings.pop() # Remove a nota a ser corrigida
    #         display_feedback_interaction() # Exibe uma nova interação de feedback
        

    else:
        st.error("Por favor, avalie a sugestão da IA antes de prosseguir.")


    if st.button("Adicionar ao histórico", key=f"adicionar_historico_{st.session_state.interaction_count}"):
        # st.session_state["estado_botao_enviar"] = 0 # Reseta o estado do botão de enviar
        display_interaction() # Exibe uma nova interação
        st.experimental_rerun()
        # if st.button("Adicionar nova mensagem do cliente", key=f"adicionar_nova_mensagem_{st.session_state.interaction_count}"):
        #     display_interaction() # Exibe uma nova interação

    # st.session_state["estado_botao_enviar"] = 0

    # if feedback:
    #     st.session_state.user_ratings.append(feedback)
    #     st.session_state.feedback_corrected = False
    #     user_response = st.text_input("Passo 3. Insira a mensagem que você vai enviar ao cliente:", bot_suggestion, key=f"user_response_{st.session_state.interaction_count}")
    #     st.session_state.user_responses.append(user_response)
    #     botao_corrigir_feedback = st.button("Corrigir Feedback", key=f"corrigir_feedback_{st.session_state.interaction_count}")
    #     if botao_corrigir_feedback:
    #         if st.session_state.user_ratings:
    #             st.session_state.user_ratings.pop()
    #         st.session_state.feedback_corrected = True
    #         st.experimental_rerun()  # Reinicializa a execução do app para recolher novo feedback



# interaction_count_feedback


        # if st.button("Adicionar nova mensagem do cliente"):
        #     display_interaction()



    # Entrada da resposta final do usuário
    # user_response = st.text_input("Passo 3. Insira a mensagem que você vai enviar ao cliente:", bot_suggestion, key=f"user_response_{st.session_state.interaction_count}")
    # st.session_state.user_responses.append(user_response)

    # Botão para adicionar nova interação
    # if st.button("Adicionar nova mensagem do cliente"):
    #     display_interaction()
    # ----------- #

    # Avaliação da sugestão do bot
    
    # st.write(f"Passo 2. Avalie a sugestão da IA:")
    # # Define componentes de feedback para o usuário avaliar a sugestão do bot
    # feedback = streamlit_feedback(
    #     feedback_type="faces",
    #     optional_text_label="[Opcional] Explique o motivo da sua nota",
    #     key="feedback",
    #     align="flex-start"
    # )

    # Cria um estado para verificar se o usuário deseja corrigir o feedback
    # if 'deseja_corrigir_feedback' not in st.session_state:
    #     st.session_state.deseja_corrigir_feedback = True

    # Enquanto o usuário não corrigir o feedback, o botão de corrigir feedback é exibido
    # Não sai do loop enquanto o usuário desejar corrigir o feedback


    # if feedback:
    #     # Salva o feedback do usuário
    #     st.session_state.user_ratings.append(feedback)
        
    #     # Entrada da resposta final do usuário
    #     user_response = st.text_input("Passo 3. Insira a mensagem que você vai enviar ao cliente:", bot_suggestion, key=f"user_response_{st.session_state.interaction_count}")
    #     st.session_state.user_responses.append(user_response)

    #     # Botão para adicionar nova interação
    #     if st.button("Adicionar nova mensagem do cliente"):
    #         display_interaction()
    
    # else:
    #     st.error("Por favor, avalie a sugestão da IA antes de prosseguir.")
    
    # while st.session_state.deseja_corrigir_feedback:

    #     st.write(f"Passo 2. Avalie a sugestão da IA:")
    #     # Define componentes de feedback para o usuário avaliar a sugestão do bot
    #     feedback = streamlit_feedback(
    #         feedback_type="faces",
    #         optional_text_label="[Opcional] Explique o motivo da sua nota",
    #         # key="feedback",
    #         align="flex-start"
    #     )

    #     if feedback:
    #         # Salva o feedback do usuário
    #         st.session_state.user_ratings.append(feedback)
            
    #         # Entrada da resposta final do usuário
    #         user_response = st.text_input("Passo 3. Insira a mensagem que você vai enviar ao cliente:", bot_suggestion, key=f"user_response_{st.session_state.interaction_count}")
    #         st.session_state.user_responses.append(user_response)
    #     else:
    #         st.error("Por favor, avalie a sugestão da IA antes de prosseguir.")
        
    #     if st.button("Corrigir Feedback"):
    #         st.session_state.user_ratings.pop()
    #         st.session_state.deseja_corrigir_feedback = True
    #         st.experimental_rerun()
        
    #     else: deseja_corrigir_feedback = False

    # Botão para adicionar nova interação
    # if st.button("Adicionar nova mensagem do cliente"):
    #     display_interaction()
    
    





# st.chat_message("Hello, I'm a chatbot. How can I help you today?")
# st.chat_input()

# id = 'x'

# dados = {
#     "dados_cliente":
#         {
#             "cpf": "12345678901",
#             "nome": "João"
#         },

#     "dados_conversa":
#         {
#             "id": id,


#             "id_1":
#                 {
#                     "data": "2024-06-01",
#                     "hora": "12h42",
#                 },
#             "id_2":
#                 {
#                     "data": "2024-06-01",
#                     "hora": "12h42",
#                 },
#         }
    
    
    
#     }
 
 
#  }


# {"id": id 
#     data = 
#     hora = 
#     mensagem_cliente = 
#     sugestao_ia = 
    # resposta_usuario =


if st.session_state.interaction_count > 0:
    # Exibição das interações
    st.write("---")
    st.write("### Histórico da Conversa")
    st.write("---")

    # Exibir da mensagem mais recente para a mais antiga
    for i in range(st.session_state.interaction_count, -1, -1):
        st.write(f"ID: {i+1} / Data: {"2024-06-01"} / Hora: {"12h42"}") # Colocar datas e horas corretas
        st.write(f"Mensagem do cliente: {st.session_state.customer_messages[i]}")
        st.write(f"Sugestão da IA: {st.session_state.bot_suggestions[i]}  (Nota {st.session_state.user_ratings[i]})")
        st.write(f"Resposta enviada ao cliente: {st.session_state.user_responses[i]}")
        st.write("---")

# digitalk
# bom ...
# 