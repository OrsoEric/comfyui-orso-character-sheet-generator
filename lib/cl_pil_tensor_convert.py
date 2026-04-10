class lib_pil:
    from PIL import Image
    
class lib_torch:
    from torchvision.transforms.functional import to_pil_image, to_tensor
    from torch import Tensor, empty_like


class Cl_pil_tensor_convert:
    @staticmethod
    def tensor_to_pil(i_st_tensor: lib_torch.Tensor):
        """
        Convert a single image tensor (H, W, C) in [0,1] to a PIL Image.
        """
        if i_st_tensor.ndim != 3:
            raise ValueError("Expected tensor of shape (H, W, C).")

        # (H, W, C) -> (C, H, W)
        chw = i_st_tensor.permute(2, 0, 1).contiguous()

        # to_pil_image expects CHW
        return lib_torch.to_pil_image(chw)

    @staticmethod
    def pil_to_tensor(i_st_pil: lib_pil.Image.Image):
        """
        Convert a PIL Image back to a tensor (H, W, C) in [0,1].
        """
        # to_tensor returns (C, H, W)
        chw = lib_torch.to_tensor(i_st_pil)

        # (C, H, W) -> (H, W, C)
        hwc = chw.permute(1, 2, 0).contiguous()

        return hwc
