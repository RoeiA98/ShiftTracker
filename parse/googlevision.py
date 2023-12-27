from google.cloud import vision
import os

def detect_text(path):

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vision_key.json'

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations[0]

    with open('result.txt', 'w') as file:
        file.write(str(texts.description))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    