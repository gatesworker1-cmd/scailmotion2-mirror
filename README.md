# scailmotion2 mirror

A copy of the public Docker Hub image `aiorbust/vast-ai-scailmotion2` on GitHub Container Registry, so
Vast.ai hosts renting for gatesgen.com pull it from `ghcr.io/gatesworker1-cmd/scailmotion2` instead of
Docker Hub (which throttles anonymous pulls per address and stalled several pods).

Nothing runs here on a schedule. To refresh the copy after upstream updates: Actions → "mirror scailmotion2"
→ Run workflow.

## scailmotion2-slim

`ghcr.io/gatesworker1-cmd/scailmotion2-slim:<date>` — the same ComfyUI (v0.25.0, commit `135abed8`), the same eight
custom nodes at the same commits and the same 243 pinned Python packages (torch 2.11.0+cu128) as the original image,
inventoried from the original itself (`inventory` workflow), without the 10 GB CUDA *devel* toolkit the original never
uses at run time, without the original's boot script (which re-downloaded every model from HuggingFace, built
SageAttention from source and started a second Jupyter), and without models — the gatesgen template's on-start
(`pod-start.sh`) provides everything at boot from R2. Left out on purpose: `Nvidia_RTX_Nodes_ComfyUI` (unused by the
workflow; its 1.1 GB C++ extension does not load without the devel toolkit).

Build: Actions → "build scailmotion2-slim" → Run workflow (tag = a date). The job builds, starts ComfyUI on CPU inside
the image and checks that every node type the site's workflow uses is registered and no custom node failed to import,
then pushes.
