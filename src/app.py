import streamlit as st
from sidebar import Sidebar
from chat import Chat

# 72388905850

# Testes dando errado
# Adicionar mensagem novo chat (não adiciona)
# Adicionar mensagem chat existente (não adiciona e limpa o histórico)
# Sidebar ordenando errado

### Variáveis de teste ###
# st.session_state["cpf"] = "12345678901"
# st.session_state["assunto"] = "Reclamação"
# st.session_state["dt_hr_ini"] = "2023-03-12"


def configurar_pagina():
    st.set_page_config(
        page_title="NegociaAI Santander",
        page_icon="./images/santander-icon.png",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None)
    st.title("NegociaAI Santander")
    st.write("---")


def main():
    """
    Função principal que instancia a classe CustomerChat
    e chama o método para exibir a interface do chat.
    """
    sidebar = Sidebar()
    chat = Chat()
    configurar_pagina()
    sidebar.carregar_sidebar()
    chat.exibir_informacoes_iniciais_chat()
    chat.exibir_informacoes_cliente()
    chat.exibir_elemento_chat()
    chat.exibir_historico_conversa()


if __name__ == "__main__":
    main()