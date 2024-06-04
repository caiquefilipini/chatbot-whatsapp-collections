import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
import torch

# Carregar o modelo e o tokenizador
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForCausalLM.from_pretrained("distilgpt2")

# Configurar o pipeline do Hugging Face
device = 0 if torch.cuda.is_available() else -1  # 0 para GPU, -1 para CPU
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)

# Definir o template do prompt com LangChain
template = PromptTemplate(
    input_variables=["question"],
    template="Você é um assistente útil. Responda à pergunta: {question}"
)

# Criar a cadeia LLM usando HuggingFacePipeline
llm_pipeline = HuggingFacePipeline(pipeline=pipe)
chain = template | llm_pipeline

# Função para gerar a resposta usando LangChain
def generate_response(user_input):
    # Gerar resposta usando o pipeline diretamente para depuração
    response = pipe(user_input, max_length=100, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    generated_text = response[0]['generated_text']
    return generated_text

# Variáveis para armazenar estado da conversa
conversation_history = []

# Função principal do chatbot
def chatbot_flow(client_message, user_rating=None, user_message=None):
    global conversation_history
    
    if client_message:
        # Etapa 2: O bot sugere uma resposta
        bot_suggestion = generate_response(client_message)
        conversation_history.append({'Client': client_message, 'Bot Suggestion': bot_suggestion})
        return bot_suggestion, gr.update(visible=True), gr.update(visible(True)), gr.update(visible(False))
    
    if user_rating is not None and user_message:
        # Registrar a avaliação e a mensagem do usuário
        conversation_history[-1]['User Rating'] = user_rating
        conversation_history[-1]['User Message'] = user_message
        
        # Abrir o campo para a próxima mensagem do cliente
        return "", gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)
    
    return "", gr.update(visible=False), gr.update(visible(False)), gr.update(visible(False))

# Interface do Gradio
with gr.Blocks() as demo:
    gr.Markdown("## ChatGPT Simulator")
    
    with gr.Row():
        client_input = gr.Textbox(label="Mensagem do Cliente", interactive=True)
    
    bot_suggestion_output = gr.Textbox(label="Sugestão do Bot", interactive=False, visible=False)
    rating = gr.Slider(1, 5, step=1, label="Avalie a Sugestão", interactive=True, visible=False)
    user_message_input = gr.Textbox(label="Sua Mensagem ao Cliente", interactive=True, visible=False)
    
    with gr.Row():
        client_submit = gr.Button("Enviar Mensagem do Cliente")
        rating_submit = gr.Button("Avaliar e Enviar Resposta", visible=False)
    
    client_submit.click(fn=chatbot_flow, inputs=[client_input], outputs=[bot_suggestion_output, rating, user_message_input, client_input])
    rating_submit.click(fn=chatbot_flow, inputs=[rating, user_message_input], outputs=[bot_suggestion_output, rating, user_message_input, client_input])

if __name__ == "__main__":
    demo.launch()
