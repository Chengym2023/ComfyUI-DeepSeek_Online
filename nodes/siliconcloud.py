from openai import OpenAI
from .aiing import *

class SiliconCloudReasoning:
    def __init__(self):
        sc = config.get('SiliconCloud')
        
        self.api_key = sc.get('api_key', '')
        assert self.api_key != '', "Please add your SiliconCloud API key to {}".format(config_path)
        self.base_url = sc.get('url', '')
        

    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "reasoning_model":(reasoning_model_list,{"default":"none"}),
                "model":(model_list,{"default":"none"}),
                "system":("STRING", {"default": SYSTEM,
                                    "multiline": True}),
                "prompt": ("STRING", {"default": USER,"multiline": True}),
                "prefix_continuation": ("STRING", {"default": ""}),
                "fim": ("STRING", {"default": ""}),
                "max_tokens": ("INT", {"default": 4096, "min": 1, "max": 8192, "step": 1}),
                "temperature": ("FLOAT", {"default": 0.6, "min": 0.0, "max": 2.0, "step": 0.1}),
                "top_p": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 1.0, "step": 0.1}),
                "frequency_penalty": ("FLOAT", {"default": 0.1, "min": -2.0, "max": 2.0, "step": 0.1}),
                "presence_penalty": ("FLOAT", {"default": 0.1, "min": -2.0, "max": 2.0, "step": 0.1}),
                "stream": ("BOOLEAN", {"default": True}),

            },
            "optional": {
                "context": ("STRING"),
                "context_q": ("STRING"),
            }
        }

    RETURN_TYPES = ("STRING", "STRING","STRING","STRING")
    RETURN_NAMES = ("content", "reasoning","format","negative prompt")
    FUNCTION = "process"
    CATEGORY = "💯AI"

    def process(self,reasoning_model, model,system, prompt, prefix_continuation,fim,max_tokens, temperature,top_p,frequency_penalty,presence_penalty,stream, context="", context_q=""):
        if reasoning_model == "none" and model == "none":
            return ("Please select a reasoning model or a model", "unavailable.","unavailable.","unavailable.")
        try:
            client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key
                )

            messages = [                    
                    {"role": "user", "content": system+","+prompt}]
            if context:
                messages.append({"role": "assistant", "content": context})
                messages.append({'role': 'user', 'content': context_q})
            
            if prefix_continuation or fim:
                response = client.chat.completions.create(
                    model=reasoning_model if reasoning_model != "none" else model,
                    messages=messages,
                    stream=stream, # 是否流式处理
                    max_tokens=max_tokens,# 最大输出长度
                    temperature=temperature,      # 控制随机性 (0-2)
                    top_p=top_p,          # 核采样概率 (0-1)
                    frequency_penalty=frequency_penalty,  # 重复惩罚 (-2.0~2.0)
                    presence_penalty=presence_penalty,   # 话题新鲜度 (-2.0~2.0)
                    extra_body = prefix_continuation if prefix_continuation else fim
)
            else:
                response = client.chat.completions.create(
                        model=reasoning_model if reasoning_model != "none" else model,
                        messages=messages,
                        stream=stream, # 是否流式处理
                        max_tokens=max_tokens,# 最大输出长度
                        temperature=temperature,      # 控制随机性 (0-2)
                        top_p=top_p,          # 核采样概率 (0-1)
                        frequency_penalty=frequency_penalty,  # 重复惩罚 (-2.0~2.0)
                        presence_penalty=presence_penalty,   # 话题新鲜度 (-2.0~2.0)
                    
)
            
            content = ""
            reasoning_content=""
            format_prompt = ""
            negative_prompt = ""
            if stream:
                for chunk in response:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        content += delta.content
                    if delta.reasoning_content:
                        reasoning_content += delta.reasoning_content
            else:
                messages = response.choices[0].message
                if messages.content:
                    content = messages.content
                    if messages.reasoning_content:
                        reasoning_content = messages.reasoning_content
            format_prompt = format_content(content)
            negative_prompt = extract_negative_prompt(content)
            return (content, reasoning_content,format_prompt,negative_prompt)


        except Exception as e:
            error = f"Error: {str(e)}"
            return (error, "unavailable.","unavailable.","unavailable.")



