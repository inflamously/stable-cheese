from enum import Enum
from re import findall
from typing import List, Union
from PIL import Image
from clip_interrogator import Interrogator, Config
import os
import time
import typer
from json import dumps


APP = typer.Typer()


# Classes
class ModelType(str, Enum):
    fast = "fast",
    best = "best"


# Functions
def unique_words(words_as_list):
    result = []
    for word in words_as_list:
        if not word in result:
            result.append(word)
    return result


def caption_stripper(caption):
    words_as_list = findall(r"[A-Za-z0-9]+", caption)
    resulting_words = unique_words(words_as_list)
    return " ".join(resulting_words)


def interrogate_image(file_index: int, filepath: str, CI: Interrogator, model_type: str, session_path: Union[str, None]):
    with Image.open(filepath) as image:
        original_caption = None
        if model_type == 'fast':
            original_caption = CI.interrogate_fast(
                image, max_flavors=1)  # type: ignore
        elif model_type == 'best':
            original_caption = CI.interrogate(
                image, max_flavors=1)  # type: ignore
        stripped_caption = caption_stripper(original_caption)

        if session_path and len(session_path) > 0:
            output_path = os.path.join(
                session_path, stripped_caption + "." + "png")
            print("Image", file_index, "Output", output_path)
            image.save(output_path, quality=100, subsampling=0)
        else:
            print("{}".format(
                dumps({"index": file_index, "caption": stripped_caption, "filetype": ".png"})))


def create_session_dirs(output_path, session_path):
    if not os.path.exists(output_path):
        print("Creating session output folder")
        os.mkdir(output_path)

    if not os.path.exists(session_path):
        print("Creating session folder")
        os.mkdir(session_path)


def test_callback(input):
    return input if input in ["fast", "best"] else "fast"


@APP.command()
def interrogate(files: List[str], model_type: ModelType = ModelType.fast, output_files: bool = typer.Option(False)):
    if files and len(files) > 0:
        index: int = 0

        output_path = None
        session_path = None

        if output_files == True:
            print("New session")
            output_path = os.path.join(".", "outputs")
            session_path = os.path.join(
                output_path, time.strftime("%Y%m%d-%H%M%S"))
            create_session_dirs(output_path, session_path)

        print("Warming up stable-cheese")
        print("On first run this step it can take a while because the models have to process the tokens for the interrogating once")
        CI = Interrogator(Config(
            clip_model_name="ViT-H-14/laion2b_s32b_b79k", blip_max_length=15, device="cuda"))
        for filepath in files:
            index += 1
            interrogate_image(index, filepath, CI, model_type, session_path)


if __name__ == '__main__':
    APP()
