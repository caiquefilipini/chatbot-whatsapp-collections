# import streamlit as st

# # Verifica se a chave 'button_clicked' existe no estado de sessão
# if 'button_clicked' not in st.session_state:
#     st.session_state.button_clicked = False

# # Função que será chamada ao clicar no botão
# def on_button_click():
#     st.session_state.button_clicked = True

# # Verifica o estado do botão
# if not st.session_state.button_clicked:
#     # Exibe o botão se ele não foi clicado
#     if st.button("Clique aqui", on_click=on_button_click):
#         st.experimental_rerun()

# # Exibe uma mensagem se o botão foi clicado
# if st.session_state.button_clicked:
#     st.write("O botão foi clicado e agora está oculto!")


import streamlit as st

# Inicializando a sessão do Streamlit
if 'chats' not in st.session_state:
    st.session_state['chats'] = {}

if 'current_chat' not in st.session_state:
    st.session_state['current_chat'] = None

def new_chat():
    chat_id = len(st.session_state['chats']) + 1
    st.session_state['chats'][f"Chat {chat_id}"] = []
    st.session_state['current_chat'] = f"Chat {chat_id}"
    st.experimental_rerun()  # Atualiza a página para exibir o novo chat

def select_chat(chat):
    st.session_state['current_chat'] = chat
    st.experimental_rerun()  # Atualiza a página para exibir o chat selecionado

# Sidebar para exibir os chats passados e a opção de iniciar um novo chat
st.sidebar.header("Chats")
for chat in st.session_state['chats']:
    if st.sidebar.button(chat, key=chat):
        select_chat(chat)

st.sidebar.button("Iniciar novo chat", on_click=new_chat)

# Área principal para exibir e interagir com o chat atual
if st.session_state['current_chat']:
    st.title(st.session_state['current_chat'])
    messages = st.session_state['chats'][st.session_state['current_chat']]
    
    for message in messages:
        st.write(message)

    # Campo de entrada para enviar novas mensagens
    new_message = st.text_input("Sua mensagem", key='input_message')
    if st.button("Enviar", key='send_button'):
        if new_message:
            st.session_state['chats'][st.session_state['current_chat']].append(new_message)
            st.experimental_rerun()  # Atualiza a página para exibir a nova mensagem
else:
    st.title("Inicie um novo chat ou selecione um chat existente")
