# Character Sheet Generator Node

This sets of nodes for ComfyUI takes an image and a D&D5E character sheet and generate a character sheet card meant for NPCs

# WORKFLOW

![](/WORKFLOW-orso-character-sheet-generator.png)

# comfyui-orso-character-sheet-generator

A ComfyUI custom node extension for generating **printable D&D 5th Edition NPC character sheets** as card-sized (63.5mm × 88.9mm) front-and-back images.

## Features

- **Front side**: NPC illustration, name, race, Challenge Rating (CR), Armor Class (AC), and Hit Points (HP)
- **Back side**: Full stat block with ability modifiers, skill proficiencies, resistances, immunities, weaknesses, spellcasting info, and custom actions/abilities
- **Scalable layout**: All positions use parts-per-thousand (ppt) coordinates, making layouts resolution-independent
- **Multi-language layouts**: English and Italian layout files included
- **Mask overlays**: Front and back mask images for visual styling (opacity adjustable)
- **Print-ready output**: Configurable DPI (default 300) and card dimensions

## Installation

1. Place this extension in your ComfyUI custom nodes directory:
   ```
   ComfyUI/custom_nodes/comfyui-orso-character-sheet-generator/
   ```
2. Restart ComfyUI.

## Nodes

### 1. D&D5E NPC Sheet Generator

The main node that combines all inputs into a final character sheet image.

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `i_w_card_width_mm` | FLOAT | 63.5 | Card width in millimeters |
| `i_h_card_height_mm` | FLOAT | 88.9 | Card height in millimeters |
| `i_n_dots_per_inch` | INT | 300 | Output DPI for print quality |
| `image` | IMAGE | — | NPC illustration (from any image generation workflow) |
| `i_s_npc_json` | STRING | — | NPC stat block data as JSON (multiline) |
| `i_ls_layout_file_path` | STRING | `layout/npc_layout_en.json` | Layout JSON file defining text/attribute positions |
| `i_ls_mask_front_path` | STRING | `mask/front_mask.png` | Front overlay mask image |
| `i_ls_mask_back_path` | STRING | `mask/back_mask.png` | Back overlay mask image |

**Output:**
- `card_image` (IMAGE) — Combined front/back character sheet tensor

---

### 2. D&D5E NPC STAT BLOCK

Generates the NPC JSON data from individual input fields. Use this to define your NPC's stats, skills, and flavor text.

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | STRING | "Olivia Prezzo" | NPC name |
| `race` | STRING | "Halfling - Lightfoot" | Species |
| `cr` | STRING | "5" | Challenge Rating |
| `hp` | INT | 50 | Hit Points |
| `ac` | INT | 16 | Armor Class |
| `speed` | STRING | "Walk: 6sq" | Movement speed |
| `image_prompt` | STRING | — | Prompt used to generate the NPC illustration |
| `description` | STRING | — | NPC background/flavor text |
| `resources` | STRING | — | Action economy (Actions, Bonus Actions, etc.) |
| `spellcasting` | STRING | — | Spellcasting info (ability, list, DC, slots) |
| `immunity` | STRING | "Poison" | Damage immunities |
| `resistance` | STRING | "Acid" | Damage resistances |
| `weakness` | STRING | "Holy, Blunt, Fire" | Damage vulnerabilities |
| `proficiency` | INT | 3 | Proficiency bonus |
| `initiative` | INT | 3 | Initiative modifier |
| All 6 ability scores + saves + skills | INT | — | Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma with saves and skill modifiers |
| `ability` *(optional)* | STRING | — | Pre-existing abilities JSON to append to |

**Output:**
- `STRING` — Complete NPC JSON

---

### 3. D&D5E NPC ABILITY

Appends a single ability/action to the NPC's ACTIONS list. Chain multiple instances together to build up the full ability list.

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `action_name` | STRING | "Master Alchemist" | Name of the ability |
| `action_text` | STRING | — | Effect description |
| `action_flavor` | STRING | — | Flavor text / lore |
| `abilities_in` *(optional)* | STRING | — | Previous abilities JSON (for chaining) |

**Output:**
- `abilities_out` (STRING) — Updated abilities JSON

---

## Workflow

