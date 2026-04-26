from pathlib import Path
from typing import List, Tuple, Optional

import comfy.utils
import comfy.model_management as model_management
from PIL import Image

from .lib.st_image import St_image

from .lib.cl_generator import Cl_npc_character_sheet_generator

import json

class lib_torch:
    from torch import Tensor

#category in ComfyUI where the nodes are displayed
C_S_CATEGORY = "dnd5e-orso"

class Cl_orso_character_sheet_generator_comfyui_bindings:
    """
    ComfyUI node that wraps your generate_card() method.
    """

    @classmethod
    def INPUT_TYPES(cls):
        d_input_definitions = {
            "i_w_card_width_mm" : ("FLOAT", {"default": 63.5, "min": 0.0 }),
            "i_h_card_height_mm" : ("FLOAT", {"default": 88.9, "min": 0.0 }),
            "i_n_dots_per_inch": ("INT", {"default": 300, "min": 1, "step": 50}),
            "image": ("IMAGE",),
            "i_s_npc_json": ("STRING", {"multiline": True}),
            "i_ls_layout_file_path": ("STRING", {"multiline": False, "default": "layout/npc_layout_en.json"}),
            "i_ls_mask_front_path": ("STRING", {"multiline": False, "default": "mask/front_mask.png"}),
            "i_ls_mask_back_path": ("STRING", {"multiline": False, "default": "mask/back_mask.png"}),
        }

        #d_optional = {}

        return {
            "required": d_input_definitions,
            #"optional": d_optional,
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("card_image",)
    FUNCTION = "generate"
    CATEGORY = C_S_CATEGORY

    def generate(
        self,
        i_w_card_width_mm : float,
        i_h_card_height_mm : float,
        i_n_dots_per_inch : int, 
        image: lib_torch.Tensor,
        i_s_npc_json: str,
        i_ls_layout_file_path: str,
        i_ls_mask_front_path: str,
        i_ls_mask_back_path: str,
    ) -> Tuple[lib_torch.Tensor]:
    
        s_node_root_folder = Path(__file__).resolve().parent
        print(f"D&D Generator Parent Directory {s_node_root_folder}")
    
        # --- Tensor → St_image ---
        st_img = St_image.from_tensor( image[0], 300 )
        print(f"Loading NPC image: {st_img}")
        
        cl_generator = cl_generator = Cl_npc_character_sheet_generator(
            i_w_card_width_mm=i_w_card_width_mm,
            i_h_card_height_mm=i_h_card_height_mm,
            i_n_dots_per_inch = i_n_dots_per_inch,
            i_s_comfy_root = s_node_root_folder,
            i_background_color=(255, 255, 255),
            i_border_color=(0, 0, 0)
        )
        
        o_st_pil = cl_generator.generate_comfy_ui(
            i_cl_npc_illustration=st_img,
            i_d_npc_json=json.loads(i_s_npc_json),
            
            i_ls_layout_file_path = i_ls_layout_file_path,
            i_ls_mask_front_path = i_ls_mask_front_path,
            i_ls_mask_back_path= i_ls_mask_back_path,
        )
        print(f"Generated NPC Character SHeet Image: {o_st_pil}")
            
        o_st_tensor : lib_torch.Tensor = o_st_pil.to_tensor()
        #add an extra batch dimension at the beginning
        o_st_tensor = o_st_tensor.unsqueeze(0)
        print(f"Character Sheet Tensor Shape: {o_st_tensor.shape}") 
        
        return (o_st_tensor,)

class Cl_npc_json:
    @classmethod
    def INPUT_TYPES(cls):
        d_required = {
            # Core identity
            "name": ("STRING", {"default": "Olivia Prezzo"}),
            "race": ("STRING", {"default": "Halfling - Lightfoot"}),

            # Stats
            "cr": ("STRING", {"default": "5"}),
            "hp": ("INT", {"default":50, "min": 1, "max": 999}),
            "ac": ("INT", {"default": 16, "min": 0, "max": 50}),
            "speed": ("STRING", {"default": "Walk: 6sq"}),

            # Description & flavor
            "image_prompt": ("STRING", {"multiline": True, "default": "Portrait AR1:1.5. Digital, semi-realistic painterly style that blends heroic fantasy with vibrant color palettes and detailed, textured, and shadowed rendering. Full body from head to toe. Chubby Halfling. Visible eye bags. Neutral expression. She's wearing a pointed hat and a rugged, earth‑toned robe cinched with a belt. In each hand, she holds a large glass flask—one filled with a vivid red liquid and the other with a bright green one. On her back, a alchemical refining alambic backpack with glass tubes and condensation loops with colorful liquids gurgling trough. Background is her workshop with wooden walls."}),
            "description": ("STRING", {"multiline": True, "default": "Olivia Prezzo, a halfling woman in her forties, has become Campocestro's clandestine alchemist. Her laboratory is lined with dusty vials and ancient apparatus that glimmer with a faint blue glow despite their age. Chubby and a leg tall, her eyes perpetually rimmed with dark circles from endless nights of experimentation. She does lots of field work, and possesses an alchemical backpack to brew perishible ingredients on her gathering expeditions. The villagers hold her in high regard for her botanical expertise that saved countless crops from drought. Nobody knows why she left her prestigious job in Ironspur to come to the Ao forsaken frontier village of Campocestro"}),

            "resources": ("STRING", {"multiline": True, "default": "Actions: 1\nBonus Actions: 1\nReactions: 1\nLegendary Actions: 1"}),

            "spellcasting": ("STRING", {"multiline": True, "default": "Spell ability: INT\nSpell List: Wizard (Alchemist)\nSpell Bonus: +5\nSpell Save DC: 16\nSpell Slots: 5, 3, 1"}),

            # Combat traits
            "immunity": ("STRING", {"default": "Poison"}),
            "resistance": ("STRING", {"default": "Acid"}),
            "weakness": ("STRING", {"default": "Holy, Blunt, Fire"}),

            # Meta
            "proficiency": ("INT", {"default": 3, "min": -10, "max": 10}),
            "initiative": ("INT", {"default": 3, "min": -10, "max": 10}),

            # --- STRENGTH ---
            "str_sep": ("STRING", {"default": "====== STRENGTH ======", "multiline": False}),
            "STRENGTH": ("INT", {"default": -2, "min": -10, "max": 10}),
            "STR SAVE": ("INT", {"default": -2, "min": -10, "max": 10}),
            "ATHLETICS": ("INT", {"default": -1, "min": -10, "max": 20}),

            # --- DEXTERITY ---
            "dex_sep": ("STRING", {"default": "====== DEXTERITY ======", "multiline": False}),
            "DEXTERITY": ("INT", {"default": 3, "min": -10, "max": 10}),
            "DEX SAVE": ("INT", {"default": 3, "min": -10, "max": 10}),
            "ACROBATICS": ("INT", {"default": 3, "min": -10, "max": 20}),
            "SLEIGHT OF HAND": ("INT", {"default": 1, "min": -10, "max": 20}),
            "STEALTH": ("INT", {"default": 2, "min": -10, "max": 20}),

            # --- CONSTITUTION ---
            "con_sep": ("STRING", {"default": "====== CONSTITUTION ======", "multiline": False}),
            "CONSTITUTION": ("INT", {"default": 1, "min": -10, "max": 10}),
            "CON SAVE": ("INT", {"default": 1, "min": -10, "max": 10}),

            # --- INTELLIGENCE ---
            "int_sep": ("STRING", {"default": "====== INTELLIGENCE ======", "multiline": False}),
            "INTELLIGENCE": ("INT", {"default": 5, "min": -10, "max": 10}),
            "INT SAVE": ("INT", {"default": 8, "min": -10, "max": 10}),
            "ARCANA": ("INT", {"default": 4, "min": -10, "max": 20}),
            "INVESTIGATION": ("INT", {"default": 3, "min": -10, "max": 20}),
            "HISTORY": ("INT", {"default": 2, "min": -10, "max": 20}),
            "NATURE": ("INT", {"default": 1, "min": -10, "max": 20}),
            "RELIGION": ("INT", {"default": 0, "min": -10, "max": 20}),

            # --- WISDOM ---
            "wis_sep": ("STRING", {"default": "====== WISDOM ======", "multiline": False}),
            "WISDOM": ("INT", {"default": 1, "min": -10, "max": 10}),
            "WIS SAVE": ("INT", {"default": 2, "min": -10, "max": 10}),
            "ANIMAL HANDLING": ("INT", {"default": -1, "min": -10, "max": 20}),
            "INSIGHT": ("INT", {"default": 2, "min": -10, "max": 20}),
            "PERCEPTION": ("INT", {"default": 3, "min": -10, "max": 20}),
            "MEDICINE": ("INT", {"default": 5, "min": -10, "max": 20}),
            "SURVIVAL": ("INT", {"default": 0, "min": -10, "max": 20}),

            # --- CHARISMA ---
            "cha_sep": ("STRING", {"default": "====== CHARISMA ======", "multiline": False}),
            "CHARISMA": ("INT", {"default": 0, "min": -10, "max": 10}),
            "CHA SAVE": ("INT", {"default": 0, "min": -10, "max": 10}),
            "DECEPTION": ("INT", {"default": 1, "min": -10, "max": 20}),
            "INTIMIDATION": ("INT", {"default": -1, "min": -10, "max": 20}),
            "PERFORMANCE": ("INT", {"default": -1, "min": -10, "max": 20}),
            "PERSUASION": ("INT", {"default": -1, "min": -10, "max": 20}),
        }

        d_optional = {
            "ability": ("STRING",),
        }

        return {
            "required": d_required,
            "optional": d_optional
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_json"
    CATEGORY = C_S_CATEGORY

    def generate_json(self, **kwargs):
        
        i_s_ability = kwargs["ability"]

        # If no input, start new list
        if i_s_ability is None or i_s_ability == "":
            ability = []
        else:
            try:
                ability = json.loads(i_s_ability)
            except:
                ability = []


        data = {
            "system": "DnD5E",
            "actor": "NPC",
            
            "NAME": kwargs["name"],
            "RACE": kwargs["race"],

            "CR": kwargs["cr"],
            "HP": str(kwargs["hp"]),
            "AC": str(kwargs["ac"]),
            "SPEED": f"SPEED: {kwargs['speed']}",

            "IMAGE PROMPT": kwargs["image_prompt"],
            "DESCRIPTION": kwargs["description"],

            "RESOURCES": f"{kwargs['resources']}",

            "IMMUNITY": f"IMMUNITY: {kwargs['immunity']}",
            "RESISTENCE": f"RESISTENCE: {kwargs['resistance']}",
            "WEAKNESS": f"WEAKNESS: {kwargs['weakness']}",
            
            "SPELLCASTING": f"{kwargs['spellcasting']}",

            "PROFICIENCY": kwargs["proficiency"],
            
            "INITIATIVE": kwargs["initiative"],

            "STRENGTH": kwargs["STRENGTH"],
            "STR SAVE": kwargs["STR SAVE"],
            "ATHLETICS": -2,

            "DEXTERITY": kwargs["DEXTERITY"],
            "DEX SAVE": kwargs["DEX SAVE"],
            "ACROBATICS": kwargs["ACROBATICS"],
            "SLEIGHT OF HAND": kwargs["SLEIGHT OF HAND"],
            "STEALTH": kwargs["STEALTH"],

            "CONSTITUTION": kwargs["CONSTITUTION"],
            "CON SAVE": kwargs["CON SAVE"],

            "INTELLIGENCE": kwargs["INTELLIGENCE"],
            "INT SAVE": kwargs["INT SAVE"],
            "ARCANA": kwargs["ARCANA"],
            "INVESTIGATION": kwargs["INVESTIGATION"],
            "HISTORY": kwargs["HISTORY"],
            "NATURE": kwargs["NATURE"],
            "RELIGION": kwargs["RELIGION"],

            "WISDOM": kwargs["WISDOM"],
            "WIS SAVE": kwargs["WIS SAVE"],
            "ANIMAL HANDLING": kwargs["ANIMAL HANDLING"],
            "INSIGHT": kwargs["INSIGHT"],
            "PERCEPTION": kwargs["PERCEPTION"],
            "MEDICINE": kwargs["MEDICINE"],
            "SURVIVAL": kwargs["SURVIVAL"],

            "CHARISMA": kwargs["CHARISMA"],
            "CHA SAVE": kwargs["CHA SAVE"],
            "DECEPTION": kwargs["DECEPTION"],
            "INTIMIDATION": kwargs["INTIMIDATION"],
            "PERFORMANCE": kwargs["PERFORMANCE"],
            "PERSUASION": kwargs["PERSUASION"],

            "ACTIONS": ability,
        }

        return (json.dumps(data, indent=4),)

class Cl_npc_ability_json:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "action_name": ("STRING", {"default": "Master Alchemist"}),
                "action_text": ("STRING", {"multiline": True, "default": "(passive) Olivia chooses an effect to add to potion she throws.\n--Venemous: Poison damage stacks and ticks at the end of the target turn, successfull CON SAVE removes one stack\n--Volatile: Acid damage affects all adjacent targets and objects\n--Corrosive: target AC is reduced by 1"}),
                "action_flavor": ("STRING", {"multiline": True, "default": "The knowledge that allow Olivia to proficiently heal people with her concoctions, is equally as effective in turning cococtions deadly"}),
            },
            "optional": {
                "abilities_in": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("abilities_out",)
    FUNCTION = "append_ability"
    CATEGORY = C_S_CATEGORY

    def append_ability(self, action_name, action_text, action_flavor, abilities_in=None):
        ability = {
            "s_name": action_name,
            "s_text": action_text,
            "s_flavor": action_flavor
        }

        # If no input, start new list
        if abilities_in is None or abilities_in == "":
            abilities = []
        else:
            try:
                abilities = json.loads(abilities_in)
            except:
                abilities = []

        abilities.append(ability)

        return (json.dumps(abilities, indent=4),)
