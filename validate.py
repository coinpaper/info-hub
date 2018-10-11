import os

from Validation.YMLValidator import YMLValidator

COINS_DIR = "coins"


def get_coins():
    coins = os.listdir(os.path.normpath(os.path.join(os.path.dirname(__file__), COINS_DIR)))
    coins.remove("test-testing-coin")
    return coins


if __name__ == "__main__":
    coins = get_coins()
    print(coins)
    for coin in coins:
        print(f"***{coin}***")
        validator = YMLValidator(coin)
        validator.validate()