```
┌─────────────────────────┐
│  D&D5E NPC STAT BLOCK   │
│  (define NPC stats)      │
└───────────┬─────────────┘
            │ STRING (JSON)
            │
            ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│  D&D5E NPC ABILITY ×N   │──────▶│    (chain as needed)     │
│  (add abilities/actions) │       └───────────┬─────────────┘
└─────────────────────────┘                   │ STRING (JSON)
                                              │
┌─────────────────────────┐                   │
│   Image Generation      │                   │
│   (any workflow)        │                   │
│   NPC illustration      │                   │
└───────────┬─────────────┘                   │
            │ IMAGE                           │
            │                                 │
            ▼                                 ▼
┌─────────────────────────────────────────────────────────┐
│          D&D5E NPC Sheet Generator                      │
│                                                         │
│  Inputs:                                                │
│    • IMAGE  — NPC illustration                          │
│    • STRING — NPC JSON (stats + abilities)              │
│    • STRING — Layout file path                          │
│    • STRING — Front mask path                           │
│    • STRING — Back mask path                            │
│    • FLOAT  — Card width (mm)                           │
│    • FLOAT  — Card height (mm)                          │
│    • INT    — DPI                                       │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │  card_image   │
                  │  (IMAGE)      │
                  └───────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │  Save Image   │
                  │  (printable)  │
                  └───────────────┘
```

### Step-by-step

1. **Define your NPC** using the **D&D5E NPC STAT BLOCK** node — fill in name, race, stats, skills, resistances, description, etc.

2. **Add abilities/actions** using one or more **D&D5E NPC ABILITY** nodes — chain them together to build up the ACTIONS list. Feed the output of one into the `abilities_in` input of the next.

3. **Generate an NPC illustration** using any image generation workflow (AnimateDiff, SDXL, etc.). The illustration should be a full-body portrait suitable for a card front.

4. **Feed everything into the Sheet Generator** node along with:
   - The layout JSON file (defines where text and stats appear on each side)
   - Front and back mask images (visual overlays for styling)
   - Card dimensions and DPI settings

5. **Save the output** — the result is a combined front/back character sheet ready for printing.

---

## Project Structure

```
comfyui-orso-character-sheet-generator/
├── __init__.py                          # Node registration
├── cl_orso_character_sheet_generator_comfyui_bindings.py   # ComfyUI node classes
├── pyproject.toml                       # Project metadata
├── font/
│   └── CormorantGaramond-BoldItalic.ttf # Fantasy-style font
├── layout/
│   ├── npc_layout_en.json               # English layout definition
│   └── npc_layout_it.json               # Italian layout definition
├── mask/
│   ├── front_mask.png                   # Front overlay mask
│   └── back_mask.png                    # Back overlay mask
└── lib/
    ├── cl_generator.py                  # Core sheet generation logic
    ├── cl_npc.py                        # NPC JSON data loader
    ├── cl_multiline_text.py             # Text wrapping & rendering
    ├── cl_pil_tensor_convert.py         # PIL ↔ Tensor conversion
    ├── cl_utility_path.py               # Cross-platform path utilities
    ├── st_image.py                      # Image container (mm/px/dpi metadata)
    └── st_attribute_ability.py          # Attribute/ability dataclass
```

---

## Layout JSON Format

Layout files define the appearance of each character sheet. They use **parts-per-thousand (ppt)** coordinates for resolution-independent positioning.

### Key sections:

| Section | Purpose |
|---------|---------|
| `FRONT_TEXT_BOXES` | Text fields on the front (name, race, CR, AC, HP) |
| `text_boxes` | Text fields on the back (description, resources, spellcasting, etc.) |
| `attributes_and_abilities` | Ability scores, saves, and skill modifiers on the back |
| `ACTIONS` | Configuration for rendering the actions/abilities section |

### Field properties:

- `s_name`: Key name matching the NPC JSON field
- `w_top_left_ppt / h_top_left_ppt`: Position as ppt of card size
- `w_size_ppt / h_size_ppt`: Box dimensions as ppt (0 = auto-height)
- `h_font_ppt`: Font size as ppt of card height
- `t_text_color`: RGB text color tuple

---

## Dependencies

- ComfyUI
- Pillow (PIL)
- PyTorch / torchvision

---

## Links

- **Repository**: https://github.com/OrsoEric/comfyui-orso-character-sheet-generator
- **Bug Tracker**: https://github.com/OrsoEric/comfyui-orso-character-sheet-generator/issues

---