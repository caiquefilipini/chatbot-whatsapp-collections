import requests
import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify
from datetime import datetime
from pymongo import MongoClient
import pandas as pd
from dateutil import parser
import openai

collection = None

load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

global DATA_PATH 
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")

global base_clientes
base_clientes = pd.read_excel(os.path.join(DATA_PATH, "base_clientes_excel.xlsx"), engine="openpyxl")

def get_mongo_collection():
    global collection, telefones_teste
    if collection is None:
        # Estabelece a conexão apenas se ainda não estiver conectada
        client = MongoClient('mongodb://localhost:27017/')
        db = client["whatsapp"]
        collection = db["messages"]
        telefones_teste = db["matriculas"]
    return collection, telefones_teste


app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():

    # Captura a mensagem recebida
    data = request.get_json()
    # print(data)

    # Processa a mensagem
    retorno = processa_mensagem(data)

    # Enviar a resposta
    envia_resposta(retorno["telefone"], retorno["resposta"])

    return jsonify({"status": "success"}), 200


def _carregar_ofertas(cpf):
    ofertas = pd.read_excel(os.path.join(DATA_PATH, "ofertas.xlsx"), engine="openpyxl")
    ofertas = ofertas.query("CPF == @cpf")

    cols_a_vista = [
        "Valor de Entrada ou à Vista",
        "Desconto Concedido"
    ]

    cols_parcelado = [
        "Valor de Entrada ou à Vista",
        "Quantidade de Parcelas",
        "Valor da Parcela",
        "Taxa de Juros (am)",
        "Taxa CET",
        "Desconto Concedido"
    ]

    ofertas_a_vista = ofertas[ofertas['Tipo de Oferta'] == 'À Vista'][cols_a_vista].rename(columns={"Valor de Entrada ou à Vista": "valor", "Desconto Concedido": "desconto"}).to_dict(orient='records')
    ofertas_parcelado = ofertas[ofertas['Tipo de Oferta'] == 'Parcelado'][cols_parcelado].rename(columns={"Valor de Entrada ou à Vista": "valor", "Quantidade de Parcelas": "parcelas", "Valor da Parcela": "valor_parcela", "Taxa de Juros (am)": "taxa_juros", "Taxa CET": "taxa_cet", "Desconto Concedido": "desconto"}).to_dict(orient='records')

    relacao_ofertas = {
        'Ofertas À Vista': ofertas_a_vista,
        'Ofertas Parcelado': ofertas_parcelado
    }

    return relacao_ofertas


# Função para carregar o prompt
def _carrega_prompt(dados_cliente, ofertas_disponiveis):
    PROMPT_FILE = os.path.join(os.path.dirname(__file__), "prompts", "prompt_negociacao.txt")
    with open(PROMPT_FILE, "r", encoding="utf-8") as file:
        return file.read().format(
            dados_cliente=dados_cliente, 
            ofertas_disponiveis=ofertas_disponiveis
        )
    

