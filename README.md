# Comfy Asset Downloader

A ComfyUI custom node that allows you to download models and other assets used in ComfyUI workflows from external sources like Hugging Face and CivitAI directly within your workflows to make it easier to share workflows and save time finding and downloading all the assets needed.

## Features

- Download models, checkpoints, VAEs, and other assets from external URLs
- Specify custom save locations within your ComfyUI models directory
- Support for authenticated downloads using API tokens
- Visual progress indicator during downloads
- Embed download nodes directly in your workflows to ensure dependencies are available

[![](./examples/workflow.webp)](https://raw.githubusercontent.com/ServiceStack/comfy-asset-downloader/refs/heads/main/examples/workflow.webp)

## Installation

### Using ComfyUI Manager

Search and install **Comfy Asset Downloader** from [ComfyUI's Manager](https://github.com/Comfy-Org/ComfyUI-Manager) **Custom Nodes Manager**.

### Using Git

```bash
git clone https://github.com/ServiceStack/comfy-asset-downloader \
    ComfyUI/custom_nodes/comfy-asset-downloader
```

### Configure Environment Variables (Optional)

To download models and resources from CivitAI or protected Hugging Face repositories we recommend your ComfyUI
instance has these environment variables (e.g. by adding to `~/.profile`):

```
export HF_TOKEN=hf_xxx
export CIVITAI_TOKEN=civitai_token
```

Restart ComfyUI after installation.

## Description

The Asset Downloader node provides a simple interface:

- **url**: The direct URL to the file you want to download
- **save_to**: The subfolder within your ComfyUI models directory to save the file
- **filename**: The name to save the file as
- **token** (optional): API token for authenticated downloads (e.g. for CivitAI or private Hugging Face repositories)

For ease of use and security the **token** can be prefixed with `$` to use an environment variable (e.g. `$HF_TOKEN` or `$CIVITAI_TOKEN`) for the token available to the ComfyUI instance.

This will use the value of the `HF_TOKEN` environment variable if it exists.

### Usage

1. Add an `AssetDownloader` node to your workflow
2. Set the URL to a model file (e.g., `https://huggingface.co/model-repo/resolve/main/the_model.safetensors`)
3. Choose the appropriate save location (e.g. `checkpoints`)
4. Set the filename (e.g., `the_model.safetensors`)
5. Run the workflow - the file will be downloaded if it doesn't already exist

## Example ComfyUI Workflows

Check out the example workflows containing asset dependencies in the `examples` folder:

![](./examples/hidream-dev-face.png)

__(Drag image to ComfyUI)__

### HiDream

- [hidream-dev-face.json](./examples/hidream-dev-face.json): ComfyUI workflow that downloads and uses the leading OSS **HiDream-I1 Dev** model for high quality image generation
- [hidream-fast-crystalball.json](./examples/hidream-fast-crystalball.json): A workflow that downloads and uses the fast version of **HiDream-I1 Fast** model

### Flux

- [flux1-schnell-cyborg.json](./examples/flux1-schnell-cyborg.json): A workflow using the **FLUX.1-schnell** model from Hugging Face (requires HF_TOKEN)

### Stable Diffusion

- [sdxl_lightning-enchantress.json](./examples/sdxl_lightning-enchantress.json): A workflow that downloads **SDXL-Lightning** from Hugging Face for fast image generation using SDXL
- [sdxl_base_refiner-bottle.json](./examples/sdxl_base_refiner-bottle.json): A workflow that downloads **SDXL Base** and **SD XL Refiner** from Hugging Face for an image generation example using a base model with a refiner
- [sdxl-base_refiner_sytan-tiger.json](./examples/sdxl-base_refiner_sytan-tiger.json): A more complex **SDXL Base** and **SD XL Refiner** workflow from [@SytanSD](https://github.com/SytanSD/Sytan-SDXL-ComfyUI)
- [sdxl_turbo1-fox.json](./examples/sdxl_turbo1-fox.json): A workflow that downloads **SDXL Turbo v1.0** from Hugging Face for basic image 512x512 generation
- [sd3.5_large_fp8-spider.json](./examples/sd3.5_large_fp8-spider.json): A workflow that downloads **Stable Diffusion 3.5 Large FP8** model from Hugging Face for a more resource efficient high quality SD 3.5 Large image generation

### CivitAI (requires CIVITAI_TOKEN)

- [epiCRealismXL-sparrow.json](./examples/epiCRealismXL-sparrow.json): A workflow that downloads the [epiCRealism XL](https://civitai.com/models/277058?modelVersionId=1522905) model from CivitAI
- [dreamshaperXL-forest-woman.json](./examples/dreamshaperXL-forest-woman.json): A workflow using [DreamShaper XL](https://civitai.com/models/112902/dreamshaper-xl) from CivitAI
- [jibMixRealisticXL-hamster.json](./examples/jibMixRealisticXL-hamster.json): A workflow that uses [Jib Mix Realistic XL](https://civitai.com/models/194768/jib-mix-realistic-xl) from CivitAI
- [CheyenneXL-samurai.json](./examples/CheyenneXL-samurai.json): A workflow that uses [CHEYENNE v2.2 (VAE Baked)](https://civitai.com/models/198051/cheyenne) from CivitAI

### Wan

- [wan-image-to-video.json](./examples/wan-image-to-video.json.json): A workflow that downloads **Wan2.1** text-to-video model from Hugging Face for generating videos from an initial image and text prompt


## Credits

 - [comfyui-model-downloader](https://github.com/ciri/comfyui-model-downloader)