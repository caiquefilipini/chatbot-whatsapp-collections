
import os
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def hello():
    return "Hello, Flask!"

@app.route("/consultar_cpf", methods=["POST"])
def consultar_cpf(cpf="72388905850"):
    """
    Verifica se o CPF existe no banco de dados e, se sim,
    retorna o nome, o CPF e a data de nascimento do cliente.
    
    Args:
    cpf (str): CPF do cliente.
    
    Returns:
    list: Lista com as conversas associadas ao CPF.
    """
    try:

        # Carrega o CPF do corpo da requisição
        data = request.get_json()

        # Remove os pontos e traços do CPF
        cpf = cpf.replace(".", "").replace("-", "")

        # Carrega o banco de dados
        abs_path_file = os.path.abspath(__file__)
        abs_path_dir = os.path.dirname(abs_path_file)
        abs_path = os.path.dirname(abs_path_dir)
        file_customer_path = os.path.join(abs_path, "data", "base_clientes_excel.xlsx")
        consulta_cliente = pd.read_excel(file_customer_path)
        consulta_cliente = consulta_cliente[consulta_cliente["cpf"] == int(cpf)]

        if consulta_cliente.empty:
            return jsonify({"erro": "CPF não encontrado no banco de dados."}), 404

        dados_cliente = {
            "nome": consulta_cliente["nome"].values[0],
            "primeiro_nome": consulta_cliente["nome"].values[0].split(" ")[0],
            "data_nascimento": consulta_cliente["data_nascimento"].values[0].astype("M8[D]").astype(datetime).strftime("%d-%m-%Y"), # .astype(datetime),
        }

        return jsonify(dados_cliente)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# app.run(host="0.0.0.0")



if __name__ == '__main__':
    app.run(debug=True)

# # Endpoint to create a new guide
# @app.route('/guide', methods=["POST"])
# def add_guide():
#     title = request.json['title']


# print(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "base_clientes.xlsx"))