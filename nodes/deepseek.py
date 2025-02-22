from openai import OpenAI
from .aiing import *

class DeepSeekOnline:
    def __init__(self):
        sc = config.get('DeepSeek_online')
        
        self.api_key = sc.get('api_key', '')
        assert self.api_key != '', "Please add your deepseek API key to {}".format(config_path)
        self.base_url = sc.get('url', '')
        

    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model":(("deepseek-chat","deepseek-reasoner"), {"default": "deepseek-chat"}),
                "system":("STRING", {"default": SYSTEM+FORMAT_OUTPUT,
                                    "multiline": True}),
                "prompt": ("STRING", {"default": USER,"multiline": True}),
                "prefix_continuation": ("STRING", {"default": ""}),
                "fim": ("STRING", {"default": ""}),
                "max_tokens": ("INT", {"default": 4096, "min": 1, "max": 8192, "step": 1}),
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

    def process(self, model,system, prompt, prefix_continuation,fim,max_tokens, stream, context="", context_q=""):
        if prefix_continuation or fim:
            self.base_url="https://api.deepseek.com/beta"


        try:
            client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key
                )
            if prefix_continuation:    
                messages = [
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": prefix_continuation, "prefix": True}
]           
            else:
                messages = [      
                        {"role": "system", "content": system},              
                        {"role": "user", "content": prompt}]
            if context:
                messages.append({"role": "assistant", "content": context})
                messages.append({'role': 'user', 'content': context_q})
            
            if fim:
                response = client.completions.create(
                    model=model,
                    prompt=prompt,
                    suffix=fim,
                    max_tokens=max_tokens,
                    stream=stream,
                )

            else:
                response = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        stream=stream, # 是否流式处理
                        max_tokens=max_tokens,# 最大输出长度
                    
)
            
            content = ""
            reasoning_content=""
            format_content = ""
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
            format_content = format_content(content)
            negative_prompt = extract_negative_prompt(content)
            return (content, reasoning_content,format_content,negative_prompt)


        except Exception as e:
            error = f"Error: {str(e)}"
            return (error, "unavailable.","unavailable.","unavailable.")



