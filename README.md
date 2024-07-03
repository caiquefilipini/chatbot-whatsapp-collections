# 1. Introdução

O NegociaAI é um projeto voltado para a negociação de dívidas por meio de GenAI.

# 2. Instalação

## 2.1. Clone do Projeto

Esta etapa assume que você já tenha o git bash instalado na sua máquina.

Abra o seu terminal (bash) e execute o comando:
   ```bash
   git clone https://github.com/caiquefilipini/chatbot-whatsapp-collections.git
   ```

## 2.2. Instalação e Configuração do MongoDB

É necessário fazer a instalação e configuração do MongoDB na máquina/servidor que vai rodar a aplicação.

## 1. Instalação do MongoDB

### Windows

1. **Baixar o MongoDB**:
   - Vá para o [site oficial do MongoDB](https://www.mongodb.com/try/download/community) e baixe a versão adequada para o seu sistema operacional.

2. **Instalar**:
   - Execute o arquivo baixado (.msi) e siga as instruções de instalação. Durante a instalação, marque a opção para instalar o MongoDB como um serviço.

3. **Configuração do Path (opcional)**:
   - Adicione o diretório `bin` do MongoDB ao seu `PATH` para poder usar os comandos `mongo` e `mongod` de qualquer lugar no prompt de comando. O diretório geralmente é algo como `C:\Program Files\MongoDB\Server\{versão}\bin`.

## 2. Testando a Conexão:
   - Execute o script Python abaixo para testar se deu tudo certo:
    ```python
    from pymongo import MongoClient

    # Conectar ao servidor MongoDB
    client = MongoClient('localhost', 27017)

    # Acessar o banco de dados de teste
    db = client.test

    # Inserir um documento de teste
    result = db.test_collection.insert_one({'name': 'teste', 'value': 42})

    print(f"Documento inserido com ID: {result.inserted_id}")
    ```