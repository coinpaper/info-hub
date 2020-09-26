import os

from Validation.YMLValidator import YMLValidator

COINS_DIR = "coins"


def get_coins():
    return os.listdir(os.path.normpath(os.path.join(os.path.dirname(__file__), COINS_DIR)))


if __name__ == "__main__":
    coins = get_coins()
    for coin in coins:
        validator = YMLValidator(coin)
        validator.validate()

