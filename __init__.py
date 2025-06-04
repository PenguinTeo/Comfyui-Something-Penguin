from .color_nodes import (
    BrightnessContrastNode,
    LevelsNode,
    HueSaturationNode,
    ColorBalanceNode,
    PerspectiveTransformNode,
)

NODE_CLASS_MAPPINGS = {
    "BrightnessContrastNode": BrightnessContrastNode,
    "LevelsNode": LevelsNode,
    "HueSaturationNode": HueSaturationNode,
    "ColorBalanceNode": ColorBalanceNode,
    "PerspectiveTransformNode": PerspectiveTransformNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BrightnessContrastNode": "Brightness/Contrast",
    "LevelsNode": "Levels",
    "HueSaturationNode": "Hue/Saturation",
    "ColorBalanceNode": "Color Balance",
    "PerspectiveTransformNode": "Perspective Transform",
}

__all__ = list(NODE_CLASS_MAPPINGS.keys())
