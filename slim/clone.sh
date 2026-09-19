#!/usr/bin/env bash
# ComfyUI + custom nodes at the EXACT commits found in the original image (inventory 2026-09-20). Shallow fetch by
# commit keeps .git tiny; node requirements are installed after, and are already satisfied by the frozen pins.
set -euo pipefail
clone() { mkdir -p "$1"; git -C "$1" init -q; git -C "$1" remote add origin "$2"; git -C "$1" fetch -q --depth 1 origin "$3"; git -C "$1" checkout -q FETCH_HEAD; echo "$1 @ $(git -C "$1" rev-parse HEAD)"; }
clone /ComfyUI https://github.com/comfyanonymous/ComfyUI 135abed8da169e33ab0b86550e05e3ae55d6df8c
pip install --no-cache-dir -r /ComfyUI/requirements.txt
while read -r name url sha; do
  clone "/ComfyUI/custom_nodes/$name" "$url" "$sha"
  [ -f "/ComfyUI/custom_nodes/$name/requirements.txt" ] && pip install --no-cache-dir -r "/ComfyUI/custom_nodes/$name/requirements.txt"
done < /tmp/nodes.txt
# model folders exist (empty) exactly as ComfyUI ships them; the template's on-start fills them from R2
find /ComfyUI/models -type f -name 'put_*' | wc -l
rm -rf /root/.cache/pip
