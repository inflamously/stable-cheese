# Stable Cheese Interrogator

A minimal app using [clip-interrogator](https://github.com/pharmapsychotic/clip-interrogator) and [blip](https://github.com/salesforce/BLIP) for captioning lots of images quickly.

The application served to caption custom images which had only basic names like IMAGE_001.png and such.

This program has an optionated way on captioning images. May open it up more by implementing some more parameters for customizing captioning.

#### How to use?

Well you can either use it as a CLI tool using following commands:

##### Installation

```
py -m venv venv
py -m pip install -r requirements.txt
```



##### Output JSON in Terminal for CLI usage

```bash
py main.py C:\Users\<username>\OneDrive\Pictures\test_picture_01.png C:\Users\<username>\OneDrive\Pictures\test_picture_02.png # Caption as many images as you like.
```


##### Output JSON for images in a folder

```bash
py main.py C:\Users\<username>\OneDrive\Pictures\test_picture_01.png C:\Users\<username>\OneDrive\Pictures\test_picture_02.png # Caption as many images as you like.
```


##### Output Files in directory

This creates an "outputs" directory with a new subfolder (current date & time) where images get saved with a new captioned filename and their respective extension.

```
py main.py C:\Users\<username>\OneDrive\Pictures\test_picture_01.png C:\Users\<username>\OneDrive\Pictures\test_picture_02.png --output_files
```

##### Or by directly running the gradio app:

```bash
py app.py # Starts an gradio instance which can be accessed via browser
```



#### App.py



* Image by [Michelle McEwen](https://unsplash.com/@michellem18?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/de/fotos/zZbcIw0LHb4?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)