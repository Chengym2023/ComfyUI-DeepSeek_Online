from .nodes.siliconcloud import SiliconCloudReasoning
from .nodes.deepseek import DeepSeekOnline


NODE_CLASS_MAPPINGS = {
    "SiliconCloud": SiliconCloudReasoning,
    "DeepSeekOnline": DeepSeekOnline
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SiliconCloud": "💯SiliconCloudReasoning",
    "DeepSeekOnline": "💯DeepSeekOnline"
}


__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']