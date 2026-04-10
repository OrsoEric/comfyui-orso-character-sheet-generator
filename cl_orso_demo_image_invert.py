# custom_nodes/cl_orso_demo_image_invert.py

from typing import Tuple
#from .lib.cl_pil_tensor_convert import Cl_pil_tensor_convert
from .lib.st_image import St_image 

class lib_torch:
    from torch import Tensor
    
class lib_pil:
    from PIL import Image
    from PIL.ImageOps import invert

class Cl_orso_demo_image_invert:
    """
    A ComfyUI node that takes an image tensor, converts it to St_image,
    inverts pixels using St_image logic (no PIL), and returns the result.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"image": ("IMAGE",)},
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "invert"
    CATEGORY = "orso"
    
    def invert(self, image: lib_torch.Tensor):
        """
        Invert an RGB(A) image using PIL through St_image.

        Input:
            image: Tensor (B, H, W, C) in [0,1]

        Output:
            (inverted_tensor,)
        """

        if not hasattr(image, "shape"):
            raise TypeError("Input 'image' must be a torch.Tensor.")

        # Ensure float and clamp
        image = image.float().clamp(0.0, 1.0)

        batch, height, width, channels = image.shape
        out = image.clone()

        for n_index_batch in range(batch):
            hwc = image[n_index_batch]  # (H, W, C)

            # --- Tensor → St_image ---
            st_img = St_image.from_tensor(hwc, 300)

            # --- PIL inversion ---
            pil_img = st_img.g_cl_image

            if pil_img.mode == "RGBA":
                r, g, b, a = pil_img.split()
                rgb = lib_pil.Image.merge("RGB", (r, g, b))
                rgb_inv = lib_pil.invert(rgb)
                r_i, g_i, b_i = rgb_inv.split()
                st_img.g_cl_image = lib_pil.Image.merge("RGBA", (r_i, g_i, b_i, a))
            else:
                st_img.g_cl_image = lib_pil.invert(pil_img)

            # --- St_image → Tensor ---
            out[n_index_batch] = st_img.to_tensor()

        return (out,)