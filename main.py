from re import findall
from PIL import Image
from clip_interrogator import Interrogator, Config
from easygui import fileopenbox, choicebox
import os
import time

OUTPUT_PATH = './outputs/'
SESSION_PATH = os.path.join(OUTPUT_PATH, time.strftime("%Y%m%d-%H%M%S")) + "/"

if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)
    
if not os.path.exists(SESSION_PATH):
    os.mkdir(SESSION_PATH)
    

def unique_words(words_as_list):
    result = []
    for word in words_as_list:
        if not word in result:
            result.append(word)
    return result;


def caption_stripper(caption):
    words_as_list = findall(r"[A-Za-z0-9]+", caption)
    resulting_words = unique_words(words_as_list)
    return " ".join(resulting_words)


def interrogate_image(filepath):
    with Image.open(filepath) as image:
        original_caption = None
        if model == 'fast':
            original_caption = CI.interrogate_fast(image, max_flavors=1)
        elif model == 'best':
            original_caption = CI.interrogate(image, max_flavors=1)
        stripped_caption = caption_stripper(original_caption)
        output_path = os.path.join(SESSION_PATH, stripped_caption + "." + "png")
        print("Image", index, "Output", output_path)
        image.save(output_path, quality=100, subsampling=0)
    

print("Loading Model")
print("WARN: On first run this step it can take a while because the models have to process the tokens for the interrogating once.")
CI = Interrogator(Config(clip_model_name="ViT-H-14/laion2b_s32b_b79k", blip_max_length=15, device="cuda"))


print("Awaiting Files")
model = choicebox('Select model', choices=['fast', 'best'])
files = fileopenbox('Select images to interrogate: ', 'Stable-Cheese', multiple=True)
if files and len(files) > 0:
    index = 0
    for filepath in files:
        index += 1
        interrogate_image(filepath)