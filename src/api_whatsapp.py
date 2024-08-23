import requests
import json
from flask import Flask, request, jsonify
from datetime import datetime
from pymongo import MongoClient
import pandas as pd

collection = None

def get_mongo_collection():
    global collection
    if collection is None:
        # Estabelece a conexão apenas se ainda não estiver conectada
        client = MongoClient('mongodb://localhost:27017/')
        db = client["whatsapp"]
        collection = db["messages"]
    return collection



app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()
    # print(data)

    # Processa a mensagem
    retorno = processa_mensagem(data)

    # Enviar a resposta
    envia_resposta(telefone, resposta)

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
            "primeira_mensagem": 1,
            "autenticar_matricula": 0,
            "comecar_negociacao": 0,
            "autenticar_cpf": 0,
            "autenticar_data_nascimento": 0,
            "conversa_ativa": 0,
            "nome_usuario": "",
            "chat": [chat]
        })

    # Carrega o histórico de mensagens
    historico = collection.find_one({"numero": numero})

    if historico["primeira_mensagem"]:
        resposta = """Olá! Muito prazer, me chamo Sander. Sou o novo bot inteligente do Negocia AI, um projeto de Inteligência Artificial desenvolvido pelo time de Advanced Analytics de Recuperações! Nesse momento, estou sendo treinado para negociar dívidas direto com o cliente. 

Essa é uma etapa de teste interno, com objetivo de avaliar como eu me sairia numa conversa real com um cliente. Para isso, vamos simular uma negociação com dados de algum cliente fictício, ok?

Mas antes de começar a testar, preciso que me informe o número da sua matrícula...
        """
        collection.update_one({"numero": numero}, {"$set": {"primeira_mensagem": 0, "autenticar_matricula": 1}})


    if historico["autenticar_matricula"]:

        base_matriculas = pd.read_excel("matriculas.xlsx", engine="openpyxl")
        matricula_informada = int(str(mensagem).replace(" ", "").replace(".", "").replace("-", "").replace("/", "").replace("T", ""))
        primeiro_nome_usuario = base_matriculas.query("matricula == @matricula_informada")["nome"].values[0].split(" ")[0]

        if matricula_informada not in base_matriculas["matricula"].values:
            resposta = f"""Desculpe, não consegui encontrar sua matrícula em nossa base de dados. 😢
            
Por favor, verifique se digitou corretamente e tente novamente.
            
Se mesmo assim não der certo, peça para o time de Advanced Analytics de Recuperações adicionar sua matrícula na base de usuários habilitados para teste."""

        else:    
            resposta = f"""Que honra te ver por aqui, {primeiro_nome_usuario}! 🚀
            
Vou te explicar como esse teste vai funcionar:

1. Vamos simular uma negociação de dívida com um cliente fictício.
2. Você vai representar o cliente e eu vou representar o atendente.
3. Vou te passar as informações do cliente e você vai me ajudar a negociar a dívida.
4. Vamos tentar chegar a um acordo que seja bom para ambas as partes.
5. A qualquer momento da conversa você pode digitar alguns comandos especiais, como #ajuda, #encerrar, #sair, #cancelar.
    - #ajuda: para receber informações sobre os comandos disponíveis.
    - #encerrar: para encerrar a conversa.
    - #sair: para sair da negociação e reiniciar o chat.
    - #cancelar: para cancelar a última ação realizada.
6. Quando estiver pronto para começar, me avise digitando #começar.

Agora, você precisa escolher um cliente fictício para simular a negociação. 🤝

Você prefere: 
1. Escolher um cliente fictício específico da planilha?
2. Quer que eu escolha um cliente fictício aleatório para você?

Digite o número correspondente à sua escolha.
"""
        collection.update_one({"numero": numero}, {"$set": {"autenticar_matricula": 0, "escolher_cliente": 1}})


    if historico["escolher_cliente"]:
        if mensagem == "1":
            resposta = """Ótimo! Então assim que estiver pronto, me avise digitando #começar."""
            collection.update_one({"numero": numero}, {"$set": {"escolher_cliente": 0, "comecar_negociacao": 1}})

        elif mensagem == "2":
            base_clientes = pd.read_excel("base_clientes_excel.xlsx", engine="openpyxl")
            cliente_aleatorio = base_clientes.sample(1).iloc[0]

            nome = cliente_aleatorio["nome"].values[0]
            cpf = cliente_aleatorio["cpf"].values[0]
            segmento = cliente_aleatorio["segmento"].values[0]
            genero = cliente_aleatorio["genero"].values[0]
            prob_rolagem = cliente_aleatorio["prob_rolagem"].values[0]
            data_nascimento = cliente_aleatorio["data_nascimento"].values[0]
            produto = cliente_aleatorio["produto"].values[0]
            numero_contrato = cliente_aleatorio["nro_contrato"].values[0]
            valor_divida = cliente_aleatorio["vlr_divida"].values[0]
            dias_atraso = cliente_aleatorio["dias_atraso"].values[0]

            resposta = f"""Beleza!
             
Então, você será o seguinte cliente fictício:
- Nome: {nome}
- CPF: {cpf}
- Segmento: {segmento}
- Gênero: {genero}
- Probabilidade de Rolagem: {prob_rolagem}
- Data de Nascimento: {data_nascimento}
- Produto: {produto}
- Número do Contrato: {numero_contrato}
- Dívida: R$ {valor_divida}
- Dias de Atraso: {dias_atraso}

Assim que estiver pronto, me avise digitando #começar.
"""
        collection.update_one({"numero": numero}, {"$set": {"escolher_cliente": 0, "comecar_negociacao": 1}})
    else:
        resposta = """Desculpe, não entendi o que você quis dizer. 🤔
Digite o número referente a uma das opções disponíveis:
1. Quero escolher um cliente fictício específico da planilha.
2. Escolha para mim um cliente fictício aleatório.

Se você digitar 1, você poderá escolher qualquer cliente fictício específico da planilha que o time de Advanced Analytics passou.

Se você digitar 2, eu mesmo escolherei um cliente fictício aleatório para você.
"""

    if historico["comecar_negociacao"]:
        if mensagem == "#começar":
            resposta = """Show... então vamos começar! 🚀

Incorporando o personagem 🧘‍♂️... Foi!

---

Olá, meu nome é Sander, sou o novo bot inteligente do Santander. Fui treinado para ajudar você a negociar suas dívidas e organizar sua vida financeira.
             
Para sua segurança, preciso que me informe o número do seu CPF.
"""
            collection.update_one({"numero": numero}, {"$set": {"comecar_negociacao": 0, "autenticar_cpf": 1}})
        else:
            resposta = """Desculpe, não entendi o que você quis dizer. 🤔
Assim que estiver pronto, me avise digitando #começar.
"""

    if historico["autenticar_cpf"]:
        base_clientes = pd.read_excel("base_clientes_excel.xlsx", engine="openpyxl")
        cpf_informado = str(mensagem).replace(" ", "").replace(".", "").replace("-", "").replace("/", "")
        primeiro_nome_cliente = base_clientes.query("cpf == @cpf_informado")["nome"].values[0].split(" ")[0]
        if cpf_informado not in base_clientes["cpf"].values:
            resposta = f"""Desculpe, não consegui encontrar seu CPF em nossa base de dados. 😢

Verifique se digitou corretamente e tente novamente.
"""
        else:
            resposta = f"""Ótimo, {primeiro_nome_cliente}! Consegui localizar aqui. Agora preciso que me informe sua data de nascimento."""
            collection.update_one({"numero": numero}, {"$set": {"autenticar_cpf": 0, "autenticar_data_nascimento": 1}})

    if historico["autenticar_data_nascimento"]:

        data_nascimento_informada = str(mensagem).strftime('%Y-%m-%d')
        data_nascimento_cliente = base_clientes.query("cpf == @cpf_informado")["data_nascimento"].values[0]

        if data_nascimento_informada != data_nascimento_cliente:
            resposta = f"""Desculpe, a data de nascimento informada não confere com a data de nascimento cadastrada em nosso sistema. 😢
Por favor, verifique se digitou corretamente e tente novamente.
"""
        else:
            resposta = f"""Perfeito, {primeiro_nome_cliente}! Seus dados foram validados com sucesso 🚀
Me conta, o que posso fazer por você hoje? ♨️
"""
            collection.update_one({"numero": numero}, {"$set": {"autenticar_data_nascimento": 0, "realizar_negociacao": 1}})


    if historico["realizar_negociacao"]:
        resposta = """bot_chat_gpt"""


