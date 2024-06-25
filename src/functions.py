from datetime import datetime
from dateutil.relativedelta import relativedelta
import streamlit as st
import pyperclip
from pycpfcnpj import cpf
from chatbot import bot_response
from save_conversations import conectar_mongo, inserir_cliente, inserir_mensagem
import sqlite3
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

    def _initialize_session_state(self):
        """
        Inicializa o estado da sessão com valores padrão, caso não estejam definidos.
        """
        if 'input_visibility' not in st.session_state:
            st.session_state.input_visibility = True

        if 'input_visibility_assunto' not in st.session_state:
            st.session_state.input_visibility_assunto = True

        if 'cpf_encontrado' not in st.session_state:
            st.session_state.cpf_encontrado = False

    def _inserir_cpf(self):
        """
        Insere o CPF no estado da sessão se for válido e esconde o campo de input.
        """
        cpf = st.session_state.cpf_temp
        if cpf.validate(cpf):
            st.session_state.input_visibility = False
            st.session_state.cpf_cliente = cpf

    def _inserir_assunto(self):
        """
        Insere o assunto no estado da sessão se não for vazio e esconde o campo de input.
        """
        assunto = st.session_state.assunto_temp
        if assunto != "":
            st.session_state.input_visibility_assunto = False
            st.session_state.assunto = st.session_state.assunto_temp

    def _carregar_dados_cliente(self):
        """
        Busca os dados do cliente do banco de dados e retorna em um dicionário.

        Returns:
        dict: Dicionário com informações do cliente.
        """
        path = "./data/"
        cpf_value = st.session_state.cpf_cliente
        
        query = f"SELECT * FROM customer_database_table WHERE cpf = '{cpf_value}'"        
        with sqlite3.connect(os.path.join(path, 'customer_database.sqlite')) as conn:
            consulta_cliente = pd.read_sql_query(query, conn)
        
        dados_cliente = {
            "cpf": consulta_cliente["cpf"][0],
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
        ciclo = self._calcula_ciclo(dias_atraso)

        query = f"SELECT * FROM politica_database_table WHERE ciclo = '{ciclo}' AND prob_rolagem = '{prob_rolagem}'"        
        with sqlite3.connect(os.path.join(path, 'politica_database.sqlite')) as conn:
            consulta_politica = pd.read_sql_query(query, conn)

        dados_oferta = dict()
        dados_oferta["dias_pgto"] = None
        dados_oferta["desc_vista"] = None
        dados_oferta["desc_exc_vista"] = None
        dados_oferta["qtd_max_parcelas"] = None
        dados_oferta["perc_min_entrada"] = None
        dados_oferta["vlr_min_parcela"] = None
        dados_oferta["desc_parc_3_12"] = None
        dados_oferta["desc_parc_13_24"] = None
        dados_oferta["desc_parc_25_36"] = None
        dados_oferta["desc_parc_37_48"] = None
        dados_oferta["desc_parc_49_60"] = None
        dados_oferta["juros_3_12"] = None
        dados_oferta["juros_13_24"] = None
        dados_oferta["juros_25_36"] = None
        dados_oferta["juros_37_48"] = None
        dados_oferta["juros_49_60"] = None
        dados_oferta["desc_exc_parc_3_12"] = None
        dados_oferta["desc_exc_parc_13_24"] = None
        dados_oferta["desc_exc_parc_25_36"] = None
        dados_oferta["desc_exc_parc_37_48"] = None
        dados_oferta["desc_exc_parc_49_60"] = None
        dados_oferta["juros_exc_3_12"] = None
        dados_oferta["juros_exc_13_24"] = None
        dados_oferta["juros_exc_25_36"] = None
        dados_oferta["juros_exc_37_48"] = None
        dados_oferta["juros_exc_49_60"] = None

        return dados_oferta


    def _store_customer_data(self, cpf, dados_cliente, dados_oferta, assunto, dt_hr_ini):
        inserir_cliente(cpf, dados_cliente, dados_oferta, assunto, dt_hr_ini)





    def _display_customer_info(self, dados_cliente, dados_oferta):
        """
        Exibe informações do cliente obtidas a partir do banco de dados, caso o CPF esteja registrado.
        """
        
        # Define quais variáveis do cliente serão exibidas
        variaveis_exibir = [
            ("Nome", "nome"),
            ("Segmento", "segmento"),
            ("Idade", "idade"),
            ("Valor da dívida", "vlr_divida"),
            ("Dias em atraso", "dias_atraso")
        ]

        st.subheader("Informações do cliente:")
        for label, var in variaveis_exibir:
            st.write(f"{label}: {dados_cliente[var]}")
        st.write("---")
        
        st.session_state.cpf_encontrado = True

        cpf = st.session_state.cpf_cliente
        assunto = st.session_state.assunto
        dt_hr_ini = st.session_state.dt_hr_ini






    def display_chat_interface(self):
        """
        Exibe a interface do chat para inserção de CPF, seleção de assunto e exibição de dados do cliente.
        """
        if st.session_state.input_visibility:
            # Exibe o campo de entrada do CPF
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                campo_cpf = st.text_input("Insira o CPF do cliente:", key='cpf_temp', help="Insira um CPF válido com 11 dígitos.")
            
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
        if 'cpf_cliente' in st.session_state:
            st.session_state.dt_hr_ini = datetime.now().strftime("%d/%m/%Y %H:%M")
            st.write(f"Data e hora de início do chat: {st.session_state.dt_hr_ini}") # Data e hora de início do chat
            st.write("CPF do cliente:", st.session_state.cpf_cliente) # CPF do cliente
            
            # Exibe campo para seleção do assunto
            if st.session_state.input_visibility_assunto:
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    assunto = st.selectbox("Selecione o assunto:", ["", "Negociação", "Boleto", "Reclamação"], key='assunto_temp')

                # Botão para inserir o assunto
                botao_inserir_assunto = st.button("Inserir assunto", on_click=self._inserir_assunto, key="inserir_assunto")
                if botao_inserir_assunto:
                    st.error("Insira um assunto válido.")

            # Exibe assunto selecionado
            if "assunto" in st.session_state:
                st.write("Assunto:", st.session_state.assunto)
                st.write("---")

            if "assunto" in st.session_state:
                self.display_customer_info()






# Exibir chat



# Função para exibir histórico de interações
def display_interaction():
    # Verifica se houve alguma interação
    if st.session_state.interaction_count > 0:
        # Exibição das interações
        st.write("---")
        st.write("### Histórico da Conversa")
        st.write("---")

        range_interactions = list(range(st.session_state.interaction_count - 1, -1, -1))
        # Exibir da mensagem mais recente para a mais antiga
        for p, i in enumerate(range_interactions):
            current_time = st.session_state.datetime_message[i].strftime("%H:%M:%S")
            current_date = st.session_state.datetime_message[i].strftime("%Y-%m-%d")
            _id = i+1
            st.write(f"ID: {_id} / Data: {current_date} / Hora: {current_time}") # Colocar datas e horas corretas
            st.write(f"Mensagem do cliente: {st.session_state.customer_messages[i]}") #####
            st.write(f"Sugestão da IA: {st.session_state.bot_suggestions[i]}  (Nota {st.session_state.user_ratings[i]})") #####
            st.write(f"Resposta enviada ao cliente: {st.session_state.user_responses[i]}")
            st.write("---")

# Função para exibir o chat
def display_chat():
    # Inicialização das variáveis de sessão
    if "interaction_count" not in st.session_state:
        st.session_state.interaction_count = 0
    if "customer_messages" not in st.session_state:
        st.session_state.customer_messages = []
    if "bot_suggestions" not in st.session_state:
        st.session_state.bot_suggestions = []
    if "user_ratings" not in st.session_state:
        st.session_state.user_ratings = []
    if "user_responses" not in st.session_state:
        st.session_state.user_responses = []
    if "feedback_applied" not in st.session_state:
        st.session_state.feedback_applied = False
    if "datetime_message" not in st.session_state:
        st.session_state.datetime_message = []

    # Exibição do campo para o usuário inserir a mensagem do cliente
    customer_message = st.text_input(label=f"Passo 1. Insira a mensagem que o cliente enviou:", key=f"customer_message_{st.session_state.interaction_count}")

    # Escala de notas que o usuário deve utilizar para avaliar a sugestão da IA
    escala_notas = """
        1 – Resposta Crítica. Poderia causar dano na imagem do banco, gerar reclamações por parte do cliente ou ainda um processo judicial.\n
        2 – Resposta Ruim. Sem riscos de danos ao banco ou de reclamação por parte do cliente, mas não avalio como um bom atendimento.\n
        3 – Resposta Razoável. Resposta correta, porém poderia ser mais empático/educado.\n
        4 – Boa resposta. Praticamente a mesma resposta que eu daria, porém faria alguns ajustes.\n
        5 – Ótima resposta. Resposta igual ou ainda melhor do que a resposta que eu daria.\n
    """

# 1 - Descarte completamente a sugestão da IA
# 2 - Descarte completamente a sugestão da IA
# 3 - Faça os ajustes necessários na sugestão da IA
# 4 - Fazer ajustes leves na sugestão da IA
# 5 - Envie a resposta sugerida pela IA sem alterações


	# 0 – Crítico. Poderia gerar dano na imagem do banco, processo judicial, ou ainda gerar reclamações por parte do cliente.
    # 1 – Ruim. Sem riscos de danos ao banco ou de reclamação por parte do cliente, mas avalio como um bom atendimento.
	# 3 – Razoável. Resposta correta, porém poderia ser mais empático/educado.
	# 4 – Boa resposta. Praticamente a mesma resposta que eu daria, porém com alguns ajustes.
	# 5 – Ótima resposta. Resposta igual ou ainda melhor do que a resposta que eu daria.

    # Exibe sugestões de resposta do bot e permite a avaliação
    if customer_message and not st.session_state.feedback_applied:
        bot_suggestion = bot_response(customer_message) # Sugestão de resposta do bot
        st.session_state.datetime_message.append(datetime.now()) # Salva a data e hora da mensagem
        st.write(f"Sugestão da IA: {bot_suggestion}") # Exibe a sugestão do bot
        
        # Botão para copiar a sugestão
        if st.button('Copiar sugestão'):
            pyperclip.copy(bot_suggestion)
            st.success('Sugestão copiada!')

        # ELemento de feedback
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
        bt_aplicar_feedback = st.button("Aplicar Feedback", key=f"feedback_{st.session_state.interaction_count}")
        if bt_aplicar_feedback:
            st.session_state.customer_messages.append(customer_message) # Salva a mensagem do cliente
            st.session_state.bot_suggestions.append(bot_suggestion) # Salva a sugestão do bot
            st.session_state.user_ratings.append(feedback) # Salva o feedback do usuário
            st.session_state.feedback_applied = True
        else:
            st.error("Por favor, avalie a sugestão da IA antes de prosseguir.")

    # Se o feedback for aplicado, exibe o campo para o usuário inserir a resposta que ele vai enviar ao cliente
    if st.session_state.feedback_applied:
        user_response = st.text_input("Passo 3. Insira a mensagem que você vai enviar ao cliente:", value=st.session_state.bot_suggestions[-1], key=f"user_response")
        bt_add_historico = st.button("Adicionar ao histórico", key=f"historico_{st.session_state.interaction_count}")
        
        if bt_add_historico:
            st.session_state.user_responses.append(user_response) # Salva a resposta do usuário
            st.session_state.interaction_count += 1
            st.session_state.feedback_applied = False
            st.experimental_rerun()



# Armazenando dados da mensagem
cpf = ""
assunto = ""
dt_hr_ini = ""

dict_mensagem = {
    "id": _id,
    "data_hora": current_date + " - " + current_time,
    "mensagem_cliente": customer_message,
    "sugestao_ia": bot_suggestion,
    "rating_sugestao_ia": feedback,
    "resposta_final_operador": user_response,
}

# dict_mensagem = {
#     "id": 1,
#     "data_hora": "2024-06-27 10:30:00",
#     "mensagem_cliente": "Iphone 24",
#     "sugestao_ia": "Esse produto não existe",
#     "rating_sugestao_ia": 4,
#     "resposta_final_operador": "Sr. João, o produto correto é o Iphone 15",
# }

inserir_mensagem(cpf, assunto, dt_hr_ini, dict_mensagem)



####################################################################################################################################

# Formato Json


# Para 1 cliente
# {
#     "dados_cliente": {
#         "cpf": "123.456.789-00",
#         "nome": "Carlos Silva",
#         "email": "carlos.silva@example.com",
#         "telefone": "(11) 1234-5678"
#     },
#     "dados_conversa": [
#         {
#             "id": 1,
#             "data": "2024-06-01",
#             "hora": "12h42",
#             "mensagem_cliente": "bom dia",
#             "sugestao_ia": "bom dia, sr.",
#             "resposta_final": "bom dia, sr. Carlos",
#             "rating": "4. Boa Resposta"
#         },
#         {
#             "id": 2,
#             "data": "2024-06-01",
#             "hora": "14h15",
#             "mensagem_cliente": "qual o status do meu pedido?",
#             "sugestao_ia": "Seu pedido está a caminho.",
#             "resposta_final": "Seu pedido está a caminho e deve chegar até o fim do dia.",
#             "rating": "5. Excelente"
#         }
#     ]
# }


# Para mais de 1 cliente
# {
#     "clientes": {
#         "987.654.321-00": {
#             "dados_cliente": {
#                 "nome": "Ana Pereira",
#                 "email": "ana.pereira@example.com",
#                 "telefone": "(21) 9876-5432"
#             },
#             "conversas": [
#                 {
#                     [
#                        {"id": 1,
    #                     "assunto": "Entrega",
    #                     "data_hora_inicio": ["2024-06-01 - 12h42"],
    #                     "mensagens": [
    #                         {
    #                             "data": "2024-06-01",
    #                             "hora": "09h30",
    #                             "mensagem_cliente": "olá",
    #                             "sugestao_ia": "olá, como posso ajudar?",
    #                             "resposta_final": "olá, Ana. Como posso ajudar?",
    #                             "rating": "5. Excelente"
    #                         },
    #                         {
    #                             "data": "2024-06-01",
    #                             "hora": "10h00",
    #                             "mensagem_cliente": "gostaria de saber sobre a minha entrega",
    #                             "sugestao_ia": "Seu pedido está em processamento.",
    #                             "resposta_final": "Seu pedido está em processamento e será enviado em breve.",
    #                             "rating": "4. Boa Resposta"
    #                         }
#                     ]
#                 }
#             ]
#         }
#     }
# }




##### sidebar

def exibir_historico():
    pass

def exibir_chat_encontrado():
    pass

def pesquisar_chat():
    pass



