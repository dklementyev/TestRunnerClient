import json
import io
import os
import sys


def load_json(template_file, **data):
    j = json.load(io.open(file=(os.getcwd() + '\\' + template_file), encoding="utf-8"))

    for key, value in data.items():
        j[str(key)] = value
    return dict(j)
