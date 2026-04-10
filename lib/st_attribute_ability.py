from dataclasses import dataclass

@dataclass
class St_attribute_ability:
    """
    One attribute or ability as defined by the layout JSON.

    Attributes
    ----------
    s_name : str
        Name of the attribute / ability (e.g. “Strength”).
    w_name_pos_px : int
        X coordinate of the name in pixels.
    h_name_pos_px : int
        Y coordinate of the name in pixels.
    s_modifier_value : str
        Text that represents the modifier (e.g. “+10”, “-3”).
    w_pos_modifier_px : int
        X coordinate for rendering the modifier text.  If not supplied by
        the layout it defaults to ``w_name_pos_px`` so the modifier is drawn
        next to its name.
    """

    s_name: str
    w_name_pos_px: int
    h_name_pos_px: int
    h_name_font : int

    s_modifier_value: str
    w_modifier_pos_px: int