def processa_mensagem(data):
    # Extrai as informações da mensagem
    numero = data['data']['key']['remoteJid'].split('@')[0]
    try:
        mensagem = data['data']['message']['conversation']
    except KeyError:
        mensagem = data['data']['message']['extendedTextMessage']['text']
    data_hora_recebida = datetime.fromtimestamp(data['data']['messageTimestamp']).strftime('%Y-%m-%d - %H:%M')
    formato = "texto" if data['data']['messageType'] in ["conversation", "extendedTextMessage"] else "nao_texto"
    # chat = {
    #     "mensagem": mensagem,
    #     "data_hora": data_hora,
    #     "tipo": "recebida"
    # }

    if formato != "texto":
        return {"telefone": numero, "resposta": "Desculpe, ainda não aprendi a entender mensagens em formatos diferentes de texto."}
    
    else:
        # Armazena a mensagem no banco de dados
        collection, telefones_teste = get_mongo_collection()
        historico = collection.find_one({"numero": numero})
        if historico:
            # collection.update_one({"numero": numero}, {"$push": {"chat": chat}})
            pass
        else:
            collection.insert_one({
                "numero": numero,
                "cpf": 0,
                "data_nascimento": "",
                "primeiro_nome": "",
                "primeira_mensagem": 1,
                "autenticar_matricula": 0,
                "escolher_cliente": 0,
                "comecar_negociacao": 0,
                "autenticar_cpf": 0,
                "autenticar_data_nascimento": 0,
                "inicio_chatbot": 0,
                "reportar_problema": 0,
                "nome_usuario": "",
                "chat": []
                # "chat": [chat]
            })

        # Carrega o histórico de mensagens
        historico = collection.find_one({"numero": numero})

        #encerrar, #iniciar, #ajuda, #report
        # Verifica se é um comando
        if mensagem in ["#encerrar", "#iniciar", "#ajuda", "#reportar", "#continuar"]:

            if mensagem == "#encerrar":
                collection.delete_one({"numero": numero})
                return {"telefone": numero, "resposta": "A conversa foi encerrada. Para iniciar uma nova conversa, envie qualquer mensagem."}
            
            if mensagem == "#iniciar":
                collection.delete_one({"numero": numero})
                return {"telefone": numero, "resposta": "A conversa foi encerrada. Para iniciar uma nova conversa, envie qualquer mensagem."}
            
            if mensagem == "#ajuda":
                resposta = """Opaaa... parece que você precisa de ajuda! 🆘

Seguem algumas informações importantes para você:

- O objetivo desse teste interno é simular uma negociação de dívida com um cliente fictício.
- Você representa o cliente e eu vou representando o atendente.
- Fique à vontade para criar situações diferentes na conversa.
- Lembre-se: Agora, nosso objetivo não é fazer dar tudo certo, mas sim avaliar como eu me sairia em diferentes situações de uma conversa real com o cliente.
- Ou seja, você pode testar o que quiser, sem medo de errar! O momento de errar é agora 😄
- A qualquer momento da conversa você pode digitar alguns comandos especiais:
    - #iniciar: inicia um chat novo
    - #encerrar: encerra a conversa
    - #ajuda: exibe essa mensagem que você está lendo agora 😂
    - #reportar: reporta alguma problema

Espero ter ajudado! 😊

Para continuar a conversa, envie uma mensagem sobre a negociação.
"""
                return {"telefone": numero, "resposta": resposta}
            
            if mensagem == "#reportar":
                resposta = """Hmm... Entendi que você quer reportar algo 🤔

Vou considerar sua próxima mensagem como um report e enviar ao time de Advanced Analytics. Por favor, digite o que deseja reportar.
"""
                collection.update_one({"numero": numero}, {"$set": {"reportar_problema": 1}})
                return {"telefone": numero, "resposta": resposta}
            
            # if mensagem == "#continuar":
            #     resposta = """Ok, vamos continuar a conversa. Assuma novamente o papel do cliente enviando uma mensagem sobre a negociação."""

            #     return {"telefone": numero, "resposta": resposta}
            
        else:
            historico = collection.find_one({"numero": numero})
            

        if historico["reportar_problema"]:
            resposta = f"""Show... Enviei seu report para o time de Advanced Analytics avaliar. Obrigado por reportar o problema! 😊
            
Agora, você pode voltar ao papel do cliente e continuar a conversa normalmente.
"""
            collection.update_one({"numero": numero}, {"$set": {"reportar_problema": 0}})
            return {"telefone": numero, "resposta": resposta}


        if historico["primeira_mensagem"]:

            # Verifica se o número já enviou alguma mensagem antes
            historio_telefone = telefones_teste.find_one({"numero": numero})
            if historio_telefone:
                collection.update_one(
                    {"numero": numero},
                    {"$set": {"primeira_mensagem": 0, "escolher_cliente": 1, "nome_usuario": historio_telefone["nome_usuario"]}}
                )

                resposta = f"""Olá de novo, {historio_telefone["nome_usuario"]}!

Como já nos conhecemos antes, entendo que você já sabe como funciona esse teste. 😄

Mas se precisar refrescar a memória, é só digitar #ajuda que eu te passo novamente as orientações sobre esse teste, ok?

Para fazer um novo teste com um cliente fictício, escolha uma das opções abaixo:

1. Escolher um cliente fictício específico da planilha.
2. Escolha um cliente fictício aleatório para mim.

Digite o número correspondente à sua escolha.
"""
                return {"telefone": numero, "resposta": resposta}


            resposta = """Olá! Muito prazer, me chamo Sander. Sou o novo bot inteligente do Negocia AI, um projeto de Inteligência Artificial desenvolvido pelo time de Advanced Analytics de Recuperações! Nesse momento, estou sendo treinado para negociar dívidas direto com o cliente. 

Essa é uma etapa de teste interno, com objetivo de avaliar como eu me sairia numa conversa real com um cliente. Para isso, vamos simular uma negociação com dados de algum cliente fictício, ok?

Mas antes de começar a testar, preciso que me informe o número da sua matrícula...
"""
            collection.update_one({"numero": numero}, {"$set": {"primeira_mensagem": 0, "autenticar_matricula": 1}})
            return {"telefone": numero, "resposta": resposta}

        if historico["autenticar_matricula"]:

            base_matriculas = pd.read_excel(os.path.join(DATA_PATH, "matriculas.xlsx"), engine="openpyxl")
            try:
            # matricula_informada = int(str(mensagem).replace(" ", "").replace(".", "").replace("-", "").replace("/", "").replace("T", "")) # forçar virar um número
                matricula_informada = int(str(mensagem).replace(" ", "").replace(".", "").replace("-", "").replace("/", "").replace("T", "")) # forçar virar um número
            except:
                matricula_informada = 0

            if matricula_informada not in base_matriculas["matricula"].values:
                resposta = f"""Desculpe, não consegui encontrar sua matrícula em nossa base de dados. 😢
                
Por favor, verifique se digitou corretamente e tente novamente.
            
Se mesmo assim não der certo, peça para o time de Advanced Analytics de Recuperações adicionar sua matrícula na base de usuários habilitados para teste.
"""
                return {"telefone": numero, "resposta": resposta}
            else:    
                primeiro_nome_usuario = base_matriculas.query("matricula == @matricula_informada")["nome"].values[0].split(" ")[0]
                resposta = f"""Que honra te ver por aqui, {primeiro_nome_usuario}! 🚀
                
Vou te explicar como esse teste vai funcionar:

1. Vamos simular uma negociação de dívida com um cliente fictício.
2. Você vai representar o cliente e eu vou representar o atendente.
4. Vamos tentar chegar a um acordo que seja bom para ambas as partes.
5. A qualquer momento da conversa você pode digitar alguns comandos especiais, como:
    - #iniciar: inicia um chat novo
    - #encerrar: para encerrar a conversa
    - #ajuda: exibe as orientações sobre esse teste
    - #reportar: reporta alguma problema

Agora, você precisa escolher um cliente fictício para simular a negociação. 🤝

O que você prefere: 
1. Escolher um cliente fictício específico da planilha? Ou...
2. Quer que eu escolha um cliente fictício aleatório para você?

Digite o número correspondente à sua escolha.
"""
            collection.update_one(
                {"numero": numero},
                {"$set": {"nome_usuario": primeiro_nome_usuario, "autenticar_matricula": 0, "escolher_cliente": 1}})
            telefones_teste.insert_one({"numero": numero, "nome_usuario": primeiro_nome_usuario})
            return {"telefone": numero, "resposta": resposta}

        if historico["escolher_cliente"]:
            if mensagem == "1":
                resposta = """Ótimo! Então assim que estiver pronto, me avise digitando #ja"""
                collection.update_one({"numero": numero}, {"$set": {"escolher_cliente": 0, "comecar_negociacao": 1}})
                return {"telefone": numero, "resposta": resposta}

            elif mensagem == "2":
                # base_clientes = pd.read_excel(os.path.join(DATA_PATH, "base_clientes_excel.xlsx"), engine="openpyxl")
                cliente_aleatorio = base_clientes.sample(1).iloc[0]

                nome = cliente_aleatorio["nome"]
                cpf = cliente_aleatorio["cpf"]
                segmento = cliente_aleatorio["segmento"]
                genero = cliente_aleatorio["genero"]
                prob_rolagem = cliente_aleatorio["prob_rolagem"]
                data_nascimento = cliente_aleatorio["data_nascimento"].strftime('%Y-%m-%d')
                produto = cliente_aleatorio["produto"]
                numero_contrato = cliente_aleatorio["nro_contrato"]
                valor_divida = cliente_aleatorio["vlr_divida"]
                dias_atraso = cliente_aleatorio["dias_atraso"]
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

