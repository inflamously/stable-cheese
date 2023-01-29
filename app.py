from re import match
from tempfile import _TemporaryFileWrapper
import tempfile
from typing import Any, Tuple
from PIL import Image
import gradio as gr
import os
from json import loads
import zipfile


interrogating = False


def parse_images(images: list[_TemporaryFileWrapper]):
    return [image.name if image else "" for image in images]


def upload_to_folder(images: list[_TemporaryFileWrapper]):
    input_folder = os.path.join(".", "inputs")

    if not os.path.exists(input_folder):
        os.mkdir(input_folder)

    file_paths = []

    for image in images:
        image_path = os.path.join(input_folder, os.path.basename(image.name))
        file_paths = file_paths + [image_path]
        with Image.open(image.file) as image_file:
            image_file.save(image_path)

    return file_paths


def parse_jsons(stdout: str):
    lines = stdout.splitlines()
    return list(filter(lambda line: match(r"\[\".*\"\]", line), lines))


def download_zip(image_tuples: list[Tuple[_TemporaryFileWrapper, str, int, str]]):
    temp = tempfile.TemporaryFile()
    with zipfile.ZipFile(temp.file, 'w') as zip:
        for image_pair in image_tuples:
            zip.write(image_pair[0].name, os.path.join(str(image_pair[2]) + "-" + image_pair[1], image_pair[3]))
    return {
        zip_file: gr.update(value=temp.name, visible=True)
    }


with gr.Blocks() as app:
    files = gr.Files(file_types=["image"])
    gallery = gr.Gallery().style(grid=4)

    files.change(fn=parse_images, inputs=[files], outputs=[gallery])
    button_interrogate = gr.Button("Interrogate")
    button_download_zip = gr.Button("Download .ZIP", visible=False)
    captions = gr.JSON()
    caption_state = gr.State(value=None)
    zip_file = gr.File(visible=False)

    def interrogate_images(images: list[_TemporaryFileWrapper]):
        # file_paths = upload_to_folder(images)
        # command = "python main.py {}".format(" ".join(file_paths))
        # result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        # out = result.stdout
        # jsons = parse_jsons(out)
        jsons = ['{"index": 1, "caption": "a statue of bull sitting on top wooden portrait minotaur", "filetype": ".png"}',
                 '{"index": 2, "caption": "a statue of bull sitting on top wooden portrait minotaur", "filetype": ".png"}', '{"index": 3, "caption": "a statue of bull sitting on top wooden portrait minotaur", "filetype": ".png"}']
        parsed_json_array: list[list[dict[str, Any]]] = [
            loads(json) for json in jsons]
        output_images = []
        caption_state_value = []
        for json in parsed_json_array:
            image = images[int(json["index"]) - 1]  # type: ignore
            caption = json["caption"]  # type: ignore
            index = json["index"] # type: ignore
            filetype = json["filetype"] # type: ignore

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

        return {
            gallery: output_images,
            captions: output_images,
            button_download_zip: gr.update(visible=True),
            caption_state: caption_state_value
        }

    button_interrogate.click(fn=interrogate_images, inputs=[
        files], outputs=[gallery, captions, button_download_zip, caption_state])

    button_download_zip.click(fn=download_zip, inputs=[caption_state], outputs=[zip_file])


app.launch()
