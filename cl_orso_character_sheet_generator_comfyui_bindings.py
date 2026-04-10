from pathlib import Path
from typing import List, Tuple, Optional

import comfy.utils
import comfy.model_management as model_management
from PIL import Image

from .lib.st_image import St_image

from .lib.cl_generator import Cl_npc_character_sheet_generator

class lib_torch:
    from torch import Tensor

class Cl_orso_character_sheet_generator_comfyui_bindings:
    """
    ComfyUI node that wraps your generate_card() method.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "i_st_npc_illustration": {"image": ("IMAGE",)},
                "i_d_npc_json": ("STRING", {"multiline": True}),        
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("card_image",)
    FUNCTION = "generate"
    CATEGORY = "orso"

    def generate(
        self,
        i_ast_npc_illustration: lib_torch.Tensor,
        i_d_npc_json: dict,
    ) -> Tuple[lib_torch.Tensor]:
    
        # --- Tensor → St_image ---
        st_img = St_image.from_tensor(i_ast_npc_illustration[0], 300)

        i_ls_layout_file_path: List[str] = [""],
        i_ls_mask_front_path: List[str],
        i_ls_mask_back_path: List[str],

        i_background_color: Optional[Tuple[int, int, int]] = None,
        i_border_color: Optional[Tuple[int, int, int]] = None

        # Convert optional colors
        bg = self._parse_color(background_color)
        border = self._parse_color(border_color)

        # Instantiate your engine
        generator = YourCardGeneratorClass()

        # Call your existing method
        success = generator.generate_card(
            i_ls_layout_file_path=[layout_json],
            i_ls_mask_front_path=[mask_front],
            i_ls_mask_back_path=[mask_back],
            i_ls_npc_illustration_path=[npc_image],
            i_ls_npc_json_path=[npc_json],
            i_ls_output_file_path=[output_path],
            i_background_color=bg,
            i_border_color=border
        )

        if success:
            raise RuntimeError("Card generation failed inside generate_card().")

        # Load the output image for ComfyUI
        img = Image.open(output_path).convert("RGB")
        return (comfy.utils.PIL_to_tensor(img),)
