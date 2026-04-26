# python src\test_k_card_back_class.py

"""
Class for generating NPC character sheet images from JSON layout definitions.

This module provides a class that combines the functionality of loading
card layouts from JSON and rendering them into PIL Images.
"""

import logging

import json
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path

import PIL.Image as image
import PIL.ImageDraw as draw
import PIL.ImageFont as font

from .cl_utility_path import convert_to_path
#from lib.st_attribute_ability import St_attribute_ability
from .st_image import St_image
#this utility allows to draw a multiline text box onto an image
from .cl_multiline_text import Cl_multiline_text
#load the individual NPC stats
from .cl_npc import Cl_npc

from .cl_utility_path import find_file_pair_image_json

from .cl_utility_path import build_path_output_jpg

class Cl_npc_character_sheet_generator:
    """
    A class for generating NPC character sheet images from JSON layout definitions.
    
    This class encapsulates the functionality to load card layouts from JSON files
    and render them into PIL Images with proper positioning and font handling.
    """

    # Default colors for the generated images
    CN_DEFAULT_BACKGROUND_COLOR: Tuple[int, int, int] = (255, 255, 255)  # white
    CN_DEFAULT_BORDER_COLOR: Tuple[int, int, int] = (0, 0, 0)            # black
    CN_BORDER_WIDTH: int = 5

    def __init__(
        self,
        i_w_card_width_mm: float,
        i_h_card_height_mm: float,
        i_n_dots_per_inch : int,
        i_s_comfy_root : str,
        i_background_color: Optional[Tuple[int, int, int]] = None,
        i_border_color: Optional[Tuple[int, int, int]] = None
    ):
        """
        Initialize the character sheet generator with card dimensions and colors.
        
        Parameters
        ----------
        i_card_width : int
            Width of the card in pixels.
        i_card_height : int
            Height of the card in pixels.
        i_background_color : tuple[int, int, int] or None, default=None
            RGB background colour.  If ``None`` a default white is used.
        i_border_color : tuple[int, int, int] or None, default=None
            RGB border colour.  If ``None`` a default black is used.
        """

        self.g_w_card_width_mm: float = i_w_card_width_mm
        self.g_h_card_height_mm: float = i_h_card_height_mm
        self.g_n_dots_per_inch: int = i_n_dots_per_inch
        #root of the comfyi extension
        self.g_s_comfy_root = Path( i_s_comfy_root )

        self.g_tn_background_color: Tuple[int, int, int] = (
            i_background_color or self.CN_DEFAULT_BACKGROUND_COLOR
        )

        self.g_tn_border_color: Tuple[int, int, int] = (
            i_border_color or self.CN_DEFAULT_BORDER_COLOR
        )

        self.g_cl_image_card : St_image = St_image(
            i_w_card_mm = self.g_w_card_width_mm *2,
            i_h_card_mm = self.g_h_card_height_mm,
            i_dot_per_inch = self.g_n_dots_per_inch
        )

        self.g_cl_image_card_front : St_image = St_image(
            i_w_card_mm = self.g_w_card_width_mm,
            i_h_card_mm = self.g_h_card_height_mm,
            i_dot_per_inch = self.g_n_dots_per_inch
        )

        self.g_cl_image_card_back : St_image = St_image(
            i_w_card_mm = self.g_w_card_width_mm,
            i_h_card_mm = self.g_h_card_height_mm,
            i_dot_per_inch = self.g_n_dots_per_inch
        )

        #s_node_root_folder = Path(__file__).resolve().parent.parent
        #print(f"D&D Generator Parent Directory {s_node_root_folder}")

        self.s_font_bold_path = self.g_s_comfy_root / convert_to_path(["font","CormorantGaramond-BoldItalic.ttf"])
        print(f"loading font from node font folder: >{self.s_font_bold_path}<")

        self.g_t_stroke = (200,200,250)

        return

    def load_layout_from_json(
        self,
        i_file_path: str,
    ) -> List[Dict[str, Any]]:
        """
        Load the card layout specification from a JSON file.
        
        Parameters
        ----------
        i_file_path : str
            Path to the JSON file that contains the layout definition.

        Returns
        -------
        list[dict]
            A list where each element represents a single layout item.
            The dictionary keys are the ones used in the JSON
            (e.g. ``s_name``, ``w_pos`` …).
        """
        with open(i_file_path, "r", encoding="utf-8") as cl_file:
            ln_layout_data = json.load(cl_file)
        return ln_layout_data

    def draw_layout_front_to_image(
        self,
        i_ld_layout: List[Dict[str, Any]],
        i_cl_image : St_image
    ) -> bool:
        """
        """

        w_size_px = i_cl_image.g_w_card_px
        h_size_px = i_cl_image.g_h_card_px

        try:
            ast_text_boxes = i_ld_layout["FRONT_TEXT_BOXES"]
        except KeyError:
            logging.error("ERR: field doesn't exist, json is wrong")
            return True #ERROR

        #cursor
        w_cursor : int = 0
        h_cursor : int = 0

        for st_text_box in ast_text_boxes:
            logging.debug(f"Front Text Box {st_text_box}")
            #TODO: I should make this into a structure
            #load text box parameters
            s_label: str = st_text_box.get("s_name", "") 
            s_text: str = st_text_box.get("s_text", "")
            w_top_left_ppt: int = st_text_box.get("w_top_left_ppt", 0)
            h_top_left_ppt: int = st_text_box.get("h_top_left_ppt", 0)
            w_size_ppt: int = st_text_box.get("w_size_ppt", 0)
            h_size_ppt: int = st_text_box.get("h_size_ppt", 0)
            h_font_ppt: int = int(st_text_box.get("h_font_ppt", 0))
            
            # Convert PPT values to pixels
            w_top_left_px = int(w_size_px * w_top_left_ppt / 1000)
            h_top_left_px = int(h_size_px * h_top_left_ppt / 1000)
            w_text_box_px = int(w_size_px * w_size_ppt / 1000)
            
            h_font_px = int(h_size_px * h_font_ppt / 1000)

            #0 height mean that the text box renderer with automatically calculate and return height
            if (h_size_ppt <= 0):
                h_text_box_px = 0

                h_rendered = Cl_multiline_text.render_fixed_size_text_box_center(
                    i_cl_imgage = i_cl_image.g_cl_image,
                    i_s_text = s_text,
                    i_w_margin = w_top_left_px,
                    i_h_margin = h_cursor,
                    i_w_border = w_text_box_px,
                    i_h_border = 0,
                    i_s_font_name = self.s_font_bold_path,
                    i_n_font_size = h_font_px,
                    i_tn_color = (0, 0, 0),
                    i_n_padding = 5,
                    i_x_draw_border = False,
                    i_tn_border_color = (255,0,0)
                )

                h_cursor = h_cursor + h_rendered

            #height is given
            else:
                h_text_box_px = int( h_size_px * h_size_ppt / 1000)    

                h_rendered = Cl_multiline_text.render_fixed_size_text_box_center(
                    i_cl_imgage = i_cl_image.g_cl_image,
                    i_s_text = s_text,
                    i_w_margin = w_top_left_px,
                    i_h_margin = h_top_left_px,
                    i_w_border = w_text_box_px,
                    i_h_border = h_text_box_px,
                    i_s_font_name = self.s_font_bold_path,
                    i_n_font_size = h_font_px,
                    i_tn_color = (0, 0, 0),
                    i_n_padding = 5,
                    i_x_draw_border = False,
                    i_tn_border_color = (255,0,0)
                )

                #move the cursor
                h_cursor = h_top_left_px + h_text_box_px

        return False #SUCCESS

    def draw_layout_back_to_image(
        self,
        i_ld_layout: List[Dict[str, Any]],
        i_cl_image : St_image
    ) -> bool:
        """
        Draw the layout described by *i_layout* onto a new PIL Image.
        
        Parameters
        ----------
        i_layout : list[dict]
            The list of layout items as returned by
            :func:`load_layout_from_json`.

        Returns
        -------
        PIL.Image.Image
            An image that contains the drawn layout.
        """
        # Create base image and drawing context
        cl_draw = draw.Draw(i_cl_image.g_cl_image)

        w_size_px = i_cl_image.g_w_card_px
        h_size_px = i_cl_image.g_h_card_px

        # Draw a simple rectangle border
        if False:
            cl_draw.rectangle(
                [
                    (self.CN_BORDER_WIDTH, self.CN_BORDER_WIDTH),
                    (
                        w_size_px - self.CN_BORDER_WIDTH,
                        h_size_px - self.CN_BORDER_WIDTH,
                    ),
                ],
                outline=self.g_tn_border_color,
                width=self.CN_BORDER_WIDTH,
            )

        # Default font – Pillow will fallback to a built‑in one if the path is wrong
        cl_default_font = font.load_default()

        try:
            ast_abilities = i_ld_layout["attributes_and_abilities"]
        except KeyError:
            print("ERR: field doesn't exist, json is wrong")
            return True #ERROR

        try:
            ast_text_boxes = i_ld_layout["text_boxes"]
        except KeyError:
            print("ERR: field doesn't exist, json is wrong")
            return True #ERROR

        #cursor
        w_cursor : int = 0
        h_cursor : int = 0

        # Render each layout item; skip anything that isn't a dict
        for st_item in ast_abilities:

            # PPT part per thousand of the whole image
            # This way it's scale independent
            s_text: str = st_item.get("s_name", "")
            w_pos_ppt: int = st_item.get("w_pos_ppt", 0)
            h_pos_ppt: int = st_item.get("h_pos_ppt", 0)
            h_font_ppt: int = st_item.get("h_font_ppt", 0)
            n_value : int = st_item.get("n_value",-99)
            
            # Convert PPT values to pixels
            w_pos_px = w_size_px * w_pos_ppt / 1000
            h_pos_px = h_size_px * h_pos_ppt / 1000
            h_font_px = h_size_px * h_font_ppt / 1000

            # Load a truetype font if possible, otherwise fall back to the default
            try:
                cl_item_font = font.truetype(
                    self.s_font_bold_path,
                    int(h_font_px),
                )
            except OSError:
                cl_item_font = cl_default_font
                print("ERR: failed to load font")

            if (h_cursor <= 0):
                w_cursor = w_pos_px
                h_cursor = h_pos_px
            else:
                w_cursor += w_pos_px
                h_cursor += h_pos_px

            # Add the header for the attribute or ability 
            cl_draw.text((w_cursor+2, h_cursor), s_text, fill=(0, 0, 0), font=cl_item_font, stroke_width=1,
                stroke_fill=self.g_t_stroke)
            # Fetch the numerical value of attribute or ability
            if (n_value>=0):
                cl_draw.text((w_cursor, h_cursor), f"+{n_value}", fill=(0, 0, 0), font=cl_item_font, anchor="ra",stroke_width=1,
                stroke_fill=self.g_t_stroke)
            else: 
                cl_draw.text((w_cursor, h_cursor), f"{n_value}", fill=(0, 0, 0), font=cl_item_font, anchor="ra",stroke_width=1,
                stroke_fill=self.g_t_stroke)


        #cursor
        w_cursor = 0
        h_cursor = 0

        for st_text_box in ast_text_boxes:
            logging.debug(f"drawing text box: {st_text_box}")
            #TODO: I should make this into a structure
            #load text box parameters
            s_label: str = st_text_box.get("s_name", "") 
            s_text: str = st_text_box.get("s_text", "")
            w_top_left_ppt: int = st_text_box.get("w_top_left_ppt", 0)
            h_top_left_ppt: int = st_text_box.get("h_top_left_ppt", 0)
            w_size_ppt: int = st_text_box.get("w_size_ppt", 0)
            h_size_ppt: int = st_text_box.get("h_size_ppt", 0)
            h_font_ppt: int = int(st_text_box.get("h_font_ppt", 0))

            t_text_color: Tuple[int,int,int] = st_text_box.get("t_text_color", (0,0,0)) 
            
            # Convert PPT values to pixels
            w_top_left_px = int(w_size_px * w_top_left_ppt / 1000)
            h_top_left_px = int(h_size_px * h_top_left_ppt / 1000)
            w_text_box_px = int(w_size_px * w_size_ppt / 1000)
            
            h_font_px = int(h_size_px * h_font_ppt / 1000)

            #0 height mean that the text box renderer with automatically calculate and return height
            if (h_size_ppt <= 0):
                h_text_box_px = 0

                h_rendered = Cl_multiline_text.render_fixed_size_text_box(
                    i_cl_imgage = i_cl_image.g_cl_image,
                    i_s_text = s_text,
                    i_w_margin = w_top_left_px,
                    i_h_margin = h_cursor,
                    i_w_border = w_text_box_px,
                    i_h_border = 0,
                    i_s_font_name = self.s_font_bold_path,
                    i_n_font_size = h_font_px,
                    i_tn_color = t_text_color,
                    i_n_padding = 5,
                    i_x_draw_border = False,
                    i_tn_border_color = (255,0,0),
                    i_n_stroke = 1,
                    i_tn_stroke_color = self.g_t_stroke
                )

                h_cursor = h_cursor + h_rendered


            #height is given
            else:
                h_text_box_px = int( h_size_px * h_size_ppt / 1000)    

                h_rendered = Cl_multiline_text.render_fixed_size_text_box(
                    i_cl_imgage = i_cl_image.g_cl_image,
                    i_s_text = s_text,
                    i_w_margin = w_top_left_px,
                    i_h_margin = h_top_left_px,
                    i_w_border = w_text_box_px,
                    i_h_border = h_text_box_px,
                    i_s_font_name = self.s_font_bold_path,
                    i_n_font_size = h_font_px,
                    i_tn_color = t_text_color,
                    i_n_padding = 5,
                    i_x_draw_border = False,
                    i_tn_border_color = (255,0,0),
                    i_n_stroke = 1,
                    i_tn_stroke_color = self.g_t_stroke
                )

                #move the cursor
                h_cursor = h_top_left_px + h_text_box_px

            #render the text box

        return False #OK
    
    def load_values_front_from_npc_dict( self, i_ld_layout : Dict, i_d_npc : Dict ) -> bool:
        """
        given a npc dictionary, fill the values from the layout file
        """

        #copy the dictionary key from the NPC over to the layout value field
        ls_npc_key = i_d_npc.keys()

        try:
            ld_text_boxes : List[Dict] = i_ld_layout["FRONT_TEXT_BOXES"]
        except KeyError:
            logging.error(f"ERR: field {"FRONT_TEXT_BOXES"} doesn't exist, json is wrong")
            return True #ERROR

        #scan the layout text fields
        for d_attribute in ld_text_boxes:
            #fetch the name of the attribute
            s_attribute = d_attribute["s_name"] 
            #check that the name of the attribute is amongst the NPC stats
            if s_attribute in ls_npc_key:
                #then copy over the value
                d_attribute["s_text"] = i_d_npc[s_attribute]
                logging.debug(f"NPC value {s_attribute} assigned to layout value {d_attribute}")
            else:
                logging.error(f"ERR: unable to find attributr {s_attribute} in layout keys {ls_npc_key}")
                return True #FAIL
            
        logging.debug(f"FRONT: Loaded {len(ld_text_boxes)} text boxes")

        return False #OK

    def load_values_back_from_npc_dict( self, i_ld_layout : Dict, i_d_npc : Dict ) -> bool:
        """
        given a npc dictionary, fill the values from the layout file
        """

        #if a value is both on layout and on NPC
        #copy the dictionary key from the NPC over to the layout value field

        ls_npc_key = i_d_npc.keys()

        ld_attributes_and_abilities : List[Dict] = i_ld_layout["attributes_and_abilities"]
        logging.debug(f"Layout: {ld_attributes_and_abilities}")

        #scan the layout attribute fields
        for d_attribute in ld_attributes_and_abilities:
            #fetch the name of the attribute
            s_attribute = d_attribute["s_name"] 
            #check that the name of the attribute is amongst the NPC stats
            if s_attribute in ls_npc_key:
                #then copy over the value
                d_attribute["n_value"] = i_d_npc[s_attribute]
                logging.debug(f"NPC value {s_attribute} assigned to layout value {d_attribute}")
            else:
                logging.error(f"ERR: unable to find attributr {s_attribute} in layout keys {ls_npc_key}")
                return True #FAIL

        ld_text_boxes : List[Dict] = i_ld_layout["text_boxes"]

        #scan the layout text fields
        for d_attribute in ld_text_boxes:
            #fetch the name of the attribute
            s_attribute = d_attribute["s_name"] 
            #check that the name of the attribute is amongst the NPC stats
            if s_attribute in ls_npc_key:
                #then copy over the value
                d_attribute["s_text"] = i_d_npc[s_attribute]
                logging.debug(f"NPC value {s_attribute} assigned to layout value {d_attribute}")
            else:
                logging.error(f"ERR: unable to find attributr {s_attribute} in layout keys {ls_npc_key}")
                return True #FAIL

        logging.debug(f"text boxes: {len(ld_text_boxes)}")

        #ACTIONS
        #I spawn a text box for the action title
        #I spawn a text box for the action text
        #TODO: eventually I'd like text SVG for damage types and dice but it gets difficult

        try:
            st_layout_action = i_ld_layout["ACTIONS"]
        except KeyError:
            print("ERR: field doesn't exist, json is wrong")
            return True #ERROR

        h_font_title_ppt = st_layout_action["h_font_title_ppt"]
        h_font_body_ppt = st_layout_action["h_font_body_ppt"]
        h_font_flavor_text_ppt = st_layout_action["h_font_flavor_text_ppt"]

        #load the actions from the NPC
        ld_action_npc = i_d_npc["ACTIONS"]

        for d_action_npc in ld_action_npc:
            logging.info(f"Processing NPC action: {d_action_npc}")

            # Ensure there is at least one existing text box to copy from
            if not ld_text_boxes:
                logging.error("No template text box available to clone")
                return True  # ERROR

            # ---------- Header text box (s_name) ----------
            d_header_box = dict(ld_text_boxes[-1])     
            d_header_box["s_name"] = f"ACTION{0}"
            d_header_box["s_text"] = d_action_npc.get("s_name", "ERR:Failed to load")
            d_header_box["h_font_ppt"] = h_font_title_ppt
            d_header_box["t_text_color"] = (200,75,50)

            ld_text_boxes.append(d_header_box)
            logging.debug(f"Added header text box: {d_header_box}")

            # ---------- Body text box (s_text) ----------
            d_body_box = dict(ld_text_boxes[-1])      
            d_body_box["s_name"] = f"ACTION{0}"
            d_body_box["s_text"] = d_action_npc.get("s_text", "ERR:Failed to load")
            #auto height
            d_body_box["h_size_ppt"] = 0
            d_body_box["h_font_ppt"] = h_font_body_ppt
            d_body_box["t_text_color"] = (0,0,0)
            ld_text_boxes.append(d_body_box)
            logging.debug(f"Added body text box: {d_body_box}")

            # ---------- Description text box (s_action) ----------
            d_description_box = dict(ld_text_boxes[-1])   
            d_description_box["s_name"] = f"ACTION{0}"
            d_description_box["s_text"] = d_action_npc.get("s_flavor", "ERR:Failed to load")
            d_description_box["h_font_ppt"] = h_font_flavor_text_ppt
            d_description_box["t_text_color"] = (80,80,80)
            ld_text_boxes.append(d_description_box)
            logging.debug(f"Added description text box: {d_description_box}")

        logging.debug(f"text boxes: {len(ld_text_boxes)}")

        return False  # SUCCESS

    def generate_card(
        self,
        i_ls_layout_file_path: List[str],
        i_ls_mask_front_path : List[str],
        i_ls_mask_back_path : List[str],
        i_ls_npc_illustration_path : List[str] | Path,
        i_ls_npc_json_path: List[str] | Path,
        i_ls_output_file_path: List[str] | Path,
        i_background_color: Optional[Tuple[int, int, int]] = None,
        i_border_color: Optional[Tuple[int, int, int]] = None
    ) -> bool:
        """
        Generate a card back image from the specified JSON layout file.
        
        Parameters
        ----------
        i_layout_file_path : list[str]
            Path components to the JSON file that defines the layout.
        i_output_file_path : str
            Path where the generated image will be saved.
        i_background_color : tuple[int, int, int] or None, default=None
            RGB background colour.  If ``None`` a default white is used.
        i_border_color : tuple[int, int, int] or None, default=None
            RGB border colour.  If ``None`` a default black is used.

        Returns
        -------
        PIL.Image.Image
            The generated image object.
        """
        
        #SIZE of the image
        t_size_front = self.g_cl_image_card_back.get_size()

        #----------------------------------------------------------------------
        #   LOAD JSON
        #----------------------------------------------------------------------

        # Load the layout from JSON
        st_layout = self.load_layout_from_json(convert_to_path(i_ls_layout_file_path))

        # Load the NPC stats
        cl_npc : Cl_npc = Cl_npc()
        cl_npc.load_from_file( i_ls_npc_json_path )
        logging.debug(f"Loading NPC from file: {cl_npc}")

        #----------------------------------------------------------------------
        #   DRAW: FRONT ILLUSTRATION
        #----------------------------------------------------------------------

        #create an image for the NPC ilustration
        cl_npc_illustration : St_image = St_image(
            i_w_card_mm = self.g_w_card_width_mm,
            i_h_card_mm = self.g_h_card_height_mm,
            i_dot_per_inch = self.g_n_dots_per_inch
        )

        #load the NPC illustration and resize it
        cl_npc_illustration.load_image( i_ls_npc_illustration_path )

        #draw NPC illustration on the front
        self.g_cl_image_card_front.draw_image( cl_npc_illustration, (0,0), t_size_front )

        #----------------------------------------------------------------------
        #   DRAW: FRONT MASK
        #----------------------------------------------------------------------

        #create an image for the NPC ilustration
        cl_front_mask : St_image = St_image(
            i_w_card_mm = self.g_w_card_width_mm,
            i_h_card_mm = self.g_h_card_height_mm,
            i_dot_per_inch = self.g_n_dots_per_inch
        )

        #load the NPC illustration and resize it
        cl_front_mask.load_image( i_ls_mask_front_path )

        self.g_cl_image_card_front.compose_image( cl_front_mask, 0.6 )

        #cl_front_mask.g_cl_image.convert('RGBA')

        #draw NPC illustration on the front
        #self.g_cl_image_card_front.draw_image( cl_front_mask, (0,0), t_size_front )

        #----------------------------------------------------------------------
        #   DRAW: BACK MASK
        #----------------------------------------------------------------------

        #create an image for the NPC ilustration
        cl_back_mask : St_image = St_image(
            i_w_card_mm = self.g_w_card_width_mm,
            i_h_card_mm = self.g_h_card_height_mm,
            i_dot_per_inch = self.g_n_dots_per_inch
        )

        #load the NPC illustration and resize it
        cl_back_mask.load_image( i_ls_mask_back_path )

        self.g_cl_image_card_back.compose_image( cl_back_mask, 1.0 )

        #----------------------------------------------------------------------
        #   DRAW: FRONT
        #----------------------------------------------------------------------

        x_fail = self.load_values_front_from_npc_dict( st_layout , cl_npc.g_d_npc )
        if x_fail:
            logging.error("failed to load values from NPC into FRONT layout.")
            return True #FAIL


        #Draw layout front to image
        x_fail = self.draw_layout_front_to_image(
            st_layout,
            self.g_cl_image_card_front
        )
        if x_fail:
            logging.error("ERR: failed to draw back layout to FRONT image")
            return True #FAIL


        #----------------------------------------------------------------------
        #   DRAW: BACK
        #----------------------------------------------------------------------

        x_fail = self.load_values_back_from_npc_dict( st_layout , cl_npc.g_d_npc )
        if x_fail:
            logging.error("failed to load values from NPC into back layout.")
            return True #FAIL

        # Draw the layout to an image
        x_fail = self.draw_layout_back_to_image(
            st_layout,
            self.g_cl_image_card_back
        )
        if x_fail:
            logging.error("ERR: failed to draw back layout to back image")
            return True #FAIL

        #----------------------------------------------------------------------
        #   DRAW: COMBINE FRONT AND BACK
        #----------------------------------------------------------------------        

        #i_ls_mask_front_path

        self.g_cl_image_card.draw_image( self.g_cl_image_card_front, (0,0), t_size_front )

        #draw the back on the main image with offset
        t_size_back = self.g_cl_image_card_back.get_size()
        self.g_cl_image_card.draw_image( self.g_cl_image_card_back, (t_size_back[0],0), t_size_back )

        cl_draw = draw.Draw(self.g_cl_image_card.g_cl_image)

        # Draw a vertical line that spans the full height of the composite.
        cl_draw.line(
            xy=((t_size_back[0], 0), (t_size_back[0], t_size_back[1])),
            fill=(0, 0, 0),
            width=4
        )

        # Save the image
        self.g_cl_image_card.save_image(i_ls_output_file_path, i_s_format="JPEG")
        logging.info(f"savec output at {i_ls_output_file_path}")
        
        return False #OK
    
    def generate_comfy_ui(
        self,
        i_cl_npc_illustration: St_image,
        i_d_npc_json: dict,

        i_ls_layout_file_path: List[str],
        i_ls_mask_front_path: List[str],
        i_ls_mask_back_path: List[str],

        i_background_color: Optional[Tuple[int, int, int]] = None,
        i_border_color: Optional[Tuple[int, int, int]] = None
    ) -> St_image:
        """
        Generate a combined front/back card image using already-loaded
        NPC illustration and NPC JSON data (for ComfyUI pipelines).

        Parameters
        ----------
        i_cl_npc_illustration : St_image
            Already-loaded NPC illustration image.
        i_d_npc_json : dict
            NPC data already loaded (instead of loading from file).
        i_ls_layout_file_path : list[str]
            Path components to the JSON layout file.
        i_ls_mask_front_path : list[str]
            Path to the front mask image.
        i_ls_mask_back_path : list[str]
            Path to the back mask image.

        Returns
        -------
        St_image
            The final combined card image (front + back).
        """

        # SIZE of the image
        t_size_front = self.g_cl_image_card_back.get_size()

        #----------------------------------------------------------------------
        #   LOAD JSON LAYOUT
        #----------------------------------------------------------------------
        
        
        s_file_layout = self.g_s_comfy_root / i_ls_layout_file_path
        print(f"Load D&D Layout from : {s_file_layout}")
        st_layout = self.load_layout_from_json(s_file_layout)

        #----------------------------------------------------------------------
        #   LOAD NPC DATA (already provided)
        #----------------------------------------------------------------------
        
        cl_npc = Cl_npc()
        cl_npc.g_d_npc = i_d_npc_json
        logging.debug(f"Loaded NPC from dict: {cl_npc}")

        #----------------------------------------------------------------------
        #   DRAW: FRONT ILLUSTRATION
        #----------------------------------------------------------------------
        
        self.g_cl_image_card_front.draw_image(i_cl_npc_illustration, (0, 0), t_size_front)

        #----------------------------------------------------------------------
        #   DRAW: FRONT MASK
        #----------------------------------------------------------------------
        
        cl_front_mask = St_image(
            i_w_card_mm=self.g_w_card_width_mm,
            i_h_card_mm=self.g_h_card_height_mm,
            i_dot_per_inch=self.g_n_dots_per_inch
        )
        
        s_file_front = self.g_s_comfy_root / i_ls_mask_front_path
        print(f"Load D&D Front Image : {s_file_front}")
        cl_front_mask.load_image(s_file_front)
        self.g_cl_image_card_front.compose_image(cl_front_mask, 0.6)

        #----------------------------------------------------------------------
        #   DRAW: BACK MASK
        #----------------------------------------------------------------------
        
        cl_back_mask = St_image(
            i_w_card_mm=self.g_w_card_width_mm,
            i_h_card_mm=self.g_h_card_height_mm,
            i_dot_per_inch=self.g_n_dots_per_inch
        )
        s_file_back = self.g_s_comfy_root / i_ls_mask_back_path
        print(f"Load D&D Back Image : {s_file_back}")
        cl_back_mask.load_image(s_file_back)
        self.g_cl_image_card_back.compose_image(cl_back_mask, 1.0)

        #----------------------------------------------------------------------
        #   DRAW: FRONT TEXT
        #----------------------------------------------------------------------
        if self.load_values_front_from_npc_dict(st_layout, cl_npc.g_d_npc):
            logging.error("Failed to load NPC values into FRONT layout.")
            return None

        if self.draw_layout_front_to_image(st_layout, self.g_cl_image_card_front):
            logging.error("Failed to draw FRONT layout.")
            return None

        #----------------------------------------------------------------------
        #   DRAW: BACK TEXT
        #----------------------------------------------------------------------
        if self.load_values_back_from_npc_dict(st_layout, cl_npc.g_d_npc):
            logging.error("Failed to load NPC values into BACK layout.")
            return None

        if self.draw_layout_back_to_image(st_layout, self.g_cl_image_card_back):
            logging.error("Failed to draw BACK layout.")
            return None

        #----------------------------------------------------------------------
        #   COMBINE FRONT + BACK
        #----------------------------------------------------------------------
        t_size_back = self.g_cl_image_card_back.get_size()

        self.g_cl_image_card.draw_image(self.g_cl_image_card_front, (0, 0), t_size_front)
        self.g_cl_image_card.draw_image(self.g_cl_image_card_back, (t_size_back[0], 0), t_size_back)

        cl_draw = draw.Draw(self.g_cl_image_card.g_cl_image)
        cl_draw.line(
            xy=((t_size_back[0], 0), (t_size_back[0], t_size_back[1])),
            fill=(0, 0, 0),
            width=4
        )

        # Return the final image instead of saving it
        return self.g_cl_image_card

    @staticmethod
    def find_and_generate_cards(
        #card layout descriptor
        i_ls_layout_file_path : List[str],
        #card image frame overlay
        i_ls_mask_front_path : List[str],
        i_ls_mask_back_path : List[str],
        #pair of image and json
        i_s_input_folder : str,
        #where save output
        i_s_output_folder : str,
    ) -> bool:
        #look at the input folder, and scan for image/json files with same name, our NPCs
        ltss_npc_input_path = find_file_pair_image_json(i_s_input_folder)

        if (len(ltss_npc_input_path) < 0):
            logging.error("ERR: no valid file pair in the input folder")
            return True #FAIL

        for tss_npc_input_path in ltss_npc_input_path:
            
            #unpack
            s_input_npc_image_path = tss_npc_input_path[0]
            s_input_npc_json_path = tss_npc_input_path[1]
            logging.info(f"Processing NPC files {s_input_npc_image_path} {s_input_npc_json_path} ")

            s_output_image_path = build_path_output_jpg( i_s_output_folder, s_input_npc_image_path )
            # construct the output path
            logging.info(f"Output image path {s_output_image_path}")

            cl_generator = Cl_npc_character_sheet_generator(
                i_w_card_width_mm=63.5,
                i_h_card_height_mm=88.9,
                i_n_dots_per_inch = 300,
                i_background_color=(255, 255, 255),
                i_border_color=(0, 0, 0)
            )
            logging.info("Constructed NPC generator class...")

            # Generate the card back
            cl_generated_image = cl_generator.generate_card(
                i_ls_layout_file_path=i_ls_layout_file_path,
                i_ls_mask_front_path=i_ls_mask_front_path,
                i_ls_mask_back_path=i_ls_mask_back_path,
                i_ls_npc_illustration_path= s_input_npc_image_path,
                i_ls_npc_json_path = s_input_npc_json_path,
                i_ls_output_file_path=s_output_image_path
            )



        return False #OK