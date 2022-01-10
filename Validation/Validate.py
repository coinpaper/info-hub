import os
import re
import datetime

import requests
from PIL import Image
import validators

from Validation.Files import resolve_file

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-langauge": "de-CH,de-DE;q=0.9,de;q=0.8,en-US;q=0.7,en;q=0.6",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
}

github_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}

if 'GITHUBAPI' in os.environ:
    github_headers['Authorization'] = f"token {os.environ['GITHUBAPI']}"


def optional(value, argument=None, arguments=None, context=None):
    return True


def text(value, argument=None, arguments=None, context=None):
    if type(value) != str:
        raise ValueError(f"Type text must be a string, got value '{value}' of type '{type(value)}'")
    html_remover = re.compile("(<.*?>)")
    html_br_remover = re.compile("<br[^\S\n\t]?/?>")
    cleaned_input = re.sub(html_remover, '', value)
    removed_brs = re.sub(html_br_remover, '', value)
    if removed_brs != cleaned_input:
        raise ValueError(f"Text can not contain any HTML, found html in '{value}'")
    return True


def number(value, argument=None, arguments=None, context=None):
    if type(value) not in [int, float]:
        raise ValueError(f"Number must be int or float, got '{value}' of type '{type(value)}'")
    return True


def boolean(value, argument=None, arguments=None, context=None):
    if type(value) != bool:
        raise ValueError(f"Boolean must be true or false, got '{value}' of type '{type(value)}'")
    return True


def lowercase(value, argument=None, arguments=None, context=None):
    if value != value.lower():
        raise ValueError(f"Value must be all lowercase, got '{value}'")
    return True


def uppercase(value, argument=None, arguments=None, context=None):
    if value != value.upper():
        raise ValueError(f"Value must be all uppercase, got '{value}'")
    return True


def max(value, argument=None, arguments=None, context=None):
    max_value = float(argument)
    if type(value) == str:
        if len(value) > max_value:
            raise ValueError(f"Maximum length of string is '{max_value}', but got '{len(value)}'")
        return True
    if value > max_value:
        raise ValueError(f"Maximum value of number is '{max_value}', but got '{value}'")
    return True


def min(value, argument=None, arguments=None, context=None):
    min_value = float(argument)
    if type(value) == str:
        if len(value) < min_value:
            raise ValueError(f"Minimal length of string is '{min_value}', but got '{len(value)}'")
        return True
    if value < min_value:
        raise ValueError(f"Minimum value of number is '{min_value}', but got '{value}'")
    return True


def date(value, argument=None, arguments=None, context=None):
    if isinstance(value, datetime.date):
        return True
    try:
        datetime.datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        raise ValueError(f"Date '{value}' is not in format '%Y-%m-%d'")


def oneof(value, argument=None, arguments=None, context=None):
    choices = arguments
    if value not in choices:
        raise ValueError(f"Value '{value}' does not appear in choices: {','.join(choices)}")
    return True


def url(value, argument=None, arguments=None, context=None):
    if not validators.url(value):
        raise ValueError(f"URL has an invalid format: '{value}'")
    return True


def foreach(value, argument=None, arguments=None, context=None):
    fun_args = [resolve_validation_function(arg) for arg in arguments]
    for fun, args in fun_args:
        if not all([fun(v, argument=args[0], arguments=args, context=context) for v in value]):
            raise ValueError(f"In the for-each check, one value could not be verified")
    return True


def startswith(value, argument=None, arguments=None, context=None):
    prefix = argument
    if not value.startswith(prefix):
        raise ValueError(f"Value '{value}' does not start with prefix '{prefix}'")
    return True


def endswith(value, argument=None, arguments=None, context=None):
    postfix = argument
    if not value.endswith(postfix):
        raise ValueError(f"Value '{value}' does not end with postfix '{postfix}'")
    return True


