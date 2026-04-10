#2026-02-04 adaptive height of the text box
# 

# ------------------------------------------------------------------
#  Imports
# ------------------------------------------------------------------
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from typing import List
from lib.cl_utility_path import convert_to_path

# ------------------------------------------------------------------
#  Multiline Text Utility Class
# ------------------------------------------------------------------
class Cl_multiline_text:

    # --------------------------------------------------------------
    #  Font handling
    # --------------------------------------------------------------
    @staticmethod
    def load_font(
            i_font_path: str,
            i_font_size: int) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(i_font_path, i_font_size)

    # --------------------------------------------------------------
    #  Measurement helpers
    # --------------------------------------------------------------
    @staticmethod
    def measure_text_width(
            i_draw: ImageDraw.Draw,
            i_string: str,
            i_font: ImageFont.FreeTypeFont) -> int:
        return i_draw.textlength(i_string, font=i_font)

    # --------------------------------------------------------------
    #  Text wrapping
    # --------------------------------------------------------------
    @staticmethod
    def wrap_text_into_lines(
            i_text: str,
            i_max_width: int,
            i_draw: ImageDraw.Draw,
            i_font: ImageFont.FreeTypeFont
    ) -> List[str]:
        """
        Wrap the supplied text into lines that fit within ``i_max_width`` pixels.

        The function also honours explicit newline characters (``\n``).  Each
        paragraph is wrapped independently; an empty line in the source text
        results in a blank string in the returned list, preserving paragraph
        separation.

        Parameters:
            i_text (str): Raw text that may contain spaces and ``\n``.
            i_max_width (int): The maximum width of a line in pixels.
            i_draw (ImageDraw.Draw): Pillow drawing context used for measuring
                text widths.
            i_font (ImageFont.FreeTypeFont): Font used to render the text.

        Returns:
            List[str]: A list of strings, each representing a single wrapped line.
        """
        # Split on newline to get individual paragraphs.  Empty parts correspond
        # to blank lines that must be preserved in the output.
        ln_paragraphs: List[str] = i_text.split('\n')
        ln_wrapped_lines: List[str] = []

        for paragraph_index, paragraph_text in enumerate(ln_paragraphs):
            # Preserve explicit blank lines.
            if not paragraph_text:
                ln_wrapped_lines.append('')
                continue

            # Tokenise the paragraph into words.
            ln_words: List[str] = paragraph_text.split()
            st_current_line: str = ''
            for word_index, current_word in enumerate(ln_words):
                # Build a tentative line by appending the next word.
                st_tentative_line: str = f"{st_current_line} {current_word}".strip()

                # Measure whether this tentative line fits within ``i_max_width``.
                if (Cl_multiline_text.measure_text_width(
                        i_draw, st_tentative_line, i_font) <= i_max_width):
                    st_current_line = st_tentative_line
                else:
                    # The word does not fit – commit the current line and start a new one.
                    if st_current_line:
                        ln_wrapped_lines.append(st_current_line)
                    st_current_line = current_word

            # Append any remaining text after processing all words in the paragraph.
            if st_current_line:
                ln_wrapped_lines.append(st_current_line)

        return ln_wrapped_lines


    # --------------------------------------------------------------
    #  Rendering
    # --------------------------------------------------------------
    @staticmethod
    def draw_wrapped_text(
            i_draw: ImageDraw.Draw,
            i_x: int,
            i_y: int,
            i_lines: List[str],
            i_font: ImageFont.FreeTypeFont,
            i_text_color: tuple[int, int, int],
            i_line_spacing: int = 0,
            i_n_stroke: int = 1,
            i_tn_stroke_color: tuple[int, int, int] = (0, 0, 0)
    ) -> None:

        line_height: int = i_draw.textbbox(
            (0, 0), "A", font=i_font
        )[3]

        y_offset: int = 0

        for line in i_lines:
            i_draw.text(
                (i_x, i_y + y_offset),
                line,
                fill=i_text_color,
                font=i_font,
                stroke_width=i_n_stroke,
                stroke_fill=i_tn_stroke_color
            )
            y_offset += line_height + i_line_spacing

    # --------------------------------------------------------------
    #  Public API: render into an existing image
    # --------------------------------------------------------------
    @staticmethod
    def render_fixed_size_text_box(
            i_cl_imgage: Image.Image,
            i_s_text: str,
            i_w_margin: int,
            i_h_margin: int,
            i_w_border: int,
            i_h_border: int,
            i_s_font_name: str,
            i_n_font_size: int,
            i_tn_color: tuple[int, int, int] = (0, 0, 0),
            i_n_padding: int = 5,
            i_x_draw_border: bool = False,
            i_tn_border_color: tuple[int, int, int] = (0, 0, 0),
            i_n_stroke: int = 1,
            i_tn_stroke_color: tuple[int, int, int] = (0, 0, 0)
            ) -> int:
        """
        Render wrapped text into a fixed-size rectangle on an existing image.
        """


        cl_draw: ImageDraw.Draw = ImageDraw.Draw(i_cl_imgage)

        st_font = ImageFont.truetype(i_s_font_name, i_n_font_size)


        # f the height of the text box is zero, activate the adaptive height
        x_adaptive_height = (i_h_border <= 0)

        # Wrap text to inner width
        w_inner: int = i_w_border - (2 * i_n_padding)

        #text border wrapper
        ls_wrapped_lines: List[str] = (
            Cl_multiline_text.wrap_text_into_lines(
                i_text=i_s_text,
                i_max_width=w_inner,
                i_draw=cl_draw,
                i_font=st_font
            )
        )

        if (x_adaptive_height == True):
            n_lines = len(ls_wrapped_lines)
            h_text = n_lines * i_n_font_size + i_n_padding * 2
            i_h_border = h_text


        if i_n_font_size <= 0:
            print(f"ERR: invalid font size: {i_n_font_size}")
            return True 

        if i_x_draw_border:
            cl_draw.rectangle(
                [
                    i_w_margin,
                    i_h_margin,
                    i_w_margin + i_w_border,
                    i_h_margin + i_h_border
                ],
                outline=i_tn_border_color
            )

        # Render
        Cl_multiline_text.draw_wrapped_text(
            i_draw=cl_draw,
            i_x=i_w_margin + i_n_padding,
            i_y=i_h_margin + i_n_padding,
            i_lines=ls_wrapped_lines,
            i_font=st_font,
            i_text_color=i_tn_color,
            i_n_stroke = i_n_stroke,
            i_tn_stroke_color = i_tn_stroke_color
        )

        #return height of text box
        return i_h_border

    @staticmethod
    def draw_wrapped_text_center(
        i_draw: ImageDraw.Draw,
        i_x: int,
        i_y: int,
        i_box_width: int,
        i_lines: List[str],
        i_font: ImageFont.FreeTypeFont,
        i_text_color: tuple[int, int, int],
        i_line_spacing: int = 0
    ) -> None:

        # Height of a single line
        line_height: int = i_draw.textbbox((0, 0), "A", font=i_font)[3]

        y_offset: int = 0

        for line in i_lines:
            # Compute pixel width of this line
            w_line = i_draw.textlength(line, font=i_font)

            # Center horizontally inside the box
            x_centered = i_x + (i_box_width - w_line) // 2

            i_draw.text(
                (x_centered, i_y + y_offset),
                line,
                fill=i_text_color,
                font=i_font,
                stroke_width=2,
                stroke_fill=(255,255,255)
            )

            y_offset += line_height + i_line_spacing


    @staticmethod
    def render_fixed_size_text_box_center(
            i_cl_imgage: Image.Image,
            i_s_text: str,
            i_w_margin: int,
            i_h_margin: int,
            i_w_border: int,
            i_h_border: int,
            i_s_font_name: str,
            i_n_font_size: int,
            i_tn_color: tuple[int, int, int] = (0, 0, 0),
            i_n_padding: int = 5,
            i_x_draw_border: bool = False,
            i_tn_border_color: tuple[int, int, int] = (0, 0, 0)
        ) -> int:

        cl_draw: ImageDraw.Draw = ImageDraw.Draw(i_cl_imgage)
        st_font = ImageFont.truetype(i_s_font_name, i_n_font_size)

        # Adaptive height if requested
        x_adaptive_height = (i_h_border <= 0)

        # Inner width for wrapping
        w_inner: int = i_w_border - (2 * i_n_padding)

        # Wrap text
        ls_wrapped_lines: List[str] = (
            Cl_multiline_text.wrap_text_into_lines(
                i_text=i_s_text,
                i_max_width=w_inner,
                i_draw=cl_draw,
                i_font=st_font
            )
        )

        # Compute adaptive height
        if x_adaptive_height:
            n_lines = len(ls_wrapped_lines)
            line_height = cl_draw.textbbox((0, 0), "A", font=st_font)[3]
            i_h_border = n_lines * line_height + i_n_padding * 2

        if i_n_font_size <= 0:
            print(f"ERR: invalid font size: {i_n_font_size}")
            return True

        # Draw border
        if i_x_draw_border:
            cl_draw.rectangle(
                [
                    i_w_margin,
                    i_h_margin,
                    i_w_margin + i_w_border,
                    i_h_margin + i_h_border
                ],
                outline=i_tn_border_color
            )

        # Render centered text
        Cl_multiline_text.draw_wrapped_text_center(
            i_draw=cl_draw,
            i_x=i_w_margin + i_n_padding,
            i_y=i_h_margin + i_n_padding,
            i_box_width=w_inner,
            i_lines=ls_wrapped_lines,
            i_font=st_font,
            i_text_color=i_tn_color
        )

        return i_h_border


if __name__ == "__main__":
    cl_image = Image.new("RGB", (400, 300), (255, 255, 255))

    s_font_path = convert_to_path(["font","fantasy.ttf"])

    h_box = Cl_multiline_text.render_fixed_size_text_box_center(
        i_cl_imgage = cl_image,
        i_s_text = "This is a reusable multiline text box renderer This is a reusable multiline text box renderer . . ..",
        i_w_margin = 20,
        i_h_margin = 20,
        i_w_border = 250,
        i_h_border = 0,
        i_s_font_name = s_font_path,
        i_n_font_size = 18,
        i_tn_color = (127, 127, 127),
        i_n_padding = 5,
        i_x_draw_border = True,
        i_tn_border_color = (255,0,0)
    )

    print(f"W: {h_box}")

    cl_image.save("outest_i_multiline_text.png")
