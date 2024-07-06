# Libs
import pandas as pd
import os

from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import streamlit as st
from conexoes import ConexaoMongo
from chatbot import bot_response
from save_data import SaveData

import pyperclip
from pycpfcnpj import cpf

# import sqlite3

class Chat:
    """ Classe para gerenciar a sidebar do aplicativo.

    Attributes:
        client (MongoClient): Cliente de conexão ao MongoDB.
        db (Database): Instância do banco de dados do MongoDB.
        collection (Collection): Coleção específica dentro do banco de dados para operações.
    """

    def __init__(self):
        if "aplicar_feedback" not in st.session_state:
            st.session_state.aplicar_feedback = False
        self.client, self.db, self.collection = ConexaoMongo().conectar_mongo()

    ### INFO INICIAIS ###

    def _inserir_assunto(self):
        """
        Insere o assunto no estado da sessão se não for vazio e esconde o campo de input.
        """
        assunto = st.session_state.assunto_selecionado
        if assunto != "":
            st.session_state.inserir_assunto = False
            st.session_state.assunto = st.session_state.assunto_selecionado

    def _validar_cpf(self):
        """
        Insere o CPF no estado da sessão se for válido e esconde o campo de input.
        """
        cpf_inserido = st.session_state.cpf_temp
        st.session_state['messages'] = []

        if cpf_inserido == "":
            st.session_state.messages = ["Insira um CPF válido."] 
        elif not cpf_inserido.isdigit():
            st.session_state.messages = ["CPF inválido. Insira somente números."]
        elif len(cpf_inserido) != 11:
            st.session_state.messages = ["O CPF precisa ter exatamente 11 dígitos. Complete com zeros à esquerda, se necessário."]
        elif not cpf.validate(st.session_state.cpf_temp): 
            st.session_state.messages["CPF inválido. Verifique e tente novamente."]
        else:
            st.session_state.cpf = cpf_inserido


    def exibir_informacoes_iniciais_chat(self):
        """
        Exibe as informações iniciais do chat (Data e hora de início, CPF e Assunto).
        """
        # Campo para inserir o CPF do cliente
        if st.session_state.cpf == "":
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                campo_cpf = st.text_input(
                    "Insira o CPF do cliente:",
                    key="cpf_temp",
                    help="Insira um CPF válido com 11 dígitos."
                )
            
            # Botão para inserir o CPF
            if st.button("Inserir", key="botao_inserir_cpf", on_click=self._validar_cpf):
                if len(st.session_state.messages) > 0:
                    for message in st.session_state.messages:
                        st.error(message)
                else:
                    st.session_state.cpf = st.session_state.cpf_temp
        
        if st.session_state.cpf != "":
            # Define a variável de data e hora de início do chat
            if st.session_state.data_hora_inicio == "":
                st.session_state.data_hora_inicio = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            # Exibe informações iniciais do chat
            st.write(f"Data e hora de início do chat: {st.session_state.data_hora_inicio}")
            st.write("CPF do cliente:", st.session_state.cpf)
            
            # Passo 2. Inserir um assunto válido
            if st.session_state.assunto == "":
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    assunto = st.selectbox("Selecione o assunto:", ["", "Negociação", "Boleto", "Reclamação"], key="assunto_selecionado")

                # Botão para inserir o assunto
                botao_inserir_assunto = st.button("Inserir assunto", on_click=self._inserir_assunto, key="inserir_assunto")
                if botao_inserir_assunto:
                    st.error("Insira um assunto válido.")

            # Exibe assunto selecionado e salva as informações no banco de dados
            if st.session_state.assunto != "":
                st.write("Assunto:", st.session_state.assunto)
                st.write("---")

    ### INFO INICIAIS ###


    ### INFO CLIENTE + POLITICA + CARREGAR HISTORICO MENSAGENS ###

    def _calcula_ciclo(self, dias_atraso):
        """
        Transforma a variável "dias_atraso" em ciclo.

        Returns:
        str: Ciclo relativo aos dias em atraso.
        """
        ciclos = [
            (30, "Ciclo 1"),
            (60, "Ciclo 2"),
            (90, "Ciclo 3"),
            (120, "Ciclo 4"),
            (150, "Ciclo 5"),
        ]

        for limite, ciclo in ciclos:
            if dias_atraso <= limite:
                return ciclo

        return "Ciclo 6"


    def _carregar_politica(self, dias_atraso, prob_rolagem):
        """
        Busca os dados da política no banco de dados e retorna em um dicionário.
        
        Args:
        dias_atraso (int): Quantidade de dias em atraso do cliente.
        prob_rolagem (str): Cluster de probabilidade de rolagem do cliente.

        Returns:
        dict: Dicionário com informações da política aplicável ao cliente.
        """

        path = "./data/"
        file = "politica.xlsx"
        ciclo = self._calcula_ciclo(dias_atraso)
        
        dados_politica = pd.read_excel(os.path.join(path, file))
        dados_politica_filtrada = dados_politica[(dados_politica["ciclo"] == ciclo) & (dados_politica["prob_rolagem"] == prob_rolagem)]
        return dados_politica_filtrada.to_dict(orient="records")[0]


    def _carregar_dados_cliente(self):
        """
        Busca os dados do cliente e os retorna em um dicionário.

        Returns:
        dict: Dicionário com informações do cliente.
        """
        path = "./data/"
        file = "base_clientes_excel.xlsx"
        cpf = int(st.session_state.cpf)

        # Para produção, podemos usar um banco de dados mais robusto, como SQLite
        # query = f"SELECT * FROM customer_database_table WHERE cpf = "{cpf}""        
        # with sqlite3.connect(os.path.join(path, "customer_database.sqlite")) as conn:
        #     consulta_cliente = pd.read_sql_query(query, conn)

        # Para testes iniciais, vamos usar um arquivo Excel
        # Também estamos considerando que todos os CPFs possuem apenas 1 contrato
        consulta_cliente = pd.read_excel(os.path.join(path, file))
        consulta_cliente = consulta_cliente[consulta_cliente["cpf"] == cpf]

        dados_cliente = {}
        if consulta_cliente.shape[0] > 0:
            dados_cliente = {
                "nome": consulta_cliente["nome"].values[0],
                "segmento": consulta_cliente["segmento"].values[0],
                "genero": consulta_cliente["genero"].values[0],
                "prob_rolagem": consulta_cliente["prob_rolagem"].values[0],
                "data_nascimento": consulta_cliente["data_nascimento"].values[0].astype('M8[D]').astype(datetime).strftime("%Y-%m-%d"), # .astype(datetime),
                "idade": relativedelta(datetime.today(), consulta_cliente["data_nascimento"].values[0].astype('M8[D]').astype(datetime)).years,
                "produto": consulta_cliente["produto"].values[0],
                "nro_contrato": consulta_cliente["nro_contrato"].values[0],
                "vlr_divida": consulta_cliente["vlr_divida"].values[0],
                "dias_atraso": consulta_cliente["dias_atraso"].values[0]
            }

        return dados_cliente
    

    def _carregar_dados_conversa(self):
        """
        Carrega os dados da conversa do cliente a partir do banco de dados.

        Returns:
        list: Lista com os dicionários de informações históricas do chat.
        """
        
        dados_conversa = self.collection.aggregate([
            {"$match": {"cpf": int(st.session_state.cpf)}},
            {"$unwind": "$conversas"},
            {"$match": {"conversas.assunto": st.session_state.assunto}},
            {"$unwind": "$conversas.chats"},
            {"$match": {"conversas.chats.data_hora_inicio": st.session_state.data_hora_inicio}},
            {"$project": {
                "_id": 0,
                "chat": "$conversas.chats"
            }}
        ])
        dados_conversa = list(dados_conversa)[0]["chat"]["mensagens"]
        return dados_conversa


    def exibir_informacoes_cliente(self):
        """
        Exibe informações do cliente obtidas a partir do banco de dados, caso o CPF esteja registrado.
        """

        if st.session_state.assunto != "":   
            st.session_state.dados_cliente = self._carregar_dados_cliente()

            if st.session_state.dados_cliente == {}: # Se não encontrar o CPF
                st.error("CPF não encontrado na base de clientes. Siga com o atendimento sem o auxílio deste Chatbot.")
                SaveData().inserir_cliente()

            
            # Se encontrar o CPF, carrega a política atualizada e exibe as informações do cliente
            else:
                st.session_state.politica = self._carregar_politica(
                    st.session_state.dados_cliente["dias_atraso"],
                    st.session_state.dados_cliente["prob_rolagem"]
                )
                
                # Define quais variáveis do cliente serão exibidas
                variaveis_cliente_exibir = [
                    ("Nome", "nome"),
                    ("Segmento", "segmento"),
                    ("Idade", "idade"),
                    ("Valor da dívida", "vlr_divida"),
                    ("Dias em atraso", "dias_atraso")
                ]

                # Escreve as informações do cliente na tela
                st.subheader("Informações do cliente:")
                for label, var in variaveis_cliente_exibir:
                    st.write(f"{label}: {st.session_state.dados_cliente[var]}")
                st.write("---")

                # Define a variável de sessão de histórico de conversa
                st.session_state.dados_conversa = []
                if st.session_state.carregar_historico:
                    st.session_state.dados_conversa = self._carregar_dados_conversa()
                    st.session_state.carregar_historico = False

    ### INFO CLIENTE + POLITICA + CARREGAR HISTORICO MENSAGENS ###

    ####################################### FUNÇÃO BOT #######################################

    def _aplicar_feedback(self):
        """
        Função para o criar o elemento de feedback, solicitar a avaliação do agente e atualizar as variáveis de feedback.
        
        Returns:
        str: Feedback aplicado pelo agente.
        """

        # Escala de notas com descrição, para auxiliar o agente
        escala_notas = """
            1 – Resposta Crítica. Poderia causar dano na imagem do banco, gerar reclamações por parte do cliente ou ainda um processo judicial.\n Ação recomendada: Responda o cliente com suas próprias palavras, descartando completamente a sugestão da IA.\n\n
            2 – Resposta Ruim. Sem riscos de danos ao banco ou de reclamação por parte do cliente, mas não avalio como um bom atendimento.\n Ação recomendada: Responda o cliente com suas próprias palavras, descartando completamente a sugestão da IA.\n\n
            3 – Resposta Razoável. Resposta correta, porém poderia ser mais empático/educado.\n Ação recomendada: Responda o cliente utilizando a sugestão da IA fazendo os ajustes necessários.\n\n
            4 – Boa resposta. Praticamente a mesma resposta que eu daria, porém faria alguns ajustes.\n Ação recomendada: Responda o cliente utilizando a sugestão da IA fazendo leves ajustes.\n\n
            5 – Ótima resposta. Resposta igual ou ainda melhor do que a resposta que eu daria.\n Ação recomendada: Responda o cliente a sugestão da IA, sem alterações.
        """

        # Cria o eLemento de feedback
        feedback = st.radio(
            "Passo 2. Avalie a sugestão da IA:",
            (
                "1 – Resposta Crítica",
                "2 – Resposta Ruim",
                "3 – Resposta Razoável",
                "4 – Boa Resposta",
                "5 – Ótima Resposta",
            ),
            help=escala_notas,
            key="feedback", 
        )

        # Botão para aplicar o feedback
        bt_aplicar_feedback = st.button("Aplicar Feedback", key=f"feedback_{len(st.session_state.dados_conversa)+1}")
        if bt_aplicar_feedback:
            st.session_state.aplicar_feedback = True # Atualiza o estado para indicar que o feedback foi aplicado
        else:
            st.error("Por favor, avalie a sugestão da IA antes de prosseguir.") # Essa mensagem permanece até que o usuário aplique o feedback

        return feedback


    def _resposta_bot(dados_cliente, politica, historico_mensagens, mensagem_cliente):
        """
        Função para obter a sugestão de resposta do bot a partir da mensagem do cliente.

        Args:
        historico_conversa (dict): Dicionário contendo dados do cliente e dados conversa, históricos e atuais.
        mensagem_cliente (str): Mensagem do cliente.

        Returns:
        str: Sugestão de resposta do bot.
        """

        # resposta = get_completion(dados_cliente, politica, historico_mensagens, mensagem_cliente)

        # Resposta padrão para teste
        resposta = "Olá! O que posso fazer por você hoje?"
        return resposta


    def exibir_elemento_chat(self):
        """
        Função para o criar o elemento de feedback, solicitar a avaliação do agente e atualizar as variáveis de feedback.
        """

        # Precisa definir essas variáveis de sessão no início da aplicação !!!
        dados_cliente = st.session_state.dados_cliente
        politica = st.session_state.politica

        dados_conversa = st.session_state.dados_conversa
        qtd_mensagens_historico = len(dados_conversa)

        # st.write(qtd_mensagens_historico)

        # Usuário (agente) deve inserir a mensagem recebida do cliente
        mensagem_cliente = st.text_input(
            label=f"Passo 1. Insira a mensagem que o cliente enviou:",
            key=f"mensagem_cliente_{qtd_mensagens_historico+1}"
        )
        data_hora_mensagem = datetime.now()

        # Bot recebe a mensagem do cliente e sugere uma resposta
        if mensagem_cliente:
            historico_mensagens = []
            if len(dados_conversa) > 0:
                keys_historico_bot = ['id', 'data_hora', 'mensagem_cliente', "resposta_final_operador"]
                for i in dados_conversa:
                    novo_dict_conversa = {k: i[k] for k in keys_historico_bot}
                    historico_mensagens.append(novo_dict_conversa)

            sugestao_bot = self._resposta_bot(dados_cliente, politica, historico_mensagens, mensagem_cliente)
            st.write(f"Sugestão da IA: {sugestao_bot}")
            
            # Botão para copiar a sugestão do bot
            if st.button("Copiar sugestão"):
                pyperclip.copy(sugestao_bot)
                st.success("Sugestão copiada!")

            # Usuário (agente) deve avaliar a sugestão da IA
            if not st.session_state.aplicar_feedback:
                feedback = self._aplicar_feedback()

        # Após o usuário aplicar o feedback ele deve inserir a resposta final que ele vai enviar ao cliente e adicionar a nova interação ao histórico da conversa
        if st.session_state.aplicar_feedback:
            resposta_agente = st.text_input("Passo 3. Insira a mensagem que você vai enviar ao cliente:", value=st.session_state.sugestao_bot[-1], key=f"resposta_agente")
            bt_add_historico = st.button("Adicionar ao histórico", key=f"historico_{qtd_mensagens_historico+1}")
            
            if bt_add_historico:
                st.session_state.aplicar_feedback = False

                dict_mensagem = {
                    "id": len(st.session_state.dados_conversa) + 1,
                    "data_hora": data_hora_mensagem.strftime("%Y-%m-%d") + " - " + data_hora_mensagem.strftime("%H:%M"),
                    "mensagem_cliente": mensagem_cliente,
                    "sugestao_ia": sugestao_bot,
                    "rating_sugestao_ia": feedback,
                    "resposta_final_operador": resposta_agente,
                }

                st.session_state.dados_conversa.append(dict_mensagem)
                SaveData().inserir_mensagem(dict_mensagem)
                st.experimental_rerun()

    ####################################### FUNÇÃO BOT #######################################


    ### EXIBIR CONVERSA ###

    def exibir_historico_conversa(self, asc=False):
        """
        Exibe o histórico da conversa do cliente a partir dos dados carregados.

        Args:
        dados_conversa (dict): Dicionário com os dados da conversa do cliente.
        asc (bool): Flag para ordenar o histórico de forma ascendente ou descend
        """
        
        if len(st.session_state.dados_conversa) > 0:
            
            if st.session_state["novo_chat"]:
                SaveData().inserir_cliente()
                st.session_state.novo_chat = False

            dados_conversa_exibir = st.session_state.dados_conversa.copy()
            if not asc:
                dados_conversa_exibir.reverse()
            st.write("---")
            st.write("### Histórico da Conversa")
            st.write("---")
            # st.button(classificar) # botão para classificar a conversa (em versão futura)
            for conversa in dados_conversa_exibir:
                st.write(f"ID: {conversa['id']} - Data e Hora: {conversa['data_hora']}")
                st.write(f"Mensagem do cliente: {conversa['mensagem_cliente']}")
                st.write(f"Sugestão da IA: {conversa['sugestao_ia']}  (Nota {conversa['rating_sugestao_ia']})")
                st.write(f"Resposta enviada ao cliente: {conversa['resposta_final_operador']}")
                st.write("---")

    ### EXIBIR CONVERSA ###