def file(value, argument=None, arguments=None, context=None):
    coin_id = context["coin_id"]
    filepath = resolve_file(f"coins/{coin_id}/files/{value}")
    if not os.path.isfile(filepath):
        raise ValueError(f"File path could not be resolved: '{filepath}'")
    return True


def pdf(value, argument=None, arguments=None, context=None):
    if not value.endswith(".pdf"):
        raise ValueError(f"Value '{value}' does not end with '.pdf'")
    return True


def image(value, argument=None, arguments=None, context=None):
    coin_id = context["coin_id"]
    filepath = resolve_file(f"coins/{coin_id}/images/{value}")
    is_file = os.path.isfile(filepath)
    if not is_file:
        raise ValueError(f"Image path could not be resolved: '{filepath}'")
    image = Image.open(filepath)
    width, height = image.size
    if not (width == 512 and height == 512):
        raise ValueError(
            f"Image has not correct dimensions. Expected width=512 and height=512, but got: width={width} and height={height}")
    return True


def png(value, argument=None, arguments=None, context=None):
    if not value.endswith(".png"):
        raise ValueError(f"Value '{value}' does not end with '.png'")
    return True


def opposite(value, argument=None, arguments=None, context=None):
    opposite_val = context["opposite"]
    if not (type(value) == bool and type(opposite_val) == bool):
        raise ValueError(
            f"The input or opposite values are not of type boolean. Value is type '{type(value)}', opposite is type '{type(opposite_val)}'")
    opposite_val_neg = not opposite_val
    if value != opposite_val_neg:
        raise ValueError(
            f"Input and opposite values are not opposites of each other. Value is '{value}', but opposite is '{opposite_val}'")
    return True


def youtube(value, argument=None, arguments=None, context=None):
    regex = re.compile("^https:\/\/www\.youtube\.com\/watch\?v=[a-zA-Z0-9_-]{11}$")
    if not re.match(regex, value):
        raise ValueError(
            f"YouTube URL is malformatted: {value}. Make sure it is not a short-url and does not include a time specifier.")
    return True


def githubuser(value, argument=None, arguments=None, context=None):
    if "/" in value:
        raise ValueError(f"Github username can NOT contain a slash: {value}")
    github_request = requests.get(f"https://api.github.com/users/{value}", headers=github_headers).json()
    if github_request.get("message", "") == "Not Found":
        raise ValueError(f"Github user {value} does not exist")
    if github_request.get("message", "").startswith("API rate limit exceeded"):
        raise RuntimeError("Github API rate limit exceeded!")
    return True


def githubrepo(value, argument=None, arguments=None, context=None):
    if value.count("/") != 1:
        raise ValueError(f"Github repos contain exactly one slash: {value}")
    github_request = requests.get(f"https://api.github.com/repos/{value}", headers=github_headers).json()
    if github_request.get("message", "") == "Not Found":
        raise ValueError(f"Github user {value} does not exist")
    if github_request.get("message", "").startswith("API rate limit exceeded"):
        raise RuntimeError("Github API rate limit exceeded!")
    return True


validation_map = {
    "optional": optional,
    "text": text,
    "number": number,
    "boolean": boolean,
    "lowercase": lowercase,
    "uppercase": uppercase,
    "max": max,
    "min": min,
    "date": date,
    "oneof": oneof,
    "url": url,
    "foreach": foreach,
    "startswith": startswith,
    "endswith": endswith,
    "file": file,
    "pdf": pdf,
    "image": image,
    "png": png,
    "opposite": opposite,
    "youtube": youtube,
    "githubuser": githubuser,
    "githubrepo": githubrepo,
}


def resolve_validation_function(validation):
    if "(" in validation:
        function_name = validation[:validation.index("(")]
        function_args = validation[validation.index("(") + 1:-1].split(",")
    else:
        function_name = validation
        function_args = (None,)
    return validation_map[function_name], tuple(function_args)


if __name__ == "__main__":
    print(requests.head("https://www.facebook.com/iotatoken", headers=headers).status_code)
