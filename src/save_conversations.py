
from pymongo import MongoClient

# Verifica e inicializa conexão com o banco de dados MongoDB
def conectar_mongo():
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.server_info()
        db = client['db_conversas']
        collection = db['clientes_conversas']
        return client, db, collection
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        return None

# Função para inserir os dados do cliente
def inserir_cliente(cpf, dados_cliente, dados_oferta, assunto, dt_hr_ini):
    client, db, collection = conectar_mongo()  # Conectar ao banco de dados
    cliente = collection.find_one({"cpf": cpf})
    # Inserir novo cliente se não existir
    if not cliente:
        collection.insert_one({
            "cpf": cpf,
            "dados_cliente": dados_cliente,
            "dados_oferta": dados_oferta,
            "conversas": [
                {
                    "assunto": assunto,
                    "chats": [
                        {
                            "data_hora_inicio": dt_hr_ini,
                            # "mensagens": []
                        }
                    ]
                }
            ]
        })
    else:
        # Inserir nova conversa caso o cliente já existir na base
        assunto_existe = collection.find_one({"cpf": cpf, "conversas.assunto": assunto})
        if not assunto_existe:
            print("assunto novo")
            # Adicionar um novo assunto com o chat inicial
            collection.update_one(
                {"cpf": cpf},
                {"$push": {
                    "conversas": {
                        "assunto": assunto,
                        "chats": [
                            {
                                "data_hora_inicio": dt_hr_ini,
                                # "mensagens": []
                            }
                        ]
                    }
                }}
            )
        else:
            # Adicionar um novo chat ao assunto existente
            collection.update_one(
                {"cpf": cpf, "conversas.assunto": assunto},
                {"$push": {
                    "conversas.$.chats": {
                        "data_hora_inicio": dt_hr_ini,
                        # "mensagens": []
                    }
                }}
            )

# def inserir_cliente(cpf, assunto, dt_hr_ini):#, cliente_dados):
#     client, db, collection = conexao_mongo() # Conectar ao banco de dados
#     cliente = collection.find_one({"cpf": cpf}) # Buscar cliente pelo CPF
#     # Inserir novo cliente se não existir
#     if not cliente:
#         collection.insert_one({
#             "cpf": cpf,
#             # "dados_cliente": cliente_dados,
#             "conversas": [
#                 {
#                     "assunto": assunto,
#                     "chats": [
#                         {
#                             "data_hora_inicio": dt_hr_ini,
#                             "mensagens": []
#                         }
#                     ]
#                 }
#             ]
#         })
#     else:
#         # Inserir nova conversa caso o cliente já existir na base
#         collection.update_one(
#             {"cpf": cpf},
#             {"$push": {
#                 "conversas": {
#                     "assunto": assunto,
#                     "chats": [
#                         {
#                             "data_hora_inicio": dt_hr_ini,
#                             "mensagens": []
#                         }
#                     ]
#                 }
#             }}
#         )
# Função para inserir uma mensagem em uma conversa existente ou nova
# Essa função assume sempre a premissa de que o CPF já foi criado na base
def inserir_mensagem(cpf, assunto, dt_hr_ini, dict_mensagem):
    client, db, collection = conectar_mongo()  # Conectar ao banco de dados
    collection.update_one(
        {"cpf": cpf},
        {"$push": {"conversas.$[conversa].chats.$[chat].mensagens": dict_mensagem}},
        array_filters=[
            {"conversa.assunto": assunto},
            {"chat.data_hora_inicio": dt_hr_ini}
        ]
    )
# def inserir_mensagem(cpf, assunto, dt_hr_ini, mensagem):
#     client, db, collection = conexao_mongo()  # Conectar ao banco de dados
#     cliente = collection.find_one({"cpf": cpf})    
#     # Atualizar para o assunto e data_hora_inicio específicos
#     collection.update_one(
#         {"cpf": cpf, "conversas.assunto": assunto, "conversas.chat.data_hora_inicio": dt_hr_ini},
#         {"$push": {"conversas.$.chat.$[elem].mensagens": mensagem}},
#         array_filters=[{"elem.data_hora_inicio": dt_hr_ini}]
#     )
    
# cpf = "123.456.789-00"
# cliente_dados = {
#     "nome": "Carlos Silva",
#     "email": "carlos.silva@example.com",
#     "telefone": "(11) 1234-5678"
# }

# assunto = "Status do Pedido"
# dt_hr_ini = "2024-06-01 12:42"
# mensagem1 = {
#     "data": "2024-06-01",
#     "hora": "12h42",
#     "mensagem_cliente": "bom dia",
#     "sugestao_ia": "bom dia, sr.",
#     "resposta_final": "bom dia, sr. Carlos",
#     "rating": "4. Boa Resposta"
# }

# mensagem2 = {
#     "data": "2024-06-01",
#     "hora": "14h15",
#     "mensagem_cliente": "qual o status do meu pedido?",
#     "sugestao_ia": "Seu pedido está a caminho.",
#     "resposta_final": "Seu pedido está a caminho e deve chegar até o fim do dia.",
#     "rating": "5. Excelente"
# }

# # Passo 1: Inserir os dados do cliente com um assunto inicial e uma mensagem
# inserir_cliente(cpf, assunto, dt_hr_ini, cliente_dados)

# # Passo 2: Appendar o primeiro bloco de mensagem
# inserir_mensagem(cpf, assunto, dt_hr_ini, mensagem1)

# # Passo 3: Appendar o segundo bloco de mensagem
# inserir_mensagem(cpf, assunto, dt_hr_ini, mensagem2)
