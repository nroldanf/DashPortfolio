import base64
import numpy as np

def parse_contents(contents):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string).decode('ascii')
    return decoded
