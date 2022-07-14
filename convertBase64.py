import models as md
import base64
from methods.genUUID import GenerateUUID

def processImage(image):

    string = image
    encript = GenerateUUID()
    route = f"static/profileImages/{encript}.png"

    with open(route, "wb") as fh:
        fh.write(base64.b64decode(string))

    return f"/{route}"

def processPostImage(image):

    string = image
    encript = GenerateUUID()
    route = f"static/postImages/{encript}.png"

    with open(route, "wb") as fh:
        fh.write(base64.b64decode(string))

    return f"/{route}"
