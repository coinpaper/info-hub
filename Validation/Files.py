import os

import yaml


VALIDATION_YML_PATH = './template/validation.yml'


def resolve_file(filepath):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), "./../", filepath))


def open_yml(filepath):
    with open(resolve_file(filepath)) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def validation_yml():
    with open(resolve_file(VALIDATION_YML_PATH)) as file:
        return yaml.load(file, Loader=yaml.FullLoader)

