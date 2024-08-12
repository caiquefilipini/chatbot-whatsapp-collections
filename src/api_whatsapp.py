import requests
import json
from flask import Flask, request, jsonify
from datetime import datetime
from pymongo import MongoClient


# Variável global para armazenar a conexão
collection = None

def get_mongo_collection():
    global collection
    if collection is None:
        # Estabelece a conexão apenas se ainda não estiver conectada
        client = MongoClient('mongodb://localhost:27017/')
        db = client["whatsapp"]
        collection = db["messages"]
    return collection


# Fluxo
# tratar exceções, validar dados recebidos e segurança na comunicação.


app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(data)

    # Processa a mensagem
    resposta = processa_mensagem(data)

    # Enviar a resposta
    # envia_resposta(telefone, resposta)

    return jsonify({"status": "success"}), 200



def processa_mensagem(data):
    # Extrai as informações da mensagem
    numero = data['data']['key']['remoteJid'].split('@')[0]
    try:
        mensagem = data['data']['message']['conversation']
    except KeyError:
        mensagem = data['data']['message']['extendedTextMessage']['text']
    data_hora = datetime.fromtimestamp(data['data']['messageTimestamp']).strftime('%Y-%m-%d - %H:%M')
    formato = "texto" if data['data']['messageType'].isin("conversation", "extendedTextMessage") else "nao_texto"
    chat = {
        "mensagem": mensagem,
        "data_hora": data_hora,
        "formato": formato,
        "tipo": "recebida"
    }
    
    # Armazena a mensagem no banco de dados
    collection = get_mongo_collection()
    numero_existente = collection.find_one({"numero": numero})
    if numero_existente:
        collection.update_one({"numero": numero}, {"$push": {"chat": chat}})
    else:
        collection.insert_one({
            "numero": numero,
            "matricula_autenticada": 0, # Para teste no banco
            "conversa_ativa": 1, # Para teste no banco
            "nome_usuario": "",
            "chat": [chat]
        })

    # Carrega o histórico de mensagens
    historico = collection.find_one({"numero": numero})

    # status_chat = 
        # inicio_geral
        # autenticacao_matricula
        # autenticacao_cpf_cliente
        # autenticacao_data_nascimento
        # inicio_chat
        # chat_ativo
            # reportar
            # ajuda
        # encerrar_chat / reiniciar_chat




    # Faz algumas verificações
        # Se é início de conversa
        # Se é uma tentativa de autenticação
        # Se encotra a matrícula
        # Se encontra o CPF
        # Se a data de nascimento é válida
        # Se cliente está autenticado
        # Formato da mensagem
        # Se é uma mensagem válida
        # Se é um comando (#encerrar, #ajuda, #sair, #cancelar)
        # Etc

    # Gera uma resposta
    # resposta = define_resposta(mensagem)
    # Armazena as mensagens enviadas

    # Informações relevantes:

    # data e hora da mensagem
    # data e hora da mensagem anterior
    # histórico de mensagens --> banco de dados temporário para acesso mais rápido durante a conversa
    # matrícula
    # cliente (CPF)

    # é primeira mensagem?

    # tentativa de autenticação


#  https://a7c4-189-97-90-110.ngrok-free.app/webhook

    # Adicione sua lógica de processamento de mensagem aqui
    # return "Olá, recebemos sua mensagem: " + mensagem





def define_resposta(mensagem):
    # bot_response(mensagem)
    resposta = "*Como* _posso_ ```ajudá-lo```? 🚀.\n\nAss.: Sander."
    return resposta



def envia_resposta(telefone, resposta):

    url = "http://localhost:8080/message/sendText/NegociaAI_v2"

    headers = {
        "Content-Type": "application/json",
        "apikey": "7ij3826ys3glsr95hej01"
    }

    json_resposta = {
        "number": telefone,
        "options": {
            "delay": 1200,
            "presence": "composing",
            "linkPreview": False
        },
        "textMessage": {
            "text": f"{resposta}"
        }
    }

    response = requests.post(url, headers=headers, json=json_resposta)




if __name__ == "__main__":
    app.run(port=5000)






    # data = request.get_json()
    # print("Dados recebidos:", data)  # Isso ajudará a ver a estrutura dos dados

    # # Acessando a mensagem aninhada
    # try:
    #     message = data["data"]["message"]["conversation"]
    #     print("Mensagem recebida:", message)
    #     return jsonify({"status": "received", "message": message}), 200
    # except KeyError as e:
    #     print("Erro ao acessar uma chave:", e)
    #     return jsonify({"error": "Chave não encontrada", "details": str(e)}), 400

    # Processa a mensagem recebida
    # response_message = process_message(message)

    # Envia a resposta
    # send_message(sender, response_message)

    # return jsonify({"status": "success"}), 200


# def process_message(message):
#     # Adicione sua lógica de processamento de mensagem aqui
#     return "Olá, recebemos sua mensagem: " + message