# Starts ComfyUI on CPU inside the built image and confirms every node type the site's workflow uses is registered.
import json, sys, time, urllib.request, subprocess
NEED = ["CLIPLoader","CLIPTextEncode","CLIPVisionEncode","CLIPVisionLoader","CheckpointLoaderSimple","GetImageSize","LoadImage",
        "LoraLoaderModelOnly","ModelPatchTorchSettings","ModelSamplingSD3","PathchSageAttentionKJ","PreviewImage","PrimitiveBoolean",
        "PrimitiveFloat","ResizeImageMaskNode","SAM3_VideoTrack","SCAIL2ColoredMask","TorchCompileModelAdvanced","UNETLoader",
        "VAELoader","VHS_LoadVideo","VHS_VideoCombine","WanSCAILInfinity"]
p = subprocess.Popen(["python", "main.py", "--cpu", "--listen", "127.0.0.1", "--port", "8188"], cwd="/ComfyUI", stdout=open("/tmp/comfy.log", "w"), stderr=subprocess.STDOUT)
for _ in range(120):
    time.sleep(5)
    try:
        info = json.load(urllib.request.urlopen("http://127.0.0.1:8188/object_info", timeout=10)); break
    except Exception:
        if p.poll() is not None: print("ComfyUI exited"); print(open("/tmp/comfy.log").read()[-4000:]); sys.exit(1)
else:
    print("ComfyUI never answered"); print(open("/tmp/comfy.log").read()[-4000:]); sys.exit(1)
missing = [n for n in NEED if n not in info]
print("node types registered:", len(info), "| workflow needs", len(NEED), "| missing:", missing or "none")
log = open("/tmp/comfy.log").read()
for line in log.splitlines():
    if "IMPORT FAILED" in line or "Cannot import" in line or "Traceback" in line: print("!!", line[:200])
failed = [l for l in log.splitlines() if "IMPORT FAILED" in l]
print("custom nodes that failed to import:", len(failed))
p.terminate()
sys.exit(1 if (missing or failed) else 0)
