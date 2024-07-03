import streamlit as st
from conexoes import ConexaoMongo


##### SIDEBAR #####


# Ideia: não ter opção de aplicar filtro (operador pode pesquisar com Ctrl+F, pois os chats sempre serão exibidos em ordem cronológica e com CPF)
# GPT não tem opção de pesquisar
# Data - CPF - Assunto



class Sidebar:
    """ Classe para gerenciar a barra lateral do chat.

    Attributes:
        client (MongoClient): Cliente de conexão ao MongoDB.
        db (Database): Instância do banco de dados do MongoDB.
        collection (Collection): Coleção específica dentro do banco de dados para operações.
    """
    
    def  __init__(self):
        self.client, self.db, self.collection = ConexaoMongo.conectar_mongo()


    # def _aplicar_filtro(self, cpf_filtro, lista_cpfs):
    #     """
    #     Verifica a validade do filtro e, caso seja válido, retorna as posicoes para aplicação do filtro.
    #     Função desabilitada para esta versão.
    #     Args:
    #     cpf_filtro (str): CPF a ser filtrado.
    #     lista_cpfs (list): Lista de todos os CPFs com conversas salvas.
    #     Returns:
    #     list: As posições do CPF filtrado na lista de CPFs.
    #     """
    #     posicoes_lista = []
    #     # Valida se o CPF é numérico
    #     if not cpf_filtro.isdigit():
    #         st.session_state["mensagens_filtro"].append(
    #             {
    #                 "type": "error",
    #                 "content": "Ops... Esse campo só aceita números. Por favor, insira um CPF válido."
    #             }
    #         )
    #     # Valida se existe conversa com o CPF informado
    #     elif cpf_filtro not in lista_cpfs:
    #         st.session_state["mensagens_filtro"].append(
    #             {
    #                 "type": "error",
    #                 "content": "Não encontrei nenhuma conversa com esse CPF. Por favor, insira um CPF válido."
    #             }
    #         )
    #     # Busca as posições do CPF na lista de CPFs
    #     else:
    #         posicoes_lista = [i for i, x in enumerate(lista_cpfs) if x == cpf_filtro]
    #         self.st.session_state["filtro"] = 1
    #         st.session_state["mensagens_filtro"].append(
    #             {
    #                 "type": "info",
    #                 "content": f"Exibindo conversas do CPF: {cpf_filtro}"
    #             }
    #         )
    #     st.experimental_rerun()
    #     return posicoes_lista


    # def _limpar_filtro(self):
    #     """
    #     Limpa o filtro aplicado e as mensagens de erro.
    #     Função desabilitada para esta versão.
    #     """
    #     st.session_state["cpf_filtro"] = ""
    #     st.session_state["mensagens_filtro"] = []
    #     self.st.session_state["filtro"] == 0
    #     st.experimental_rerun()


    def _atualizar_variaveis_chat(self, lista_chat):
        """
        Atualiza a identificação do chat nas variáveis de sessão do streamlit com os dados do chat selecionado.
        """
        st.session_state["cpf"] = lista_chat[1]
        st.session_state["assunto"] = lista_chat[2]
        st.session_state["data_hora_inicio"] = lista_chat[0]
        st.experimental_rerun()


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
                    data_hora_inicio = chat["data_hora_inicio"]
                    data_inicio = data_hora_inicio.split(" - ")[0]
                    # data_hora_ultima_mensagem = max(mensagem["data_hora_mensagem"] for mensagem in chat["mensagens"])
                    # lista_conversas.append(f"{data_hora_ultima_mensagem}/{data_inicio} - {cpf} - {assunto}")
                    lista_conversas.append(f"{data_inicio} - {cpf} - {assunto}")
        
        # Ordena os chats por data do mais recente para o mais antigo (por nome de A a Z)
        lista_conversas.sort() # Ordena por data e hora de início
        # lista_conversas_separado = [i.split("/")[-1].split(" - ")[0] for i in lista_conversas] # Sem a data da última mensagem
        lista_conversas_separado = [i.split(" - ")[0] for i in lista_conversas]
        lista_cpfs = [i[1] for i in lista_conversas_separado] # Somente os CPFs

        dict_conversas = {
            "lista_conversas": lista_conversas,
            "lista_conversas_separado": lista_conversas_separado,
            "lista_cpfs": lista_cpfs
        }
        return dict_conversas


    def _criar_novo_chat(self):
        """
        Atualiza a identificação do chat nas variáveis de sessão do streamlit com os dados do chat selecionado.
        """
        st.session_state["cpf"] = ""
        st.session_state["assunto"] = ""
        st.session_state["data_hora_inicio"] = ""
        # self._limpar_filtro()


    def carregar_sidebar(self):
        """
        Atualiza a identificação do chat nas variáveis de sessão do streamlit com os dados do chat selecionado.
        """
        # Botão para criar novo chat (do zero)
        st.button("Novo Chat", on_click=self._criar_novo_chat())
        st.sidebar.write("\n")
        st.sidebar.write("\n")
        st.sidebar.write("\n")

        # Executa função para carregar todos os dados históricos do banco de dados de conversas
        dict_conversas = self._carregar_dados_conversas()
        
        # Título da sessão de chats históricos
        st.sidebar.write("---")
        st.sidebar.title("Histórico de Chats")
        st.write("Os chats estão nomeados no formato 'Data de Início - CPF - Assunto' e são exibidos em ordem de Data de Início, do mais recente para o mais antigo")
        
        # Campo para inserir o CPF a ser filtrado
        # cpf_filtro = st.sidebar.text_input(
        #         label="Buscar Conversa por CPF",
        #         placeholder="CPF do cliente",
        #         value=st.session_state["cpf_filtro"]
        # )
        
        # Botão para executar a busca
        # col1, col2 = st.sidebar.columns([0.5, 0.5])
        # with col1:
        #     botao_buscar = st.button(
        #         label="Aplicar Filtro",
        #         key="buscar",
        #         type="primary",
        #         # on_click=self._aplicar_filtro(cpf_filtro, dict_conversas["lista_cpfs"])
        #     )
        
        # Se o botão de busca foi clicado e o campo de CPF não está vazio, aplica o filtro
        # if botao_buscar and cpf_filtro != "":
        #     posicoes_lista = self._aplicar_filtro(cpf_filtro, dict_conversas["lista_cpfs"])

        #     # Habilita o botão para limpar o filtro
        #     if self.st.session_state["filtro"] == 1:
        #         botao_limpar = st.sidebar.button(
        #             label="Limpar Filtro",
        #             key="limpar",
        #             type="secondary",
        #             on_click=self._limpar_filtro()
        #         )
        # else:
        #     posicoes_lista = []

        # Se filtro aplicado, define as posições do CPF selecionado, senão define as 10 primeiras posições de todos os chats
        # qtd_exibir_sem_filtro = 10
        # if len(posicoes_lista) > 0:
        #     lista_conversas_final = dict_conversas["lista_conversas"][posicoes_lista]
        #     lista_conversas_separado_final = dict_conversas["lista_conversas_separado"][posicoes_lista]
        # else:
            # lista_conversas_final = dict_conversas["lista_conversas"][:qtd_exibir_sem_filtro]
            # lista_conversas_separado_final = dict_conversas["lista_conversas_separado"][:qtd_exibir_sem_filtro]

        lista_conversas = dict_conversas["lista_conversas"]
        lista_conversas_separado = dict_conversas["lista_conversas_separado"]

        # Salva os chats na sessão do streamlit
        st.session_state["lista_chats"] = lista_conversas_separado

        # Exibe os botões históricos na sidebar do streamlit
        for chat in st.session_state["lista_chats"]:
            lista_chat = chat.split(" - ")
            st.sidebar.button(chat, key=f"chat_{chat}", on_click=self._atualizar_variaveis_chat(lista_chat))