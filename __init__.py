# __init__.py
from .cl_orso_character_sheet_generator_comfyui_bindings import Cl_orso_character_sheet_generator_comfyui_bindings
from .cl_orso_character_sheet_generator_comfyui_bindings import Cl_npc_json
from .cl_orso_character_sheet_generator_comfyui_bindings import Cl_npc_ability_json

# node identifier - python class
NODE_CLASS_MAPPINGS = {
    "D&D5E NPC Sheet Generator": Cl_orso_character_sheet_generator_comfyui_bindings,
    "D&D5E NPC JSON": Cl_npc_json,
    "D&D5E NPC ABILITY JSON": Cl_npc_ability_json,
}

# node identifier - displayed name
NODE_DISPLAY_NAME_MAPPINGS = {
    "D&D5E NPC Sheet Generator": "D&D5E NPC Sheet Generator",
    "D&D5E NPC JSON": "D&D5E NPC STAT BLOCK",
    "D&D5E NPC ABILITY JSON": "D&D5E NPC ABILITY",
}

EXTENSION_NAME = "orso-character-sheet-generator"
