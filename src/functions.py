from datetime import datetime
import streamlit as st
from streamlit_feedback import streamlit_feedback
import pyperclip
from chatbot import bot_response

# Chat

def info_cliente():
    pass


def configuracoes_iniciais_chat():
    # info_cliente()
    pass


def iniciar_novo_chat():
    # configuracoes_iniciais_chat()
    pass



# Exibir chat



# Função para exibir histórico de interações
def display_interaction():
    # Verifica se houve alguma interação
    if st.session_state.interaction_count > 0:
        # Exibição das interações
        st.write("---")
        st.write("### Histórico da Conversa")
        st.write("---")

        range_interactions = list(range(st.session_state.interaction_count - 1, -1, -1))
        # Exibir da mensagem mais recente para a mais antiga
        for p, i in enumerate(range_interactions):
            current_time = st.session_state.datetime_message[i].strftime("%H:%M:%S")
            current_date = st.session_state.datetime_message[i].strftime("%Y-%m-%d")
            st.write(f"ID: {i+1} / Data: {current_date} / Hora: {current_time}") # Colocar datas e horas corretas
            st.write(f"Mensagem do cliente: {st.session_state.customer_messages[i]}") #####
            st.write(f"Sugestão da IA: {st.session_state.bot_suggestions[i]}  (Nota {st.session_state.user_ratings[i]})") #####
            st.write(f"Resposta enviada ao cliente: {st.session_state.user_responses[i]}")
            st.write("---")

# Função para exibir o chat
def display_chat():
    # Inicialização das variáveis de sessão
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
    if "feedback_applied" not in st.session_state:
        st.session_state.feedback_applied = False
    if "datetime_message" not in st.session_state:
        st.session_state.datetime_message = []

    # Exibição do campo para o usuário inserir a mensagem do cliente
    customer_message = st.text_input(label=f"Passo 1. Insira a mensagem que o cliente enviou:", key=f"customer_message_{st.session_state.interaction_count}")

    # Escala de notas que o usuário deve utilizar para avaliar a sugestão da IA
    escala_notas = """
        1 – Resposta Crítica. Poderia causar dano na imagem do banco, gerar reclamações por parte do cliente ou ainda um processo judicial.\n
        2 - Resposta Ruim. Sem riscos de danos ao banco ou de reclamação por parte do cliente, mas não avalio como um bom atendimento.\n
        3 – Resposta Razoável. Resposta correta, porém poderia ser mais empático/educado.\n
        4 – Boa resposta. Praticamente a mesma resposta que eu daria, porém faria alguns ajustes.\n
        5 – Ótima resposta. Resposta igual ou ainda melhor do que a resposta que eu daria.\n
    """

	# 0 – Crítico. Poderia gerar dano na imagem do banco, processo judicial, ou ainda gerar reclamações por parte do cliente.
    # 1 - Ruim. Sem riscos de danos ao banco ou de reclamação por parte do cliente, mas avalio como um bom atendimento.
	# 3 – Razoável. Resposta correta, porém poderia ser mais empático/educado.
	# 4 – Boa resposta. Praticamente a mesma resposta que eu daria, porém com alguns ajustes.
	# 5 – Ótima resposta. Resposta igual ou ainda melhor do que a resposta que eu daria.

    # Exibe sugestões de resposta do bot e permite a avaliação
    if customer_message and not st.session_state.feedback_applied:
        bot_suggestion = bot_response(customer_message) # Sugestão de resposta do bot
        st.session_state.datetime_message.append(datetime.now()) # Salva a data e hora da mensagem
        st.write(f"Sugestão da IA: {bot_suggestion}") # Exibe a sugestão do bot
        
        # Botão para copiar a sugestão
        if st.button('Copiar sugestão'):
            pyperclip.copy(bot_suggestion)
            st.success('Sugestão copiada!')

        # ELemento de feedback
        feedback = st.radio(
            "Passo 2. Avalie a sugestão da IA:",
            (
                "1 – Resposta Crítica",
                "2 - Resposta Ruim",
                "3 – Resposta Razoável",
                "4 – Boa Resposta",
                "5 – Ótima Resposta",
            ),
            help=escala_notas,
            key="feedback", 
        )
        bt_aplicar_feedback = st.button("Aplicar Feedback", key=f"feedback_{st.session_state.interaction_count}")
        if bt_aplicar_feedback:
            st.session_state.customer_messages.append(customer_message) # Salva a mensagem do cliente
            st.session_state.bot_suggestions.append(bot_suggestion) # Salva a sugestão do bot
            st.session_state.user_ratings.append(feedback) # Salva o feedback do usuário
            st.session_state.feedback_applied = True
        else:
            st.error("Por favor, avalie a sugestão da IA antes de prosseguir.")

    # Se o feedback for aplicado, exibe o campo para o usuário inserir a resposta que ele vai enviar ao cliente
    if st.session_state.feedback_applied:
        user_response = st.text_input("Passo 3. Insira a mensagem que você vai enviar ao cliente:", value=st.session_state.bot_suggestions[-1], key=f"user_response")
        bt_add_historico = st.button("Adicionar ao histórico", key=f"historico_{st.session_state.interaction_count}")
        
        if bt_add_historico:
            st.session_state.user_responses.append(user_response) # Salva a resposta do usuário
            st.session_state.interaction_count += 1
            st.session_state.feedback_applied = False
            st.experimental_rerun()

####################################################################################################################################

# Formato Json

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



##### sidebar

def exibir_historico():
    pass

def exibir_chat_encontrado():
    pass

def pesquisar_chat():
    pass



