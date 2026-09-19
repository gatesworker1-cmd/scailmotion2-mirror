#!/usr/bin/env bash
# scailmotion2-slim: the site's template on-start script (gatesgen.com/pod-start.sh) does the whole boot —
# tools, models from R2, SageAttention wheel, Jupyter on 8888, ComfyUI on 8188, the agent. This CMD only keeps
# the container alive when nothing overrides it.
echo "scailmotion2-slim $(date -u) — waiting for the template's on-start script"
exec sleep infinity
