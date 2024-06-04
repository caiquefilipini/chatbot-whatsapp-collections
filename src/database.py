import sqlite3
import json

# Função para conectar ao banco de dados
def get_connection():
    conn = sqlite3.connect('conversas.db')
    return conn

# Função para criar a tabela se não existir
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT,
            history TEXT,
            ratings TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Função para salvar uma conversa no banco de dados
def save_conversation(cpf, history, ratings):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO conversas (cpf, history, ratings)
        VALUES (?, ?, ?)
    ''', (cpf, json.dumps(history), json.dumps(ratings)))
    conn.commit()
    conn.close()

# Função para carregar todas as conversas do banco de dados
def load_conversations():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT cpf, history, ratings FROM conversas')
    rows = cursor.fetchall()
    conn.close()
    conversations = {}
    for row in rows:
        cpf, history, ratings = row
        conversations[cpf] = {
            'history': json.loads(history),
            'ratings': json.loads(ratings)
        }
    return conversations
