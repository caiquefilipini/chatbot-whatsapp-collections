from pymongo import MongoClient, errors

class ConexaoMongo:
    def conectar_mongo(self):
        try:
            client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
            client.server_info()  # Gera uma exceção se não conseguir conectar
            print("Conexão com MongoDB bem-sucedida.")
            if client:
                db = client['db_conversas']
                collection = db['clientes_conversas']
            return client, db, collection
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")
            return None



        # Verifica se a conexão já foi criada
        # if not hasattr(self.conectar_mongo, "collection"):
        #     try:
        #         # Se não, cria uma nova conexão
        #         client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        #         client.server_info()  # Tenta obter informações do servidor para testar a conexão
        #         db = self.conectar_mongo.client["db_conversas"]
        #         collection = self.conectar_mongo.db["clientes_conversas"]
        #     except Exception as e:
        #         print(f"Erro ao conectar ao MongoDB: {e}")
        #         return None

        # return self.conectar_mongo.client, self.conectar_mongo.db, self.conectar_mongo.collection

    def close(self):
        """Fecha a conexão com o MongoDB."""
        self.client.close()