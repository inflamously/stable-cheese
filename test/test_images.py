import os
from stable_cheese.src.interrogation import save_captioned_image, save_image
from PIL import Image

TEST_TEMP_FOLDER = './test/temp'
ASSETS_FOLDER = "./test/assets"

if not os.path.exists(TEST_TEMP_FOLDER):
    os.mkdir(TEST_TEMP_FOLDER)


def test_verify_test_environment():
    assert os.getcwd() == r'F:\Programming\PythonDev\Python38\stable_cheese\stable_cheese_interrogator'
    assert os.path.exists(ASSETS_FOLDER) == True
    assert os.path.exists(TEST_TEMP_FOLDER) == True


def test_image_saving():
    input_filepath = os.path.join(ASSETS_FOLDER, 'test_image_red.png')
    assert os.path.exists(input_filepath)
    output_path = os.path.join(TEST_TEMP_FOLDER, "test_image_red.png")
    with Image.open(input_filepath) as im:
        save_image(im, 1, output_path)
    assert os.path.exists(output_path) == True


def test_captioned_image_saving():
    input_filepath = os.path.join(ASSETS_FOLDER, 'test_image_red.png')
    with Image.open(input_filepath) as im:
        save_captioned_image(TEST_TEMP_FOLDER, "test caption whatever works", 1, im)
        assert os.path.exists(os.path.join(TEST_TEMP_FOLDER, "test caption whatever works" + ".png")) == True
        save_captioned_image(TEST_TEMP_FOLDER, "test caption whatever works", 1, im)
        assert os.path.exists(os.path.join(TEST_TEMP_FOLDER, "test caption whatever works" + " 1" + ".png")) == True
    