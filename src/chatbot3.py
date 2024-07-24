# from langchain import LLMChain, PromptTemplate
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
# from langchain_community.llms import HuggingFacePipeline
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAPI_API_KEY")




# pip install -U langchain-huggingface


def main():
    # Nome do modelo LLaMA 2 disponível no Hugging Face
    # model_name = "meta-llama/Llama-2-7b-hf"  # Exemplo de nome de modelo LLaMA 2 no Hugging Face
    model_name = "gpt2-large"

    # Carregar o modelo e o tokenizer do Hugging Face
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Criar o pipeline de geração de texto
    nlp = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        # max_length=512,
        truncation=True,
        pad_token_id=tokenizer.eos_token_id,
        num_return_sequences=1,
        max_new_tokens=50,
        return_full_text=False,
        temperature=0.7,
        top_p=0.9
    )
    llm = HuggingFacePipeline(pipeline=nlp)

    # Definir o template do prompt
    prompt_template = PromptTemplate(
        input_variables=["input"],
        template="Human: {input}\nAI:"
    )

    # Configurar o LLMChain com o template de prompt
    # llm_chain = LLMChain(
    #     llm=llm,
    #     prompt=prompt_template
    # )

    llm_chain = prompt_template | llm

    # Função para conversar com o chatbot
    def chat_with_bot(prompt):
        # response = llm_chain.run(input=prompt)
        response = llm_chain.invoke(input=prompt)
        return response.strip()

    # Testar o chatbot com um prompt de exemplo
    prompt = "Olá, como você está hoje?"
    resposta = chat_with_bot(prompt)
    print(resposta)

if __name__ == "__main__":
    main()

# print("oi")