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


### Variáveis de teste ###
# Lista de CPFs para buscar conversas
cpfs = list()
cpfs.append("12345678901")



def main():
    """
    Função principal que instancia a classe CustomerChat
    e chama o método para exibir a interface do chat.
    """
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




