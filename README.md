# Character Sheet Generator Node

This sets of nodes for ComfyUI takes an image and a D&D5E character sheet and generate a character sheet card meant for NPCs



# NODES

## D&D 5E FORMULAE

Receive a character sheet json. applies to formulae to compute the ability modifiers and estimate difficulty and CR.

The RAW json gives full control allowing to do any combination of stats.

Being processed by the formulae node allows to use the JSON as origin for the abilities.

The base of abilities is usually its roll stat, plus proficiency, plus a modifier that can come from class, race, background, items, etc... It uses the input ACROBATICS as other and add DEX MOD and PROF.

E.g. ACROBATICS = DEX MOD + PROF + OTHERS

## D&D 5E CHARACTER SHEET GENERATIVE 

Nodes that start from a brief NPC idea and creates the NPC json. 

Nodes to get the custom prompts to feed the LLM and get the output JSON. It should have a check stage to add possible missing stats as the generation depend on model type and isn't deterministic.

ComfyUI doesn't have much in the way of LLM inference, I should just have tensor LLM nodes for 



# FEATURES

### LLM inference

I need to add an LLM inference node that is able to reliably generate a prompt and a JSON from a description

Done in two stages. One stage generates a NPC. THe second stage make a JSON from it. Selector for desired stat reference.

