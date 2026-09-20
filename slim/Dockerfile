# syntax=docker/dockerfile:1
# scailmotion2-slim — the same ComfyUI, the same nine custom nodes at the same commits, the same 244 pinned Python
# packages (torch 2.11.0+cu128) as aiorbust/vast-ai-scailmotion2, without the 10 GB CUDA *devel* base the original
# never uses (torch's cu128 wheels carry their own CUDA/cuDNN libraries — the original reports cuDNN 9.19 from pip,
# not the apt 9.8). Ships NO models: the template's on-start pulls them from R2. Layers are split so Vast hosts
# download in parallel and keep what they already have.
FROM nvidia/cuda:12.8.1-base-ubuntu24.04
ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1 PYTHONUNBUFFERED=1 SHELL=/bin/bash \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility,video
# layer 1: OS bits the start script and the nodes rely on (python 3.12, ffmpeg 6.1, rclone, unzip, a C++ compiler for torch.compile)
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3.12 python3.12-venv python3.12-dev python3-pip git curl wget unzip ca-certificates openssh-server \
      ffmpeg libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 libgomp1 build-essential \
    && curl -fsSL https://rclone.org/install.sh | bash \
    && rm -rf /var/lib/apt/lists/* \
    && python3.12 -m venv /opt/venv
ENV PATH=/opt/venv/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
# layer 2: the CUDA / cuDNN / NCCL libraries torch's cu128 wheels depend on (+ triton), pinned exactly — ONE
# LAYER PER PACKAGE (2026-09-21): as a single 3.74 GB layer the download kept dropping on a Vast host and restarted
# from zero each time; per package the biggest piece is one wheel, well under 1 GB, and a drop costs one piece
RUN pip install --no-cache-dir "pip==24.0" "setuptools==81.0.0" "wheel==0.48.0" "packaging==26.3"
RUN pip install --no-cache-dir --no-deps "nvidia-cublas-cu12==12.8.4.1" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "nvidia-cuda-cupti-cu12==12.8.90" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "nvidia-cuda-nvrtc-cu12==12.8.93" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "nvidia-cuda-runtime-cu12==12.8.90" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "nvidia-cudnn-cu12==9.19.0.56" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "nvidia-cufft-cu12==11.3.3.83" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "nvidia-cufile-cu12==1.13.1.3" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "nvidia-curand-cu12==10.3.9.90" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "nvidia-cusolver-cu12==11.7.3.90" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "nvidia-cusparse-cu12==12.5.8.93" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "nvidia-cusparselt-cu12==0.7.1" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "nvidia-nccl-cu12==2.28.9" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "nvidia-nvjitlink-cu12==12.8.93" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "nvidia-nvshmem-cu12==3.4.5" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "nvidia-nvtx-cu12==12.8.90" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "nvidia-vfx==0.1.0.1" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
RUN pip install --no-cache-dir --no-deps "triton==3.6.0" --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
# layer 3: torch 2.11.0+cu128 / torchvision / torchaudio and their small pure-python deps, pinned exactly
COPY requirements-torch.txt /tmp/
RUN pip install --no-cache-dir --no-deps -r /tmp/requirements-torch.txt --index-url https://download.pytorch.org/whl/cu128 --extra-index-url https://pypi.org/simple
# layer 4: every other package from the original image, pinned
COPY requirements-frozen.txt /tmp/
# --no-deps: this is a complete freeze of the original environment, replayed as-is (the original carries a declared
# conflict, cupy 12.3 vs numpy 2.5, that pip's resolver refuses to re-create but that runs fine there)
RUN pip install --no-cache-dir --no-deps -r /tmp/requirements-frozen.txt --extra-index-url https://download.pytorch.org/whl/cu128 \
 && pip check || true
# layer 5: ComfyUI v0.25.0 + the custom nodes at the original commits
COPY nodes.txt clone.sh /tmp/
RUN bash /tmp/clone.sh
COPY start.sh /start.sh
RUN chmod +x /start.sh && mkdir -p /var/log && ln -sf /opt/venv/bin/python /usr/local/bin/python
WORKDIR /
EXPOSE 22 8188 8888
CMD ["/start.sh"]
