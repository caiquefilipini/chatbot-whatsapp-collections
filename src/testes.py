import streamlit as st

# Verifica se a chave 'button_clicked' existe no estado de sessão
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

# Função que será chamada ao clicar no botão
def on_button_click():
    st.session_state.button_clicked = True

# Verifica o estado do botão
if not st.session_state.button_clicked:
    # Exibe o botão se ele não foi clicado
    if st.button("Clique aqui", on_click=on_button_click):
        st.experimental_rerun()

# Exibe uma mensagem se o botão foi clicado
if st.session_state.button_clicked:
    st.write("O botão foi clicado e agora está oculto!")
