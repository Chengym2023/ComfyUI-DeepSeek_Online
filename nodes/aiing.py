import json
import os
import re


def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "config.json")

    config = {}
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

    return (config ,config_path)

(config,config_path) = load_config()

def format_output(content):
    
    pattern = r'"answer":\s*"([^"]+)"'


    match = re.search(pattern, content)
    if match:
        answer = match.group(1)
        return answer.strip()
    return content
def format_content(content):
    start_marker = "**Prompt:**"
    prefix_quote = "\""
    prefix = "`"
    extracted_content = ""
    start_index = content.find(start_marker)
    if start_index != -1:
        start_index += len(start_marker)
        start_quote_index = content.find(prefix_quote, start_index)
        if start_quote_index != -1:
            end_quote_index = content.find(prefix_quote, start_quote_index + 1)
            extracted_content = content[start_quote_index + 1:end_quote_index]
        else:
            start_index = content.find(prefix, start_index)
            if start_index != -1:
                start_index += len(prefix)
                end_index = content.find(prefix, start_index)
                if end_index != -1:
                    extracted_content = content[start_index:end_index]
            else:
                end_index = content.find("*",start_index)
                extracted_content = content[start_index:end_index]
    return extracted_content.strip() or content

def extract_negative_prompt(content):
    start_marker = "**Negative prompt:**"
    start_index = content.find(start_marker)
    if start_index == -1:
        return ""
    start_index += len(start_marker)
    end_index = content.find("\n", start_index)
    if end_index == -1:
        end_index = len(content)
    return content[start_index:end_index].strip()

SYSTEM = "You are a professional AI prompt engineer specializing in creating high-quality, structured image generation prompts for Stable Diffusion."

USER = "Give a example prompt!在这输入要求,英文输出,标签形式,非mj格式"

FORMAT_OUTPUT ='''The user will provide some exam text. Please parse the "question" and "answer" and output them in JSON format. 

EXAMPLE INPUT: 
Which is the highest mountain in the world? Mount Everest.

EXAMPLE JSON OUTPUT:
{
    "question": "Which is the highest mountain in the world?",
    "answer": "Mount Everest"
}'''
reasoning_model_list = [
    "none",
    "deepseek-ai/DeepSeek-R1",
    "Pro/deepseek-ai/DeepSeek-R1",
    "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
    "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    "Pro/deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
    "Pro/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    "Pro/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
]

model_list = [
    "none",
    "deepseek-ai/DeepSeek-V3",
    "Pro/deepseek-ai/DeepSeek-V3",
    "meta-llama/Llama-3.3-70B-Instruct",
    "AIDC-AI/Marco-o1",
    "deepseek-ai/DeepSeek-V2.5",
    "Qwen/Qwen2.5-72B-Instruct-128K",
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/Qwen2.5-32B-Instruct",
    "Qwen/Qwen2.5-14B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "Qwen/Qwen2.5-Coder-7B-Instruct",
    "Qwen/Qwen2-7B-Instruct",
    "Qwen/Qwen2-1.5B-Instruct",
    "Qwen/QwQ-32B-Preview",
    "TeleAI/TeleChat2",
    "01-ai/Yi-1.5-34B-Chat-16K",
    "01-ai/Yi-1.5-9B-Chat-16K",
    "01-ai/Yi-1.5-6B-Chat",
    "THUDM/glm-4-9b-chat",
    "Vendor-A/Qwen/Qwen2.5-72B-Instruct",
    "internlm/internlm2_5-7b-chat",
    "internlm/internlm2_5-20b-chat",
    "nvidia/Llama-3.1-Nemotron-70B-Instruct",
    "meta-llama/Meta-Llama-3.1-405B-Instruct",
    "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "google/gemma-2-27b-it",
    "google/gemma-2-9b-it",
    "Pro/Qwen/Qwen2.5-7B-Instruct",
    "Pro/Qwen/Qwen2-7B-Instruct",
    "Pro/Qwen/Qwen2-1.5B-Instruct",
    "Pro/THUDM/chatglm3-6b",
    "Pro/THUDM/glm-4-9b-chat",
    "Pro/meta-llama/Meta-Llama-3.1-8B-Instruct",
    "Pro/google/gemma-2-9b-it"
]