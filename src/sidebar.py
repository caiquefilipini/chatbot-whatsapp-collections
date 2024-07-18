import streamlit as st
from conexoes import ConexaoMongo
class Sidebar:
    """Classe para gerenciar a sidebar do aplicativo.

    Attributes:
        client (MongoClient): Cliente de conexão ao MongoDB.
        db (Database): Instância do banco de dados do MongoDB.
        collection (Collection): Coleção específica dentro do banco de dados para operações.
    """
    
    def  __init__(self):
        self._inicializar_variaveis_sessao()
        self.client, self.db, self.collection = ConexaoMongo().conectar_mongo()


    def _inicializar_variaveis_sessao(self):
        """
        Inicializa as variáveis de sessão do streamlit.
        """
        if "cpf" not in st.session_state:
            st.session_state["cpf"] = ""
        if "assunto" not in st.session_state:
            st.session_state["assunto"] = ""
        if "data_hora_inicio" not in st.session_state:
            st.session_state["data_hora_inicio"] = ""
        if "carregar_historico_conversa" not in st.session_state:
            st.session_state["carregar_historico_conversa"] = False
        if "novo_chat" not in st.session_state:
            st.session_state["novo_chat"] = True
        if "inserir_cpf" not in st.session_state:
            st.session_state.inserir_cpf = True

        # Somente é necessário carregar a sidebar no início da aplicação
        if "carregar_sidebar" not in st.session_state:
            st.session_state.carregar_sidebar = True

        # if "conexao_side" not in st.session_state:
        #     st.session_state.conexao_side = True
        #     self.client, self.db, self.collection = ConexaoMongo().conectar_mongo()
        

    def _carregar_dados_conversas(self):
        """
        Carrega os dados de todas as conversas salvas no banco de dados.
        
        Returns:
        dict: Dicionário com as listas de conversas, conversas separadas e CPFs.
        """
        documentos = self.collection.find()
        lista_conversas = []
        for documento in documentos:
            cpf = documento["cpf"]
            for conversa in documento["conversas"]:
                assunto = conversa["assunto"]
                for chat in conversa["chats"]:
                    if len(chat["mensagens"]) > 0:
                        data_hora_inicio = chat["data_hora_inicio"]
                        data_inicio = data_hora_inicio.split(" - ")[0]
                        lista_conversas.append(f"{data_inicio} - {cpf} - {assunto}")

        
        # Ordena os chats por data do mais recente para o mais antigo (por nome de A a Z)
        lista_conversas.sort()
        lista_conversas_separado = [i.split(" - ") for i in lista_conversas]
        lista_cpfs = [i[1] for i in lista_conversas_separado]

        dict_conversas = {
            "lista_conversas": lista_conversas,
            "lista_conversas_separado": lista_conversas_separado,
            "lista_cpfs": lista_cpfs
        }

        # st.session_state["dict_conversas"] = dict_conversas
        lista_conversas = dict_conversas["lista_conversas"]
        # lista_conversas_separado = dict_conversas["lista_conversas_separado"]
        st.session_state["lista_chats"] = lista_conversas
        return dict_conversas
    

    def carregar_sidebar(self):
        """
        Atualiza a identificação do chat nas variáveis de sessão do streamlit com os dados do chat selecionado.
        """
        # Botão para criar novo chat (do zero)
        if st.sidebar.button("Novo Chat", key="botao_novo_chat", type="primary"):
            st.session_state["cpf"] = ""
            st.session_state["assunto"] = ""
            st.session_state["data_hora_inicio"] = ""

            st.session_state["novo_chat"] = True
            st.session_state["inserir_cpf"] = True
            st.session_state["inserir_assunto"] = True
            st.session_state["exibir_dados_cliente"] = False
            st.session_state["carregar_historico_conversa"] = False
            st.session_state["dados_conversa"] = []
            st.experimental_rerun()

        st.sidebar.write("\n")
        st.sidebar.write("\n")
        st.sidebar.write("\n")

        # Executa função para carregar todos os dados históricos do banco de dados de conversas
        if st.session_state["carregar_sidebar"]:
            dict_conversas = self._carregar_dados_conversas()
            st.session_state.carregar_sidebar = False
        
        # Título da sessão de chats históricos
        st.sidebar.write("---")
        # if st.sidebar.button("Refresh", key="botao_refresh", type="secondary"):
        #     st.experimental_rerun()
        st.sidebar.title("Histórico de Chats")

        # lista_conversas = dict_conversas["lista_conversas"]
        # lista_conversas_separado = dict_conversas["lista_conversas_separado"]

        # Salva os chats na sessão do streamlit
        # st.session_state["lista_chats"] = lista_conversas

        # Exibe os botões históricos na sidebar do streamlit

        # lista_chats = st.session_state["lista_chats"].copy()
        # reversed(lista_chats)
        for chat in reversed(st.session_state["lista_chats"]):
            lista_chat = chat.split(" - ")
            texto_botao = f"""Data de Início: {lista_chat[0].split(" ")[0]} \n CPF: {lista_chat[1]}\nAssunto: {lista_chat[2]}"""
            if st.sidebar.button(texto_botao, key=f"chat_{chat}"): #, on_click=lambda: self._atualizar_variaveis_chat(lista_chat))
                st.session_state["cpf"] = lista_chat[1]
                st.session_state["assunto"] = lista_chat[2]
                st.session_state["data_hora_inicio"] = lista_chat[0]
                
                st.session_state["novo_chat"] = False
                st.session_state["inserir_cpf"] = False
                st.session_state["inserir_assunto"] = False
                st.session_state["exibir_dados_cliente"] = True
                st.session_state["carregar_historico_conversa"] = True
                st.experimental_rerun()

        # Ao criar um novo chat, precisa appendar o chat na lista de chats

        # st.sidebar.write(f"cpf: {st.session_state["cpf"]}")
        # st.sidebar.write(f"assunto: {st.session_state["assunto"]}")
        # st.sidebar.write(f"data_hora_inicio: {st.session_state["data_hora_inicio"]}")
        # st.sidebar.write(type(st.session_state["cpf"]) == str)
        # st.sidebar.write(st.session_state["carregar_historico_conversa"])