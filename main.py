from src.enum_model_type import ModelType
import os
import time
import typer
import json
from clip_interrogator import Interrogator, Config
from src.interrogation import create_session_dirs, interrogate_image
from src.logging import LOGGER, register_file_logger


APP = typer.Typer()


def filter_files(raw_filenames: list[str]):
    valid_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
    return list(filter(lambda file: any([extension in file.lower() for extension in valid_extensions]), raw_filenames))


# TODO: Write Unit Tests
@APP.command()
def interrogate(files: list[str], model_type: ModelType = ModelType.fast, output_files: bool = typer.Option(False), log_file: bool = typer.Option(False)):
    if log_file:
        register_file_logger(LOGGER)
    LOGGER.info("Warming up stable-cheese")
    if files and len(files) > 0:
        index: int = 0

        output_path = None
        session_path = None

        if output_files == True:
            LOGGER.info("New session")
            output_path = os.path.join(".", "outputs")
            session_path = os.path.join(
                output_path, time.strftime("%Y%m%d-%H%M%S"))
            create_session_dirs(output_path, session_path)

        LOGGER.info(
            "On first run this step it can take a while because the models have to process the tokens for interrogation")

        CI = Interrogator(Config(
            clip_model_name="ViT-H-14/laion2b_s32b_b79k", blip_max_length=15, device="cuda"))
        json_data = []
        LOGGER.info("Processing started")
        for filepath in files:
            index += 1
            image_data = interrogate_image(
                index, filepath, CI, model_type, session_path)
            if output_files == False and image_data:
                json_data.append(image_data)
        LOGGER.info("Processing finshed")
        if output_files == False:
            LOGGER.info(json.dumps(json_data))
        LOGGER.info("")


# TODO: Write Unit Tests
@APP.command()
def interrogate_folder(folder_path: str, model_type: ModelType = ModelType.fast, output_files: bool = typer.Option(False), log_file: bool = typer.Option(False)):
    if log_file:
        register_file_logger(LOGGER)
    if folder_path and len(folder_path) > 0:
        raw_filenames = os.listdir(folder_path)
        image_filenames = filter_files(raw_filenames)
        image_paths = [os.path.join(folder_path, image_filename)
                       for image_filename in image_filenames]
        LOGGER.info("Interrogating {} image files".format(len(image_paths)))
        interrogate(image_paths, model_type, output_files, log_file=False)


if __name__ == '__main__':
    APP()