Assim que estiver pronto, me avise digitando #ja
"""
                collection.update_one({"numero": numero}, {"$set": {"escolher_cliente": 0, "comecar_negociacao": 1}})
                return {"telefone": numero, "resposta": resposta}
            else:
                resposta = """Desculpe, não entendi o que você quis dizer. 🤔
    Digite o número referente a uma das opções disponíveis:
    1. Quero escolher um cliente fictício específico da planilha.
    2. Escolha para mim um cliente fictício aleatório.

    Se você digitar 1, você poderá escolher qualquer cliente fictício específico da planilha que o time de Advanced Analytics passou.

    Se você digitar 2, eu mesmo escolherei um cliente fictício aleatório para você.
    """
                return {"telefone": numero, "resposta": resposta}
        

        if historico["comecar_negociacao"]:
            if mensagem == "#ja":
                resposta = """Show... então vamos começar! 🚀
                
Incorporando o personagem 🧘‍♂️... Foi!

---

Olá, meu nome é Sander, sou o novo bot inteligente do Santander. Fui treinado para ajudar você a negociar suas dívidas e organizar sua vida financeira.
            
Para sua segurança, preciso que me informe o número do seu CPF.
"""
                collection.update_one({"numero": numero}, {"$set": {"comecar_negociacao": 0, "autenticar_cpf": 1}})
                return {"telefone": numero, "resposta": resposta}
            else:
                resposta = """Desculpe, não entendi o que você quis dizer. 🤔
