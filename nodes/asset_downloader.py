import os
import requests
import re
import shutil
import hashlib
from tqdm import tqdm
from server import PromptServer
from folder_paths import models_dir

def model_folders():
    return immediate_folders(models_dir)

def immediate_folders(directory_path):
    """
    Returns a list of folders up to 2 levels deep in the specified directory.
    """        
    folders = []
    for d in os.listdir(directory_path):
        if os.path.isdir(os.path.join(directory_path, d)):
            name = os.path.basename(d)
            if name.startswith('.'):
                continue
            folders.append(d)
            for sd in os.listdir(os.path.join(directory_path, d)):
                if os.path.isdir(os.path.join(directory_path, d, sd)):
                    name = os.path.basename(sd)
                    if name.startswith('.'):
                        continue
                    folders.append(os.path.join(d, sd))
    return folders

class AssetDownloader:
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    CATEGORY = "loaders"
    FUNCTION = "download"

    def __init__(self):
        self.status = "Idle"
        self.progress = 0.0
        self.node_id = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url": ("STRING", {"multiline": False, "default": "https://huggingface.co/ByteDance/SDXL-Lightning/resolve/main/sdxl_lightning_4step.safetensors"}),
                "save_to": (model_folders(), { "default": "checkpoints" }),
                "filename": ("STRING", {"multiline": False, "default": "sdxl_lightning_4step.safetensors"}),
            },
            "optional": {
                "token": ("STRING", { "default": "", "multiline": False, "password": True }),
            },
            "hidden": {
                "node_id": "UNIQUE_ID"
            }
        }

    def download(self, url, save_to, filename, node_id, token=""):
        if not url or not save_to or not filename:
            print(f"AssetDownloader: Missing required values: url='{url}', save_to='{save_to}', filename='{filename}'")
            return ()
            
        # Sanitize save_to to ensure it's within models_dir
        safe_save_to = os.path.normpath(os.path.join(models_dir, save_to))
        if not safe_save_to.startswith(models_dir):
            print(f"AssetDownloader: Invalid save_to path. Must be within {models_dir}")
            return ()
        save_to = os.path.relpath(safe_save_to, models_dir)

        print(f"AssetDownloader: Downloading {url} to {save_to}/{filename} {'with token' if token else ''}")

        relative_path = os.path.join(save_to, filename)
        save_path = os.path.join(models_dir, relative_path)
        if os.path.exists(save_path):
            print(f"AssetDownloader: File already exists: {relative_path}")
            return ()

        print(f'AssetDownloader: Downloading {url} to {relative_path} {" with token" if token else ""}')
        self.node_id = node_id

        # if token starts with `$` replace with environment variable if exists
        if token.startswith("$"):
            env_value = os.getenv(token[1:])
            token = env_value if env_value is not None else token

        headers={"Authorization": f"Bearer {token}"} if token else None

        print(f"Downloading {url} to {relative_path} {'with Authorization header' if headers else ''}")
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        temp_path = save_path + '.tmp'

        downloaded = 0
        last_progress_update = 0
        try:
            with open(temp_path, 'wb') as file:
                with tqdm(total=total_size, unit='iB', unit_scale=True, desc=filename) as pbar:
                    for data in response.iter_content(chunk_size=4*1024*1024):
                        size = file.write(data)
                        downloaded += size
                        pbar.update(size)

                        if total_size > 0:
                            progress = (downloaded / total_size) * 100.0
                            if (progress - last_progress_update) > 0.2:
                                print(f"Downloading {filename}... {progress:.1f}%")
                                last_progress_update = progress
                            if progress is not None and hasattr(self, 'node_id'):
                                PromptServer.instance.send_sync("progress", {
                                    "node": self.node_id,
                                    "value": progress,
                                    "max": 100
                                })

            shutil.move(temp_path, save_path)
            print(f"Complete! {filename} saved to {save_path}")
            return save_path

        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

        return ()
