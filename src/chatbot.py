# # from transformers import GPT2LMHeadModel, GPT2Tokenizer
# # import torch
# # from flask import Flask, request, jsonify





# # import langchain
# # # ...



# import os
# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
# from dotenv import load_dotenv
# load_dotenv()


# # from langchain_openai import ChatOpenAI

# ACCESS_TOKEN = os.getenv("ACCESS_TOKEN") # reads .env file with ACCESS_TOKEN=<your hugging face access token>

# model_id = "google/gemma-2b-it"
# tokenizer = AutoTokenizer.from_pretrained(model_id, token=ACCESS_TOKEN)
# quantization_config = BitsAndBytesConfig(load_in_4bit=True, 
#                                          bnb_4bit_compute_dtype=torch.bfloat16)

# model = AutoModelForCausalLM.from_pretrained(model_id, 
#                                              device_map="auto", 
#                                              quantization_config=quantization_config,
#                                              token=ACCESS_TOKEN)
# model.eval()
# device = 'cuda' if torch.cuda.is_available() else 'cpu'

# def generate(question: str, context: str):
#     if context == None or context == "":
#         prompt = f"""Give a detailed answer to the following question. Question: {question}"""
#     else:
#         prompt = f"""Using the information contained in the context, give a detailed answer to the question.
#             Context: {context}.
#             Question: {question}"""
#     chat = [{"role": "user", "content": prompt}]
#     formatted_prompt = tokenizer.apply_chat_template(
#         chat,
#         tokenize=False,
#         add_generation_prompt=True,
#     )
#     inputs = tokenizer.encode(
#         formatted_prompt, add_special_tokens=False, return_tensors="pt"
#     ).to(device)
#     with torch.no_grad():
#         outputs = model.generate(
#             input_ids=inputs,
#             max_new_tokens=250,
#             do_sample=False,
#         )
#     response = tokenizer.decode(outputs[0], skip_special_tokens=False)
#     response = response[len(formatted_prompt) :]  # remove input prompt from reponse
#     response = response.replace("<eos>", "")  # remove eos token
#     return response


# prompt = "Olá, tudo bem? Como posso ajudar você hoje?"

# resposta = llm.invoke(prompt)
# print(resposta)

# # # Resposta do chatbot
# Carregar histórico de interações
def bot_response(customer_message):
    if customer_message == "a":
        resposta = "Resposta padrão (igual a a)."
    else:
        resposta = "Resposta padrão (diferente de a)."
    return resposta

# # import langchain

# # "meta-llama/Llama-2-7b-chat-hf"

# import os


# # from langchain_openai import OpenAIGPT2

# import langchain_openai

# # print(os.listdir(os.getcwd()))

# prompt_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts", "prompt.txt")

# with open(prompt_file, "r") as file:
#     prompt = file.read()

# print(prompt)