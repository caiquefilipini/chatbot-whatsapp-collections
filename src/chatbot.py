import langchain
# ...





# Resposta do chatbot
# Carregar histórico de interações
def bot_response(customer_message):
    if customer_message == "a":
        resposta = "Resposta padrão (igual a a)."
    else:
        resposta = "Resposta padrão (diferente de a)."
    return resposta