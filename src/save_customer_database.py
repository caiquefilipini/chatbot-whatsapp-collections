# Libs
import pandas as pd
import sqlite3
import os

# Definir o caminho do arquivo CSV e do banco de dados
path = "../data/"

# Ler o arquivo CSV usando pandas
csv_file_path = os.path.join(path, "base_clientes.csv")
df = pd.read_csv(csv_file_path)

# Conectar-se (ou criar) ao banco de dados SQLite
conn = sqlite3.connect(os.path.join(path, 'customer_database.sqlite'))

# Salvar o DataFrame como uma tabela no banco de dados SQLite
df.to_sql("customer_database_table", conn, if_exists='replace', index=False)

# Fechar a conexão com o banco de dados
conn.close()

# Mensagem de sucesso
print("Arquivo CSV salvo como banco de dados SQLite com sucesso!")