from datetime import datetime
from dateutil.relativedelta import relativedelta
import streamlit as st
import pyperclip
from pycpfcnpj import cpf
from chatbot import bot_response
from save_conversations import conectar_mongo, inserir_cliente, inserir_mensagem
import sqlite3
import pymongo
import pandas as pd
import os
# Chat

def info_cliente():
    pass


def configuracoes_iniciais_chat():
    # info_cliente()
    pass


def iniciar_novo_chat():
    # configuracoes_iniciais_chat()
    pass







# functions.py


class CustomerChat:
    def __init__(self):
        """
        Método construtor da classe CustomerChat.
        Inicializa o estado da sessão ao instanciar a classe.
        """
        self._initialize_session_state()
        self.st.session_state["filtro"] = 0

        # Variáveis de conexão com o banco de dados
        self.client, self.db, self.collection = self._conectar_mongo()


    def _conectar_mongo(self):
        """
        Função para conectar ao banco de dados MongoDB.

        Returns:
        pymongo.MongoClient, pymongo.database.Database, pymongo.collection.Collection: Conexão com o banco de dados.
        """
        try:
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            client.server_info()
            db = client["db_conversas"]
            collection = db["clientes_conversas"]
            return client, db, collection
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")
            return None


    def _initialize_session_state(self):
        """
        Inicializa o estado da sessão com valores padrão, caso não estejam definidos.
        """
        # Variáveis de controle do chat
        st.session_state.inserir_cpf = True
        st.session_state.inserir_assunto = True
        st.session_state.cpf_encontrado = False


    def _inserir_cpf(self):
        """
        Insere o CPF no estado da sessão se for válido e esconde o campo de input.
        """
        cpf = st.session_state.cpf_temp
        if cpf.validate(cpf):
            st.session_state.inserir_cpf = False
            st.session_state.cpf_cliente = cpf

            
    def _inserir_assunto(self):
        """
        Insere o assunto no estado da sessão se não for vazio e esconde o campo de input.
        """
        assunto = st.session_state.assunto_temp
        if assunto != "":
            st.session_state.inserir_assunto = False
            st.session_state.assunto = st.session_state.assunto_temp


    def _carregar_dados_cliente(self):
        """
        Busca os dados do cliente do banco de dados e retorna em um dicionário.

        Returns:
        dict: Dicionário com informações do cliente.
        """
        path = "./data/"
        file = "base_clientes_excel.xlsx"
        # cpf_value = st.session_state.cpf_cliente

        # Para testes iniciais, vou usar um arquivo Excel
        consulta_cliente = pd.read_excel(os.path.join(path, file))
        consulta_cliente = consulta_cliente[consulta_cliente["cpf"] == st.session_state.cpf_cliente]
        
        # query = f"SELECT * FROM customer_database_table WHERE cpf = "{cpf_value}""        
        # with sqlite3.connect(os.path.join(path, "customer_database.sqlite")) as conn:
        #     consulta_cliente = pd.read_sql_query(query, conn)

        dados_cliente = {
            "nome": consulta_cliente["nome"][0],
            "segmento": consulta_cliente["segmento"][0],
            "genero": consulta_cliente["genero"][0],
            "prob_rolagem": consulta_cliente["prob_rolagem"][0],
            "data_nascimento": consulta_cliente["data_nascimento"][0],
            "idade": relativedelta(datetime.today(), consulta_cliente["data_nascimento"][0]).years,
            "produto": consulta_cliente["produto"][0],
            "nro_contrato": consulta_cliente["nro_contrato"][0],
            "vlr_divida": consulta_cliente["vlr_divida"][0],
            "dias_atraso": consulta_cliente["dias_atraso"][0]
        }

        return dados_cliente


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

        consulta_politica = pd.read_excel(os.path.join(path, file))
        consulta_politica = consulta_politica[(consulta_politica["ciclo"] == ciclo) & (consulta_politica["prob_rolagem"] == prob_rolagem)]

        dados_politica = dict()
        dados_politica["dias_pgto"] = consulta_politica["dias_pgto"]
        dados_politica["desc_vista"] = consulta_politica["desc_vista"]
        dados_politica["desc_exc_vista"] = consulta_politica["desc_exc_vista"]
        dados_politica["qtd_max_parcelas"] = consulta_politica["qtd_max_parcelas"]
        dados_politica["perc_min_entrada"] = consulta_politica["perc_min_entrada"]
        dados_politica["vlr_min_parcela"] = consulta_politica["vlr_min_parcela"]
        dados_politica["desc_parc_3_12"] = consulta_politica["desc_parc_3_12"]
        dados_politica["desc_parc_13_24"] = consulta_politica["desc_parc_13_24"]
        dados_politica["desc_parc_25_36"] = consulta_politica["desc_parc_25_36"]
        dados_politica["desc_parc_37_48"] = consulta_politica["desc_parc_37_48"]
        dados_politica["desc_parc_49_60"] = consulta_politica["desc_parc_49_60"]
        dados_politica["juros_3_12"] = consulta_politica["juros_3_12"]
        dados_politica["juros_13_24"] = consulta_politica["juros_13_24"]
        dados_politica["juros_25_36"] = consulta_politica["juros_25_36"]
        dados_politica["juros_37_48"] = consulta_politica["juros_37_48"]
        dados_politica["juros_49_60"] = consulta_politica["juros_49_60"]
        dados_politica["desc_exc_parc_3_12"] = consulta_politica["desc_exc_parc_3_12"]
        dados_politica["desc_exc_parc_13_24"] = consulta_politica["desc_exc_parc_13_24"]
        dados_politica["desc_exc_parc_25_36"] = consulta_politica["desc_exc_parc_25_36"]
        dados_politica["desc_exc_parc_37_48"] = consulta_politica["desc_exc_parc_37_48"]
        dados_politica["desc_exc_parc_49_60"] = consulta_politica["desc_exc_parc_49_60"]
        dados_politica["juros_exc_3_12"] = consulta_politica["juros_exc_3_12"]
        dados_politica["juros_exc_13_24"] = consulta_politica["juros_exc_13_24"]
        dados_politica["juros_exc_25_36"] = consulta_politica["juros_exc_25_36"]
        dados_politica["juros_exc_37_48"] = consulta_politica["juros_exc_37_48"]
        dados_politica["juros_exc_49_60"] = consulta_politica["juros_exc_49_60"]

        return dados_politica


    def _carregar_dados_conversas(self, cpf, assunto, dt_hr_ini):
        """
        Documentar
        
        Args: 
        
        Returns:
        
        """

        # Carrega dados historicos do Mongo DB
        

        cpf = st.session_state.cpf_cliente
        assunto = st.session_state.assunto
        dt_hr_ini = st.session_state.dt_hr_ini
        
        
        pass


   # Função para exibir na tela as informações do cliente e iniciais do chat
    def _display_customer_info(self):
        """
        Exibe informações do cliente obtidas a partir do banco de dados, caso o CPF esteja registrado.
        """

        dados_cliente = self._carregar_dados_cliente()
        dados_politica = self._carregar_politica(dados_cliente["dias_atraso"], dados_cliente["prob_rolagem"])
        
        # Define quais variáveis do cliente serão exibidas
        variaveis_cliente_exibir = [
            ("Nome", "nome"),
            ("Segmento", "segmento"),
            ("Idade", "idade"),
            ("Valor da dívida", "vlr_divida"),
            ("Dias em atraso", "dias_atraso")
        ]

        # variaveis_oferta_exibir = []

        # Escreve as informações do cliente na tela
        st.subheader("Informações do cliente:")
        for label, var in variaveis_cliente_exibir:
            st.write(f"{label}: {dados_cliente[var]}")
        st.write("---")
        
        st.session_state.cpf_encontrado = True

        # Armazena os dados do cliente e da oferta no banco de dados
        inserir_cliente(
            cpf=st.session_state.cpf_cliente,
            dados_cliente=dados_cliente,
            dados_politica=dados_politica,
            assunto=st.session_state.assunto,
            dt_hr_ini=st.session_state.dt_hr_ini
        )


    # Função para iniciar chat com novo cliente
    def display_chat_interface(self):
        """
        Exibe a interface do chat para inserção de CPF, seleção de assunto e exibição de dados do cliente.
        """
        # Passo 1. Inserir o CPF do cliente
        if st.session_state.inserir_cpf:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                campo_cpf = st.text_input("Insira o CPF do cliente:", key="cpf_temp", help="Insira um CPF válido com 11 dígitos.")
            
            # Botão para inserir o CPF
            botao_inserir = st.button("Inserir", on_click=self._inserir_cpf, key="inserir_cpf")
            if botao_inserir:
                # Validações do CPF
                if not campo_cpf.isdigit():
                    st.error("CPF inválido. Insira somente números.")
                else:
                    if len(campo_cpf) != 11:
                        st.error("O CPF precisa ter exatamente 11 dígitos. Complete com zeros à esquerda, se necessário.")
                    else:
                        st.error("CPF inválido. Verifique e tente novamente.")

        # Verifica se o CPF foi inserido para continuar a exibição das demais informações
        if "cpf_cliente" in st.session_state:
            st.session_state.dt_hr_ini = datetime.now().strftime("%d/%m/%Y %H:%M").copy() # Isso somente se for um novo chat
            st.write(f"Data e hora de início do chat: {st.session_state.dt_hr_ini}") # Data e hora de início do chat
            st.write("CPF do cliente:", st.session_state.cpf_cliente) # CPF do cliente
            
            # Passo 2. Inserir um assunto válido
            if st.session_state.inserir_assunto:
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    assunto = st.selectbox("Selecione o assunto:", ["", "Negociação", "Boleto", "Reclamação"], key="assunto_temp")

                # Botão para inserir o assunto
                botao_inserir_assunto = st.button("Inserir assunto", on_click=self._inserir_assunto, key="inserir_assunto")
                if botao_inserir_assunto:
                    st.error("Insira um assunto válido.")

            # Exibe assunto selecionado
            if "assunto" in st.session_state:
                st.write("Assunto:", st.session_state.assunto)
                st.write("---")

            # Se o assunto foi inserido, busca e exibe informações do cliente
            if "assunto" in st.session_state:
                self._display_customer_info()










