from .nodes.asset_downloader import AssetDownloader
import os

NODE_CLASS_MAPPINGS = { 
    "AssetDownloader": AssetDownloader,
}

NODE_DISPLAY_NAME_MAPPINGS = { 
    "AssetDownloader": "Requires Asset",
}

WEB_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY"
]