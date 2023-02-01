import re
import subprocess
import tempfile
from tempfile import _TemporaryFileWrapper
from typing import Tuple, Union
from PIL import Image
import json
import gradio as gr
import os
import zipfile


VERSION = "1.1"
REGEXP_BASIC_JSON_PARSER = re.compile(r"\[.*\]", re.MULTILINE)


def get_temporary_filename():
    filename: Union[str, None] = None
    with tempfile.TemporaryFile() as tmp:
        filename = os.path.basename(tmp.name)
    return filename


def parse_images(images: list[_TemporaryFileWrapper]):
    if not images or len(images) == 0: return []
    return [image.name if image else "" for image in images]


# TODO: Make this more secure.
def upload_to_folder(images: list[_TemporaryFileWrapper]):
    input_folder = os.path.join(".", "inputs")

    if not os.path.exists(input_folder):
        os.mkdir(input_folder)

    file_paths = []

    for image in images:
        temp_name = get_temporary_filename()
        image_extension = os.path.basename(image.name).split('.')[1] or "jpg"
        image_path = os.path.join(
            input_folder, "{}.{}".format(temp_name, image_extension))
        file_paths = file_paths + [image_path]
        print(image_path)
        with Image.open(image.file) as image_file:
            image_file.save(image_path)

    return file_paths


# TODO: Write Unit Tests...
def parse_jsons(stdout: str):
    lines = stdout.splitlines()
    json_match = list(filter(lambda line: not line == None, map(lambda line: re.match(REGEXP_BASIC_JSON_PARSER,line), lines)))[0]
    json_str = json_match.group(0) if json_match else "[]"
    return json.loads(json_str)


def download_zip(image_tuples: list[Tuple[_TemporaryFileWrapper, str, int, str]]):
    downloads_path = os.path.join(".", "downloads")
    if not os.path.exists(downloads_path):
        os.mkdir(downloads_path)

    # TODO: Write better duplicate handling.
    file_path = os.path.join(downloads_path, "temp.zip")
    with zipfile.ZipFile(file_path, 'w') as zip:
        for image_pair in image_tuples:
            zip.write(image_pair[0].name, os.path.join("images", str(image_pair[2]) + "-" + image_pair[1] + image_pair[3]))

    return {
        zip_file: gr.update(value=file_path, visible=True)
    }


with gr.Blocks() as app:
    files = gr.Files(file_types=["image"])
    gallery = gr.Gallery().style(grid=4)
    files.change(fn=parse_images, inputs=[files], outputs=[gallery])
    button_interrogate = gr.Button("Interrogate")
    button_download_zip = gr.Button("Download .ZIP", visible=False)
    zip_file = gr.File(visible=False)
    captions_json = gr.JSON()
    caption_state = gr.State(value=None)  # type: ignore

    def interrogate_images(images: list[_TemporaryFileWrapper]):
        output_images = []
        output_json = []
        caption_state_value = []

        uploaded_file_paths = upload_to_folder(images)
        parsed_stdout = interrogate_uploaded_images(uploaded_file_paths)
        parsed_jsons = parse_jsons(parsed_stdout) # TODO: Simplify and optimized code

        for json_item in parsed_jsons:
            image = images[int(json_item["index"]) - 1]  # type: ignore
            caption = json_item["caption"]  # type: ignore
            index = json_item["index"]  # type: ignore
            filetype = json_item["filetype"]  # type: ignore

            output_images.append((
                image.name,
                caption
            ))

            caption_state_value.append((
                image,
                caption,
                index,
                filetype
            ))

        output_json = map(lambda output_image: (os.path.basename(
            output_image[0]), output_image[1]), output_images)

        [os.remove(uploaded_file_path) for uploaded_file_path in uploaded_file_paths]

        return {
            gallery: output_images,
            captions_json: output_json,
            button_download_zip: gr.update(visible=True),
            caption_state: caption_state_value
        }

    def interrogate_uploaded_images(file_paths: list[str]):
        command = "python main.py interrogate {}".format(" ".join(file_paths))
        result = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        return result.stdout

    button_interrogate.click(fn=interrogate_images, inputs=[
        files], outputs=[gallery, captions_json, button_download_zip, caption_state])

    button_download_zip.click(fn=download_zip, inputs=[
                              caption_state], outputs=[zip_file])


app.launch()
