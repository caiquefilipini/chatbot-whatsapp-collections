from pymongo import MongoClient
from conexoes import ConexaoMongo
import streamlit as st

class SaveData:
    """ Classe para salvar as conversas no banco de dados MongoDB.
    Attributes:
        client (MongoClient): Cliente de conexão ao MongoDB.
        db (Database): Instância do banco de dados do MongoDB.
        collection (Collection): Coleção específica dentro do banco de dados para operações.
        cpf (int): CPF do cliente.
        assunto (str): Assunto da conversa.
        data_hora_inicio (str): Data e hora de início da conversa.
    """

    def __init__(self):
        self.client, self.db, self.collection = ConexaoMongo().conectar_mongo()
        self.cpf = st.session_state["cpf"]
        self.assunto = st.session_state["assunto"] 
        self.data_hora_inicio = st.session_state["data_hora_inicio"]

    def inserir_cliente(self):
        """ Insere um novo cliente no banco de dados MongoDB. """
        
        # Verifica se o cliente já existe na base
        cliente = self.collection.find_one({"cpf": self.cpf})

        # Insere novo cliente se não existir
        if not cliente:
            self.collection.insert_one({
                "cpf": self.cpf,
                "conversas": [
                    {
                        "assunto": self.assunto,
                        "chats": [
                            {
                                "data_hora_inicio": self.data_hora_inicio,
                                "mensagens": []
                            }
                        ]
                    }
                ]
            })
        else:
            # Inserir nova conversa caso o cliente já existir na base, mas não com o assunto atual
            assunto_existe = self.collection.find_one({"cpf": self.cpf, "conversas.assunto": self.assunto})
            if not assunto_existe:
                print("assunto novo")
                # Adicionar um novo assunto com o chat inicial
                self.collection.update_one(
                    {"cpf": self.cpf},
                    {"$push": {
                        "conversas": {
                            "assunto": self.assunto,
                            "chats": [
                                {
                                    "data_hora_inicio": self.data_hora_inicio,
                                    "mensagens": []
                                }
                            ]
                        }
                    }}
                )
            else:
                # Adicionar um novo chat ao assunto existente
                self.collection.update_one(
                    {"cpf": self.cpf, "conversas.assunto": self.assunto},
                    {"$push": {
                        "conversas.$.chats": {
                            "data_hora_inicio": self.data_hora_inicio,
                            "mensagens": []
                        }
                    }}
                )


    def inserir_mensagem(self, dict_mensagem):
        """Insere uma nova mensagem no banco de dados MongoDB."""

        self.collection.update_one(
            {"cpf": self.cpf},
            {"$push": {"conversas.$[conversa].chats.$[chat].mensagens": dict_mensagem}},
            array_filters=[
                {"conversa.assunto": self.assunto},
                {"chat.data_hora_inicio": self.data_hora_inicio}
            ]
        )