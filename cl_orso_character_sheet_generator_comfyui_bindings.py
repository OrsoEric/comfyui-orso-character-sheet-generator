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



class Cl_orso_character_sheet_generator_comfyui_bindings:
    """
    ComfyUI node that wraps your generate_card() method.
    """

    @classmethod
    def INPUT_TYPES(cls):
        d_input_definitions = {
            "image": ("IMAGE",),
            "i_s_npc_json": ("STRING", {"multiline": True}),
        }

        d_optional = {
            "i_ls_layout_file_path": ("layout/npc_layout_en.json",),
            "i_ls_mask_front_path": ("mask/front_mask.png",),
            "i_ls_mask_back_path": ("mask/back_mask.png",),
        }


        return {
            "required": d_input_definitions,
            "optional": d_optional,
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("card_image",)
    FUNCTION = "generate"
    CATEGORY = "orso"

    def generate(
        self,
        image: lib_torch.Tensor,
        i_s_npc_json: str,
        i_ls_layout_file_path: str,
        i_ls_mask_front_path: str,
        i_ls_mask_back_path: str,
    ) -> Tuple[lib_torch.Tensor]:
    
        # --- Tensor → St_image ---
        st_img = St_image.from_tensor( image[0], 300 )

        cl_generator = cl_generator = Cl_npc_character_sheet_generator(
            i_w_card_width_mm=63.5,
            i_h_card_height_mm=88.9,
            i_n_dots_per_inch = 300,
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
            
        o_st_tensor = o_st_pil.to_tensor()
        
        return (o_st_tensor)



