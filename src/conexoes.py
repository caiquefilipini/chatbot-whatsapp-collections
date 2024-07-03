from pymongo import MongoClient, errors

class ConexaoMongo:
    def conectar_mongo(self):
        # Verifica se a conexão já foi criada
        if not hasattr(self.conectar_mongo, "collection"):
            try:
                # Se não, cria uma nova conexão
                self.conectar_mongo.client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
                self.conectar_mongo.client.server_info()  # Tenta obter informações do servidor para testar a conexão
                self.conectar_mongo.db = self.conectar_mongo.client["db_conversas"]
                self.conectar_mongo.collection = self.conectar_mongo.db["clientes_conversas"]
            except Exception as e:
                print(f"Erro ao conectar ao MongoDB: {e}")
                self.conectar_mongo.client = None
                return None

        return self.conectar_mongo.client, self.conectar_mongo.db, self.conectar_mongo.collection

    def close(self):
        """Fecha a conexão com o MongoDB."""
        self.client.close()