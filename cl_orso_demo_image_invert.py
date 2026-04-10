# custom_nodes/cl_orso_demo_image_invert.py

import torch

class Cl_orso_demo_image_invert:
    """
    A tiny ComfyUI node that takes an image tensor, inverts every pixel,
    and emits the inverted image.
    """

    @classmethod
    def INPUT_TYPES(s):
        """Define the inputs that the UI will present.

        - `image`: a tensor of shape (batch, channels, height, width)
          with values in [0.0, 1.0].
        """
        return {
            "required": {"image": ("IMAGE",)},
        }

    # The node produces one output: an inverted image.
    RETURN_TYPES = ("IMAGE",)

    # This string tells ComfyUI which function to call when the node
    # is executed.
    FUNCTION = "invert"

    # Optional: group the node under a custom category in the sidebar.
    CATEGORY = "orso/utils"

    def invert(self, image):
        """
        Invert an RGB (or RGBA) image.

        Parameters:
            image (torch.Tensor): Input image tensor in [0.0, 1.0].

        Returns:
            tuple: A single-element tuple containing the inverted image.
        """
        # Guard against non‑float tensors or values outside [0,1]
        if not isinstance(image, torch.Tensor):
            raise TypeError("Input 'image' must be a torch.Tensor.")

        # Clip to avoid numerical issues and perform inversion
        inv = 1.0 - torch.clamp(image, 0.0, 1.0)

        return (inv,)