Assim que estiver pronto, me avise digitando #ja
"""
                return {"telefone": numero, "resposta": resposta}

        if historico["autenticar_cpf"]:
            # base_clientes = pd.read_excel(os.path.join(DATA_PATH, "base_clientes_excel.xlsx"), engine="openpyxl")
            cpf_informado = int(str(mensagem).replace(" ", "").replace(".", "").replace("-", "").replace("/", ""))
        
            if cpf_informado not in base_clientes["cpf"].values:
                resposta = f"""Desculpe, não consegui encontrar seu CPF em nossa base de dados. 😢

Verifique se digitou corretamente e tente novamente.
"""
                return {"telefone": numero, "resposta": resposta}
            else:
                # global info_cliente
                # info_cliente = base_clientes.query("cpf == @cpf_informado")
                data_nascimento_cliente = parser.parse(str(base_clientes.query("cpf == @cpf_informado")["data_nascimento"].values[0])).strftime('%Y-%m-%d')
                primeiro_nome_cliente = base_clientes.query("cpf == @cpf_informado")["nome"].values[0].split(" ")[0]
                # dados_cliente["primeiro_nome"] = primeiro_nome_cliente
                resposta = f"""Ótimo, {primeiro_nome_cliente}! Consegui localizar aqui. Agora preciso que me informe sua data de nascimento."""
                collection.update_one({"numero": numero}, {"$set": {"cpf": cpf_informado, "data_nascimento": data_nascimento_cliente, "primeiro_nome": primeiro_nome_cliente, "autenticar_cpf": 0, "autenticar_data_nascimento": 1}})
                return {"telefone": numero, "resposta": resposta}
        if historico["autenticar_data_nascimento"]:
            try:
                data_nascimento_informada = parser.parse(str(mensagem)).strftime('%Y-%m-%d')
            except:
                resposta = f"""Desculpe, não consegui entender a data de nascimento informada. 😢"""
                return {"telefone": numero, "resposta": resposta} 
            # print(data_nascimento_informada, dados_cliente["data_nascimento"].values[0])
            
            if data_nascimento_informada != historico["data_nascimento"]:
                resposta = f"""Desculpe, a data de nascimento informada não confere com a data de nascimento cadastrada em nosso sistema. 😢
Por favor, verifique se digitou corretamente e tente novamente.
"""
                return {"telefone": numero, "resposta": resposta}
            else:
                resposta = f"""Perfeito, {historico["primeiro_nome"]}! Seus dados foram validados com sucesso 🚀
Me conta, o que posso fazer por você hoje? ♨️
"""
                collection.update_one({"numero": numero}, {"$set": {"cpf": historico["cpf"], "autenticar_data_nascimento": 0, "inicio_chatbot": 1}})
                return {"telefone": numero, "resposta": resposta}

        if historico["inicio_chatbot"]:
            cpf_cliente = historico["cpf"]
            dados_cliente = base_clientes.drop("dt_ref", axis=1).query("cpf == @cpf_cliente").to_dict(orient="records")[0]
            dados_cliente["data_nascimento"] = dados_cliente["data_nascimento"].strftime("%Y-%m-%d")
            
            ofertas_disponiveis = _carregar_ofertas(cpf_cliente)
            mensagens_anteriores = [i for i in historico["chat"]]

            prompt = _carrega_prompt(dados_cliente, ofertas_disponiveis)
            
            param_messages = mensagens_anteriores.copy()
            param_messages.append({"role": "system", "content": prompt})
            param_messages.append({"role": "user", "content": mensagem})

            resposta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=param_messages
            )['choices'][0]['message']['content']

            mensagem_recebida = {
                "role": "user",
                "content": mensagem,
                # "data_hora": data_hora_recebida,
            }

            mensagem_resposta = {
                "role": "assistant",
                "content": resposta,
                # "data_hora": datetime.now().strftime('%Y-%m-%d - %H:%M'),
            }

            collection.update_one(
                {"numero": numero},
                {"$push": {"chat": {"$each": [mensagem_recebida, mensagem_resposta]}}}
            )
            return {"telefone": numero, "resposta": resposta}




# Função para enviar resposta
def envia_resposta(telefone, resposta):

    url = "http://localhost:8080/message/sendText/NegociaAI"

    headers = {
        "Content-Type": "application/json",
        "apikey": "i5v3b75srig1582t6dcof6" # Cuidado para colocar a chave correta
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

# Dúvida: e se tiver muitas mensagens simultaneamente? Vai dar problema?
#    # Verificar como colocar as mensagens em uma fila de processamento para evitar problemas

# Implantar reset de chat (começar do zero)
#   # Autentica matrícula de novo? Se não, manter banco de dados telefone/matrícula autenticada?
#   # No outro dia, força começar do zero?
#   # Explica tudo de novo?
#   # Etc.
#     # Implantar limite de tentativas para autenticação
#     # Implantar limite de interações na parte do chatbot (mensagem informativa dizendo que o limite diário de interações para aquele número de telefone foi atingido)