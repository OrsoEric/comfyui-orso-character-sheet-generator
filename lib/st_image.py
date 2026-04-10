"""
st_image.py

This module defines a structure that keeps an image together with its dimensional
information expressed in millimetres (mm), pixels (px) and dots per inch (dpi).
All configuration values are stored as **private instance attributes** – the
public API only exposes behaviour, not internal data.
"""

# --------------------------------------------------------------------------- #
# IMPORTS
# --------------------------------------------------------------------------- #

import logging

from .cl_utility_path import convert_to_path
import PIL.Image

from pathlib import Path

class lib_torch:
    from torch import Tensor
    
from .cl_pil_tensor_convert import Cl_pil_tensor_convert

# --------------------------------------------------------------------------- #
# CLASS DEFINITION
# --------------------------------------------------------------------------- #


class St_image:
    """
    A container for an image together with its dimensional metadata.

    The configuration (card size, DPI, etc.) is stored in private instance
    variables that are initialised once when the object is created.  Users
    interact only through the public methods.
    """

    # ----------------------------------------------------------------------- #
    # CONSTRUCTOR
    # ----------------------------------------------------------------------- #

    def __init__(
        self,
        i_w_card_mm : float,
        i_h_card_mm : float,
        i_dot_per_inch : int
    ) -> None:
        """
        Initialise the structure and set all configuration values.

        All parameters are kept private; they are prefixed with an underscore to
        signal that they should not be accessed directly from user code.
        """
        self.g_w_card_mm: float = i_w_card_mm          #: Width of a standard card in millimetres.
        self.g_h_card_mm: float = i_h_card_mm          #: Height of a standard card in millimetres.
        self.g_n_dot_per_inch: int = i_dot_per_inch          #: DPI – dots (pixels) per inch.
        self.g_n_mm_per_inch: float = 25.4        #: Millimetres per inch.

        self.g_w_card_px: int = int(0)
        self.g_h_card_px: int = int(0)

        self.compute_px()

        self.create_image( self.g_w_card_px, self.g_h_card_px )

        return

    # ----------------------------------------------------------------------- #
    # PUBLIC API
    # ----------------------------------------------------------------------- #

    def compute_px(
        self
    ) -> bool:
        """
        Compute the pixel width and height that correspond to the physical
        card dimensions at the configured DPI.

        Returns:
            A two‑tuple ``(width_px, height_px)`` containing the size in pixels.
        """
        logging.debug(f"W mm: {self.g_w_card_mm} | H mm {self.g_h_card_mm}")

        self.g_w_card_px: int = int(
            self.g_w_card_mm / self.g_n_mm_per_inch * self.g_n_dot_per_inch
        )
        self.g_h_card_px: int = int(
            self.g_h_card_mm / self.g_n_mm_per_inch * self.g_n_dot_per_inch
        )

        logging.debug(f"W px: {self.g_w_card_px} | H px {self.g_h_card_px}")

        return False #OK

    def get_size( self ):
        
        return (self.g_w_card_px, self.g_h_card_px)

    # ----------------------------------------------------------------------- #
    # 
    # ----------------------------------------------------------------------- #

    def draw_image(
        self,
        i_source_st_image: "St_image",
        i_offset_px: tuple[int, int],
        i_size_px: tuple[int, int]
    ) -> bool:
        """
        Draw a portion of *i_source_st_image* onto the current image.

        Parameters
        ----------
        i_source_st_image : St_image
            The source image from which data will be extracted.  Its internal
            Pillow image must already exist.
        i_offset_px : tuple[int, int]
            The (x, y) pixel coordinates inside *self.g_cl_image* where the
            top‑left corner of the drawn region will be placed.
        i_size_px : tuple[int, int]
            Desired width and height in pixels for the region to be copied.
            If this size differs from the source image's native dimensions,
            the source is resized accordingly before pasting.

        Returns
        -------
        bool
            ``False`` indicates a successful operation; ``True`` would signal an
            error (this mirrors the style of the other methods in this class).
        """
        if self.g_cl_image is None:
            logging.error("No destination image available for drawing.")
            return True  # ERROR

        if i_source_st_image.g_cl_image is None:
            logging.error("Source St_image has no image to draw.")
            return True  # ERROR

        lcl_source_img: PIL.Image.Image = i_source_st_image.g_cl_image

        # If the requested size differs from the source's actual size, resize it.
        if (i_size_px[0] != lcl_source_img.width or
                i_size_px[1] != lcl_source_img.height):
            lcl_source_img = lcl_source_img.resize(
                (i_size_px[0], i_size_px[1]),
                resample=PIL.Image.Resampling.LANCZOS
            )

        # Paste the processed source image onto the destination at the given offset.
        try:
            self.g_cl_image.paste(lcl_source_img, i_offset_px)
        except Exception as exc:  # pragma: no cover – unlikely but defensive
            logging.exception("Failed to paste image: %s", exc)
            return True  # ERROR

        logging.debug(
            "Pasted source image (%sx%s) at offset (%d,%d) onto destination "
            "(%dx%d).",
            lcl_source_img.width, lcl_source_img.height,
            i_offset_px[0], i_offset_px[1],
            self.g_cl_image.width, self.g_cl_image.height
        )

        return False  # OK


    def create_image(
        self,
        i_w_size_px : int,
        i_h_size_px : int,
        i_color: str = "white"
    ) -> bool:
        """
        Create a new RGB image that matches the physical dimensions of the card.

        The created image is stored in :attr:`_image`.  If an image already
        exists it will be replaced.

        Parameters:
            i_color (str): The background colour of the blank image.
                Any colour recognised by Pillow can be used, e.g. "white",
                "#FF00FF" or a tuple ``(R, G, B)``.
        """
        self.g_cl_image: PIL.Image.Image = PIL.Image.new(
            mode="RGB", size=(i_w_size_px, i_h_size_px), color=i_color
        )

        return False #OK

    def destroy_image(self) -> None:
        """
        Destroy the currently stored image.

        The method safely closes the Pillow image (if it implements the
        ``close`` protocol) and removes the reference so that Python's garbage
        collector can reclaim the memory.
        """
        if self.g_cl_image is not None:
            try:  # pragma: no cover
                getattr(self.g_cl_image, "close")()
            finally:
                del self.g_cl_image
                self.g_cl_image = None

    def apply_global_opacity_to_image(
        self,
        i_desired_opacity: float
    ) -> bool:
        """
        Applies a uniform opacity factor to every pixel of an RGBA image.

        Parameters
        ----------
        i_original_image : PIL.Image.Image
            The source image; it must already be in RGBA mode.
        i_desired_opacity : float
            Desired global opacity (0.0 – fully transparent, 1.0 – fully opaque).

        Returns
        -------
        PIL.Image.Image
            A new image with the alpha channel scaled by *i_desired_opacity*.
        """
        # Retrieve the pixel data as a NumPy array for efficient manipulation
        ln_pixels = self.g_cl_image.load()

        n_width, n_height = self.g_cl_image.size

        # Iterate over every pixel to modify its alpha component
        for i_x in range(n_width):
            for j_y in range(n_height):
                r_value, g_value, b_value, a_value = ln_pixels[i_x, j_y]
                # Scale the existing alpha by the desired opacity
                n_new_alpha: int = int(round(a_value * i_desired_opacity))
                n_new_alpha = max(0, min(255, n_new_alpha))  # clamp to [0,255]
                ln_pixels[i_x, j_y] = (r_value, g_value, b_value, n_new_alpha)

        return False #OK

    def compose_image(
        self, 
        i_st_mask_with_transparency : "St_image",
        i_n_opacity : float
    ) -> bool:
        
        i_st_mask_with_transparency.apply_global_opacity_to_image( i_n_opacity )

        self.g_cl_image = PIL.Image.alpha_composite(
            self.g_cl_image.convert("RGBA"),
            i_st_mask_with_transparency.g_cl_image.convert("RGBA")
        )

        return False #OK

    def load_image(
        self,
        i_ls_path : list[str] | Path
    ) -> bool:
        """
        Load an image from the supplied path components and store it in this
        instance.

        The function accepts a list of strings that together form the file
        system location of an image (e.g. ``["data", "card.png"]``).  It
        converts those parts to a :class:`pathlib.Path` using
        :func:`convert_to_path`, opens the file with Pillow, and assigns the
        resulting :class:`PIL.Image.Image` object to :attr:`g_cl_image`.

        The method follows the error‑handling convention used throughout the
        class: a return value of ``False`` indicates success while ``True``
        signals that an exception was raised during loading.

        Parameters:
            i_path_parts (list): Sequential path components that form the full
                image location.  Each element should be a string; missing
                directories will cause Pillow to raise an error and the
                method will return ``True``.

        Returns:
            bool: ``False`` on successful load, ``True`` if an exception was
            caught.
        """
        # Convert list of path components into a Path object.
        
        if type(i_ls_path) is type(list()):
            s_image_path = convert_to_path(i_ls_path)
        else:
            s_image_path = i_ls_path


        try:
            cl_image_loaded : PIL.Image.Image = PIL.Image.open(s_image_path)
            
        except Exception as exc:  # pragma: no cover – defensive
            logging.exception("Failed to load image from %s: %s", s_image_path, exc)
            return True  # ERROR
        

        # and the LANCZOS filter for high‑quality downsampling.
        cl_image_resized: PIL.Image.Image = cl_image_loaded.resize(
            (self.g_w_card_px, self.g_h_card_px),
            resample=PIL.Image.LANCZOS
        )

        self.g_cl_image = cl_image_resized

        return False  # OK


    def save_image(
        self,
        i_ls_path: list[str],
        i_s_format = "PNG"
    ) -> bool:
        """
        Persist the current image to disk as a PNG file.

        The list of strings is treated as successive components of a path
        (e.g. ``["output", "card.png"]``).  Any missing parent directories are
        created automatically.  If the supplied path does not have an extension,
        ``.png`` will be appended.

        Parameters:
            i_path_parts (list[str]): Components that together form the desired
                file path, e.g. a directory name and a filename without
                extension.

        Raises:
            ValueError: If no image has been created or loaded yet.
        """
        if self.g_cl_image is None:
            return True #ERROR

        if type(i_ls_path) is type(list()):
            s_image_path = convert_to_path(i_ls_path)
        else:
            s_image_path = i_ls_path

        logging.debug(f"input: {i_ls_path} path: {s_image_path}")

        self.g_cl_image.save(
            str(s_image_path),
            format=i_s_format,
            dpi=(self.g_n_dot_per_inch, self.g_n_dot_per_inch)
        )

        return False #OK

    # ----------------------------------------------------------------------- #
    # ComfyUI Tensor
    # ----------------------------------------------------------------------- #
    
    @classmethod
    def from_tensor(
        cls,
        i_st_tensor: lib_torch.Tensor,
        i_dot_per_inch: int
    ):
        """
        Construct a new St_image from a tensor (H, W, C) in [0,1].

        - Computes the physical size in millimetres from pixel size and DPI.
        - Creates a fully configured St_image instance.
        - Stores the tensor's pixel data WITHOUT resizing.

        Returns:
            St_image
        """

        # Extract pixel dimensions
        h_px, w_px, _ = i_st_tensor.shape

        # Convert px → mm
        mm_per_inch = 25.4
        w_mm = w_px / i_dot_per_inch * mm_per_inch
        h_mm = h_px / i_dot_per_inch * mm_per_inch

        # Create a new St_image with correct physical dimensions
        st = cls(
            i_w_card_mm=w_mm,
            i_h_card_mm=h_mm,
            i_dot_per_inch=i_dot_per_inch
        )

        # Directly store the tensor as a PIL image (NO resizing)
        st.g_cl_image = Cl_pil_tensor_convert.tensor_to_pil(i_st_tensor)

        return st


    def to_tensor(
        self
    ) -> lib_torch.Tensor:
        """
        Convert the current image into a tensor (H, W, C) in range [0,1].

        Returns:
            Tensor if image exists, None otherwise.
        """
        if self.g_cl_image is None:
            logging.error("No image available to convert to tensor.")
            return None

        try:
            return Cl_pil_tensor_convert.pil_to_tensor(self.g_cl_image)

        except Exception as exc:
            logging.exception("Failed to convert image to tensor: %s", exc)
            return None


    # ----------------------------------------------------------------------- #
    # REPRESENTATION HELPERS (optional)
    # ----------------------------------------------------------------------- #

    def __repr__(self) -> str:
        """
        Return a concise representation that includes the size of the stored
        image if it exists.
        """
        if self.g_cl_image is not None:
            return (
                f"{self.__class__.__name__}(image={self.g_cl_image.size[0]}x{self.g_cl_image.size[1]})"
            )
        else:
            return f"{self.__class__.__name__}()"



# --------------------------------------------------------------------------- #
# TEST BENCH
# --------------------------------------------------------------------------- #

#from st_image import St_image
if __name__ == "__main__":
    st = St_image(
        i_w_card_mm=63.5,
        i_h_card_mm = 88.9,
        i_dot_per_inch = 300
    )

    st.save_image(["output", "test_bench_st_image"])   # creates output/card.png
