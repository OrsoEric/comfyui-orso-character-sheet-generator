set UV_CACHE_DIR=D:\UV_CACHE
set UV_CACHE_DIR=F:\UV_CACHE

uv venv .venv --python 3.13

.venv\Scripts\activate

uv pip install comfy-cli

comfy node init


https://registry.comfy.org/publishers/mendicant-bias-05032/nodes/orso-character-sheet-generator