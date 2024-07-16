

pip install optimum
pip install transformers
pip install accelerate
pip install peft

ConversationBufferWindowMemory
ConversationBufferWindowMemory

import os
from dotenv import load_dotenv
load_dotenv()
os.getenv("ACCESS_TOKEN")


from huggingface_hub import login
login()
from transformers import AutoTokenizer, GPTQConfig
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig

from langchain.prompts import PromptTemplate


pretrained_model_name = "meta-llama/Meta-Llama-3-8B"
tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name)
quantize_config = BaseQuantizeConfig(bits=4, group_size=128)
model = AutoGPTQForCausalLM.from_pretrained(pretrained_model_name, quantize_config, torch_dtype=torch.float16, low_cpu_mem_usage=True)



pipe = pipeline(
    task="text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512
    )

llm=HuggingFacePipeline(pipeline=pipe)


template = """
{history}
Question: {input}
"""

PromptTemplate.from_file....


prompt = PromptTemplate(input_variables=["history", "input"], template=template)
memory=ConversationBufferWindowMemory(k=3)

llm_chain = ConversationChain(prompt=prompt, llm=llm, memory=memory)