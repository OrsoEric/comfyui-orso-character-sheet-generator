# __init__.py

from .cl_orso_demo_image_invert import Cl_orso_demo_image_invert
from .cl_orso_character_sheet_generator_comfyui_bindings import Cl_orso_character_sheet_generator_comfyui_bindings

NODE_CLASS_MAPPINGS = {
    "DEMO Image Invert": Cl_orso_demo_image_invert,
    "DEMO D&D5E": Cl_orso_character_sheet_generator_comfyui_bindings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DEMO Image Invert": "DEMO Image Inversion",
    "DEMO D&D5E": "DEMO D&D5E"
}

EXTENSION_NAME = "orso-character-sheet-generator"