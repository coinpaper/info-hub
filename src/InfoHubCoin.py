from .InfoHub import InfoHub

from utils import APICoin


class InfoHubCoin(APICoin):
    _info_hub = InfoHub()

    def __init__(self, coin_id, coin_name, coin_symbol):
        super().__init__(coin_id, coin_name, coin_symbol)

        self._info_hub.clone_or_pull()
        self._yml = InfoHub.readYML(self.coin_id)

        self.symbol = self._yml["symbol"]
        self.name = self._yml["name"]
        self.founded = self._yml["founded"]

        self.descriptions = self.get_descriptions()
        self.blockchain = self.get_blockchain()
        self.explorers = self.get_explorers()
        self.whitepaper = self.get_whitepaper()
        self.website = self.get_website()
        self.video = self.get_video()
        self.team = self.get_team()
        self.socials = self.get_socials()
        self.github = self.get_github()
        self.manual_reviews = self.get_manual_reviews()


    def get_descriptions(self):
        return self._yml["descriptions"]

    def get_blockchain(self):
        return self._yml["blockchain"]

    def get_explorers(self):
        return self._yml["explorers"]

    def get_whitepaper(self):
        return self._yml["whitepaper"]

    def get_website(self):
        return self._yml["website"]

    def get_video(self):
        return self._yml["video"]

    def get_team(self):
        return self._yml["team"]

    def get_socials(self):
        return self._yml["socials"]

    def get_github(self):
        return self._yml["github"]

    def get_manual_reviews(self):
        return self._yml["manual_reviews"]

    def save(self):
        InfoHub.commit_and_push(self.coin_id)


if __name__ == "__main__":
    btc = InfoHubCoin("bnb-binance-coin")
    print(btc.json())
