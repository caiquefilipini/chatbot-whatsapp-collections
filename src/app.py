

# Libs corretas
from sidebar import Sidebar




import os
import streamlit as st

from functions import display_chat, display_interaction
from save_conversations import conectar_mongo, inserir_cliente, inserir_mensagem

# app.py
# Testar sidebar e chat separados primeiro e depois juntos
# Toy app não vai ter sidebar e também não vai salvar conversas no banco de dados
# Toy app não vai carregar dados do cliente



import streamlit as st
from functions import CustomerChat


### Variáveis de teste ###
st.session_state["cpf"] = "12345678901"
st.session_state["assunto"] = "Reclamação"


# Lista de CPFs para buscar conversas
cpfs = list()
cpfs.append("12345678901")



def main():
    """
    Função principal que instancia a classe CustomerChat
    e chama o método para exibir a interface do chat.
    """

    sidebar = Sidebar.carregar_sidebar()
    


    chat = CustomerChat()
    chat.display_chat_interface()




if __name__ == "__main__":
    main()


# Configuração da página
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




