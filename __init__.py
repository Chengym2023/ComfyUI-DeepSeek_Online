from .nodes.siliconcloud import SiliconCloudReasoning


NODE_CLASS_MAPPINGS = {
    "SiliconCloud": SiliconCloudReasoning,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SiliconCloud": "💯SiliconCloudReasoning"
}


__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']