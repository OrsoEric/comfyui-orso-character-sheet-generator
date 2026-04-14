# Paths

since i'm running from comfy-ui root 
I need to give custom nodes -> d&d node



# 

Now fully run, the image seems fine, but the preview image shows a I guess 1000 images 3x1500

# json

```json
{
    "system": "DnD5E",
    "actor": "NPC",
    "NAME": "Garetto Von Garra",
    "RACE": "Human Fallen Noble (Major)",

    "CR": "1/2",
    "HP": "20",
    "AC": "12",
    "SPEED": "SPEED: Walk: 6sq",

    "IMAGE PROMPT" : "Portrait AR1:1.5. Digital, semi-realistic painterly style blending heroic fantasy with muted color palette and detailed rendering. A middle aged human major in battered and tattered noble clothes with a ruined fox pelt collar. Black hair under a noble berret, black eyes. His left eye covered by a worn leather eyepatch with a noble sigil etched. His walking stick has a large round gem as pommel, gleaning yellow light. Background a wooden town hall two stories with weathered walls, with mud road.",

    "DESCRIPTION": "Garetto Von Garra is the 56 years old Major of the impoverished settlment of Campocestro. His self‑importance far exceeds his actual authority, he calls himself “Governor” and insists that every success in the settlement be credited to him alone. With a scarred left eye hidden beneath an old leather patch, he wear worn and torn noble vestments. He often boast about his strategic victories, brought by the staff he inherited from his ancestors. The sole reminder of the lost glory of his fallen bloodline.",

    "RESOURCES": "Actions: 1\nBonus Actions: 0\nReactions: 0",

    "IMMUNITY": "IMMUNITY:",
    "RESISTENCE": "RESISTENCE:",
    "WEAKNESS": "WEAKNESS: Blunt, Fire",

    "SPELLCASTING": "Spell ability:",

    "PROFICIENCY": 3,

    "INITIATIVE": -1,

    "STRENGTH": -1,
    "STR SAVE": -1,
    "ATHLETICS": -2,

    "DEXTERITY": -1,
    "DEX SAVE": -1,
    "ACROBATICS": -1,
    "SLEIGHT OF HAND": 0,
    "STEALTH": -1,

    "CONSTITUTION": -1,
    "CON SAVE": -1,

    "INTELLIGENCE": 2,
    "INT SAVE": 2,
    "ARCANA": 5,
    "INVESTIGATION": 2,
    "HISTORY": 5,
    "NATURE": 2,
    "RELIGION": 2,

    "WISDOM": 1,
    "WIS SAVE": 2,
    "ANIMAL HANDLING": 4,
    "INSIGHT": 1,
    "PERCEPTION": -1,
    "MEDICINE": 0,
    "SURVIVAL": 1,

    "CHARISMA": 2,
    "CHA SAVE": 5,
    "DECEPTION": 5,
    "INTIMIDATION": 5,
    "PERFORMANCE": 2,
    "PERSUASION": 2,

    "ACTIONS": [
        {
            "s_name": "Boast Fool",
            "s_text": "(1 action) Target in sight with INT>-1. Target must make a CHA SAVE DC15, on fail they take 1d8 psychic damage.",
            "s_flavor": "The Governor boast and threaten to use his connection against the target, listing his achivements."
        },
        {
            "s_name": "Von Garra Heirloom",
            "s_text": "(1 action) Once a day, the Governor can use his staff to make every enemy or neutral creature within 12sq frightened. Those creatures attempt a WIS SAVE DC15 at the end of their turn to recover",
            "s_flavor": "The Von Garra staff is the last possession inherited from his ancestors that hasn't been pawned for money. A walking stick with a large gem, that once a day can make everyone around the caster frightened. This staff, more than once, saved Campocestro from wild beasts."
        }
    ]
}
```


# json node broken

```json
{
    "system": "DnD5E",
    "actor": "NPC",
    "NAME": "Garetto Von Garra",
    "RACE": "Human Fallen Noble (Major)",

    "CR": "1/2",
    "HP": "20",
    "AC": "12",
    "SPEED": "SPEED: Walk: 6sq",

    "IMAGE PROMPT": "",

    "DESCRIPTION": "",

    "RESOURCES": "Actions: 1\nBonus Actions: 1\nReactions: 1",
    "IMMUNITY": "IMMUNITY: ",
    "RESISTENCE": "RESISTENCE: ",
    "WEAKNESS": "WEAKNESS: Blunt, Fire",

    "PROFICIENCY": 3,
    "INITIATIVE": -1,
    "STRENGTH": -1,
    "STR SAVE": -1,
    "DEXTERITY": -1,
    "DEX SAVE": -1,
    "CONSTITUTION": -1,
    "CON SAVE": -1,
    "INTELLIGENCE": 2,
    "INT SAVE": 2,
    "WISDOM": 1,
    "WIS SAVE": 2,
    "CHARISMA": 2,
    "CHA SAVE": 5,
    "ACTIONS": [
        {
            "s_name": "Boast Fool",
            "s_text": "",
            "s_flavor": ""
        },
        {
            "s_name": "Von Garra Heirloom",
            "s_text": "",
            "s_flavor": ""
        }
    ]
}
```