#### Função chat ####

class CustomerChatBot:
    def __init__(self):
        """
        Método construtor da classe CustomerChat.
        Inicializa o estado da sessão ao instanciar a classe.
        """
        self._initialize_session_state()


    def _initialize_session_state(self):
        """
        Inicializa o estado da sessão com valores padrão, caso não estejam definidos.
        """
        if "interaction_count" not in st.session_state:
            st.session_state.interaction_count = 0
        if "feedback_applied" not in st.session_state:
            st.session_state.feedback_applied = False


    def _resposta_bot(dados_cliente_historico, mensagem_cliente):
        """
        Função para obter a sugestão de resposta do bot a partir da mensagem do cliente.

        Args:
        historico_conversa (dict): Dicionário contendo dados do cliente e dados conversa, históricos e atuais.
        mensagem_cliente (str): Mensagem do cliente.

        Returns:
        str: Sugestão de resposta do bot.
        """
        # resposta = get_completion(dados_cliente_historico, mensagem_cliente)

        # Resposta padrão para teste
        resposta = "Olá! Como posso ajudar você?"
        return resposta


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
        bt_aplicar_feedback = st.button("Aplicar Feedback", key=f"feedback_{st.session_state.interaction_count}")
        if bt_aplicar_feedback:
            st.session_state.feedback.append(feedback) # Salva o feedback do usuário
            st.session_state.feedback_applied = True # Atualiza o estado para indicar que o feedback foi aplicado
        else:
            st.error("Por favor, avalie a sugestão da IA antes de prosseguir.") # Essa mensagem permanece até que o usuário aplique o feedback

        return feedback


    def _exibir_historico_chat(self):
        # data_hora_mensagem, mensagem_cliente, sugestao_bot, feedback, resposta_agente
        """
        Função para obter a sugestão de resposta do bot a partir da mensagem do cliente.
        """

        dados_conversa = self._carrega_dados_conversas(cpf, assunto, dt_hr_ini)

        # Organiza os dados da conversa
        qtd_mensagens = len(dados_conversa["data_hora_mensagem"])
        data_hora_mensagem = dados_conversa["data_hora_mensagem"]
        mensagem_cliente = dados_conversa["mensagem_cliente"]
        sugestao_bot = dados_conversa["sugestao_bot"]
        feedback = dados_conversa["feedback"]
        resposta_agente = dados_conversa["resposta_agente"]

        # Somente exibe o histórico se houver mensagens
        if qtd_mensagens > 0:
            st.write("---")
            st.write("### Histórico da Conversa")
            st.write("---")
            
            # Exibe as mensagens, da mais recente para a mais antiga
            for i in range(qtd_mensagens-1, -1, -1):
                _id = i+1
                st.write(f"ID: {_id} / Data e Hora: {data_hora_mensagem[i]}")
                st.write(f"Mensagem do cliente: {mensagem_cliente[i]}")
                st.write(f"Sugestão da IA: {sugestao_bot[i]}  (Nota {feedback[i]})")
                st.write(f"Resposta enviada ao cliente: {resposta_agente[i]}")
                st.write("---")


    def display_chat(self):
        """
        Função para o criar o elemento de feedback, solicitar a avaliação do agente e atualizar as variáveis de feedback.
        """
        
        dados_cliente_historico = []
        mensagem_cliente = []

        # Passo 1. Usuário (agente) deve inserir a mensagem recebida do cliente
        customer_message = st.text_input(label=f"Passo 1. Insira a mensagem que o cliente enviou:", key=f"customer_message_{st.session_state.interaction_count}")
        data_hora_mensagem = datetime.now()

        # Passo 2. Bot recebe a mensagem do cliente e sugere uma resposta
        if customer_message:
            sugestao_bot = self._resposta_bot(dados_cliente_historico, mensagem_cliente)
            st.write(f"Sugestão da IA: {sugestao_bot}")
            
            # Botão para copiar a sugestão do bot
            if st.button("Copiar sugestão"):
                pyperclip.copy(sugestao_bot)
                st.success("Sugestão copiada!")

            # Passo 3. Usuário (agente) deve avaliar a sugestão da IA
            if not st.session_state.feedback_applied:
                feedback = self._aplicar_feedback()

        # Passo 4. Após o usuário aplicar o feedback ele deve inserir a resposta final que ele vai enviar ao cliente e adicionar a nova interação ao histórico da conversa
        if st.session_state.feedback_applied:
            resposta_agente = st.text_input("Passo 3. Insira a mensagem que você vai enviar ao cliente:", value=st.session_state.sugestao_bot[-1], key=f"resposta_agente")
            bt_add_historico = st.button("Adicionar ao histórico", key=f"historico_{st.session_state.interaction_count}")
            
            if bt_add_historico:
                st.session_state.interaction_count += 1
                st.session_state.feedback_applied = False # Reseta o estado para o próximo ciclo
                st.experimental_rerun() # Rerun da página para exibir a próxima interação da conversa




            # Armazenando dados da mensagem
            cpf = ""
            assunto = ""
            dt_hr_ini = ""

            id = "" # Adicionar 1 ao maior ID do histórico



            dict_mensagem = {
                "id": _id,
                "data_hora": data_hora_mensagem.strftime("%Y-%m-%d") + " - " + data_hora_mensagem.strftime("%H:%M"),
                "mensagem_cliente": customer_message,
                "sugestao_ia": sugestao_bot,
                "rating_sugestao_ia": feedback,
                "resposta_final_operador": resposta_agente,
            }

            inserir_mensagem(cpf, assunto, dt_hr_ini, dict_mensagem)

            # Carrega e exibe o histórico da conversa
            dados_conversa = self._carrega_dados_conversas(cpf, assunto, dt_hr_ini)
            self._exibir_historico_chat(dados_conversa)

#### Função chat ####