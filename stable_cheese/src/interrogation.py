import os
from typing import Any, Union
from .caption_tools import optimize_caption
from .logging import LOGGER
from clip_interrogator import Interrogator
from PIL import Image


def save_captioned_image(session_path: str, caption: str, file_index: int, image: Any, extension=".png"):
    captioned_filepath = os.path.join(session_path, caption + extension)
    if os.path.exists(captioned_filepath):
        LOGGER.warning('Captioned image file already exists: "{}", suffixing file index'.format(os.path.basename(captioned_filepath)))
        captioned_filepath = captioned_filepath.replace(
            ".png", " {}{}".format(file_index, extension))
    save_image(image, file_index, captioned_filepath)


def save_image(image: Any, file_index: int, output_path: str):
    LOGGER.info("Image {} Output {}".format(file_index, output_path))
    image.save(output_path, quality=100, subsampling=0)


def interrogate_image(file_index: int, filepath: str, CI: Interrogator, model_type: str, session_path: Union[str, None]):
    original_caption = None

    with Image.open(filepath) as image:
        if model_type == 'fast':
            original_caption = CI.interrogate_fast(
                image, max_flavors=1)  # type: ignore
        elif model_type == 'best':
            original_caption = CI.interrogate(
                image, max_flavors=1)  # type: ignore

    new_caption = optimize_caption(original_caption)

    if session_path and len(session_path) > 0:
        save_captioned_image(session_path, new_caption, file_index, image)
        return None
    else:
        return {"index": file_index, "caption": new_caption, "filetype": ".png"}


def create_session_dirs(output_path, session_path):
    if not os.path.exists(output_path):
        LOGGER.info("Creating session output folder")
        os.mkdir(output_path)

    if not os.path.exists(session_path):
        LOGGER.info("Creating session folder")
        os.mkdir(session_path)
