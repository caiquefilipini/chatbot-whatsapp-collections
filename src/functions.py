import streamlit as st
from streamlit_feedback import streamlit_feedback
import pyperclip

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

# Função para exibir uma nova interação
def display_interaction():
    st.session_state.interaction_count += 1


def display_chat():
    customer_message = st.text_input(label=f"Passo 1. Insira a mensagem que o cliente enviou:", key=f"customer_message_{st.session_state.interaction_count}")

    # Função que recebe a mensagem do cliente e retorna uma sugestão de resposta da IA
    def bot_response(customer_message):
        if customer_message == "a":
            resposta = "Resposta padrão (igual a a)."
        else:
            resposta = "Resposta padrão (diferente de a)."
        return resposta


    escala_notas = """
        Muito ruim: 1\n
        Ruim: 2\n
        Neutro: 3\n
        Bom: 4\n
        Muito bom: 5
    """


    # Exibe sugestões de resposta do bot e permite a avaliação
    if customer_message:
        st.session_state.customer_messages.append(customer_message) # Salva a mensagem do cliente
        bot_suggestion = bot_response(customer_message) # Sugestão de resposta do bot
        st.session_state.bot_suggestions.append(bot_suggestion) # Salva a sugestão do bot
        st.write(f"Sugestão da IA: {bot_suggestion}") # Exibe a sugestão do bot
        
        # Botão para copiar a sugestão
        if st.button('Copiar sugestão'):
            pyperclip.copy(bot_suggestion)
            st.success('Sugestão copiada!')
    

        feedback = st.radio(
            "Passo 2. Avalie a sugestão da IA:",
            ('Muito ruim', 'Ruim', 'Neutro', 'Bom', 'Muito bom'),
            help=escala_notas, # Ajuda 
            key="feedback", 
        )

        


        if st.button("Aplicar Feedback", key=f"aplicar_feedback_{st.session_state.interaction_count}"):
            st.session_state.user_ratings.append(feedback) # Salva o feedback do usuário
            user_response = st.text_input("Passo 3. Insira a mensagem que você vai enviar ao cliente:", bot_suggestion, key=f"user_response")
            st.session_state.user_responses.append(user_response) # Salva a resposta do usuário
            if st.button("Adicionar ao histórico", key=f"adicionar_historico_{st.session_state.interaction_count}"):
                display_interaction() # Exibe uma nova interação
                st.experimental_rerun()
        else:
            st.error("Por favor, avalie a sugestão da IA antes de prosseguir.")





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




##### sidebar

def exibir_historico():
    pass

def exibir_chat_encontrado():
    pass

def pesquisar_chat():
    pass