# Função para enviar resposta
def envia_resposta(telefone, resposta):

    url = "http://localhost:8080/message/sendText/NegociaAI"

    headers = {
        "Content-Type": "application/json",
        "apikey": "7ij3826ys3glsr95hej01" # Corrigir
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
    app.run(debug=True, port=5000)


# Testar o que já foi feito!!!


# Implantar comandos
# comandos funcionam somente após início da negociação
#             # reportar
#             # ajuda
#         # encerrar_chat / reiniciar_chat


# Implantar validações
#         # Formato da mensagem (somente texto)
#         # Se é um comando (#encerrar, #ajuda, #sair, #cancelar)

#     # Informações relevantes:
#     # data e hora da mensagem
#     # data e hora da mensagem anterior
#     # histórico de mensagens --> banco de dados temporário para acesso mais rápido durante a conversa

# Guardar dados autenticados do cliente
# Dúvida: e se tiver muitas mensagens simultaneamente? Vai dar problema?
#    # Verificar como colocar as mensagens em uma fila de processamento para evitar problemas
# Armazenar mensagens enviadas
# Implantar reset de chat (começar do zero)
#   # Autentica matrícula de novo? Se não, manter banco de dados telefone/matrícula autenticada?
#   # No outro dia, força começar do zero?
#   # Explica tudo de novo?
#   # Etc.
#     # Implantar limite de tentativas para autenticação
#     # Implantar limite de interações na parte do chatbot (mensagem informativa dizendo que o limite diário de interações para aquele número de telefone foi atingido)


# #  https://a7c4-189-97-90-110.ngrok-free.app/webhook

# Função para enviar resposta
# def envia_resposta(telefone, resposta):

#     url = "http://localhost:8080/message/sendText/NegociaAI_v2"

#     headers = {
#         "Content-Type": "application/json",
#         "apikey": "7ij3826ys3glsr95hej01"
#     }

#     json_resposta = {
#         "number": telefone,
#         "options": {
#             "delay": 1200,
#             "presence": "composing",
#             "linkPreview": False
#         },
#         "textMessage": {
#             "text": f"{resposta}"
#         }
#     }

#     response = requests.post(url, headers=headers, json=json_resposta)











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
