import os
import yaml
import git
import Coinpaprika
import pydash

from Coinpaprika.Coinpaprika import CoinpaprikaError

REPO = "coinpaper/info-hub"
REPO_URL = f"https://github.com/{REPO}"
REPO_DIR = f".repos/{REPO}"
EMPTY_FILE = ".empty"


class InfoHub:

    @staticmethod
    def notEmpty(d):
        return d != EMPTY_FILE

    @staticmethod
    def clone_or_pull():
        """
        Clones a new repo or pulls existing one using PyGit
        :return:
        """
        if not os.path.isdir(REPO_DIR):
            git.Repo.clone_from(REPO_URL, REPO_DIR, multi_options=["--depth 1"])
        else:
            git.Repo(REPO_DIR).remote().pull()

    @staticmethod
    def commit(coin_id: str, commit_message=None):
        repo = git.Repo(REPO_DIR)
        if repo.is_dirty():
            print("COMMITING")
            repo.git.add(A=True)
            msg = commit_message if commit_message else f"Initialize yml for {coin_id}"
            repo.index.commit(msg)

    @staticmethod
    def push():
        repo = git.Repo(REPO_DIR)
        origin = repo.remote(name='origin')
        origin.push()

    @staticmethod
    def commit_and_push(coin_id: str, commit_message=None):
        """
        Pushes an update to the info hub
        :param coin_id: Coin that was updated
        :return:
        """
        InfoHub.commit(coin_id, commit_message)
        InfoHub.push()

    @staticmethod
    def all_coin_ids():
        coin_ids = os.listdir(f"{REPO_DIR}/coins")
        test_coin_index = coin_ids.index("test-testing-coin")
        del coin_ids[test_coin_index]
        return coin_ids

    @staticmethod
    def readYML(coin_id):
        """
        Reads yml for a specific coin from the info-hub
        :param coin_id: id of coin
        :return:
        """
        main_dir = f"{REPO_DIR}/coins/{coin_id}"
        path = os.path.join(main_dir, "info.yml")
        if not os.path.isfile(path):
            InfoHub.initYML(coin_id)
        with open(path, "r") as file:
            return yaml.load(file)

    @staticmethod
    def saveYML(coin_id, yml):
        """
        Creates or overwrites the yml file for a specific coin
        :param coin_id: id of coin whose yaml shall be overwritten
        :param yml: Yaml that shall be saved
        :return:
        """
        main_dir = f"{REPO_DIR}/coins/{coin_id}"
        with open(os.path.join(main_dir, "info.yml"), "w") as file:
            yaml.dump(yml, file, sort_keys=False)


    @staticmethod
    def initYML(coin_id):
        tempalte_dir = f"{REPO_DIR}/template"
        main_dir = f"{REPO_DIR}/coins/{coin_id}"
        images_dir = f"{REPO_DIR}/coins/{coin_id}/images"
        files_dir = f"{REPO_DIR}/coins/{coin_id}/files"

        os.mkdir(main_dir)
        os.mkdir(images_dir)
        os.mkdir(files_dir)

        for dir in [images_dir, files_dir]:
            with open(os.path.join(dir, EMPTY_FILE), "w") as f:
                f.write("\n")

        with open(os.path.join(tempalte_dir, "info.yml")) as f:
            initial_yml = yaml.load(f)

        initial_yml = InfoHub.updateFromCoinpaprika(initial_yml, coin_id)
        InfoHub.saveYML(coin_id, initial_yml)

        return initial_yml

    @staticmethod
    def updateYML(coin_id):
        coin = InfoHub.readYML(coin_id)
        updated_yml = InfoHub.updateFromCoinpaprika(coin, coin_id)
        InfoHub.saveYML(coin_id, updated_yml)
        InfoHub.commit_and_push(coin_id, f"Updated infos of {coin_id}")

    @staticmethod
    def updateFromCoinpaprika(infohub_info, coin_id):
        client = Coinpaprika.Client()
        coinpaprika_info = client.coins.with_id(coin_id)
        info_mapping = [
            ["id", "id"],
            ["symbol", "symbol"],
            ["name", "name", ""],
            ["started_at[:10]", "founded"],
            ["description", "descriptions.introduction"],
            ["proof_type", "blockchain.consensus"],
            ["hash_algorithm", "blockchain.algorithm"],
            ["type", "blockchain.type"],
            ["org_structure", "blockchain.organization_structure"],
            ["development_status", "blockchain.development_status"],
            ["links.explorer", "explorers", []],
            ["links.website[0]", "website.url"],
            ["links.telegram[0]", "socials.telegram"],
            ["links.reddit[0]", "socials.reddit"],
            ["links.twitter[0]", "socials.twitter"],
            ["links.medium[0]", "socials.medium"],
            ["links.vimeo[0]", "socials.vimeo"],
            ["links.discord[0]", "socials.discord"],
        ]
        transfer_property(coinpaprika_info, infohub_info, info_mapping)

        issue_date = pydash.get(coinpaprika_info, "started_at")
        if issue_date and not pydash.get(infohub_info, "founded"):
            pydash.set_(infohub_info, "founded", issue_date.strftime("%Y-%m-%d"))
        if issue_date and not pydash.get(infohub_info, "blockchain.issue_date"):
            pydash.set_(infohub_info, "blockchain.issue_date", issue_date.strftime("%Y-%m-%d"))

        coinpaprika_github = pydash.get(coinpaprika_info, "links.source_code[0]", "")
        is_github = "github" in coinpaprika_github
        if is_github and not pydash.get(infohub_info, "github.username"):
            github_repo = coinpaprika_github.replace("https://github.com/", "")
            github_username = github_repo.split("/")[0]
            pydash.set_(infohub_info, "github.username", github_username)

        coinpaprika_team = coinpaprika_info["team"]
        infohub_lead_name = infohub_info["team"]["leader"]["name"]
        if not infohub_lead_name and len(coinpaprika_team) > 0:
            infohub_info["team"]["leader"] = create_member_from_coinpaprika(coinpaprika_team[0])

        if len(infohub_info["team"]["members"]) == 0 and len(coinpaprika_team) > 1:
            infohub_info["team"]["members"] = list(map(
                create_member_from_coinpaprika,
                coinpaprika_team[1:]
            ))

        return infohub_info


def create_member_from_coinpaprika(member):
    try:
        coinpaprika_member = Coinpaprika.Client().people.with_id(member["id"])
        coinpaprika_member["position"] = member["position"]
    except CoinpaprikaError as e:
        coinpaprika_member = member
    infohub_member = empty_team_member()
    member_mapping = [
        ["name", "name"],
        ["description", "description"],
        ["position", "position"],
        ["links.github[0].url", "links.github.url"],
        ["links.github[0].followers", "links.github.followers"],
        ["links.linkedin[0].url", "links.linkedin.url"],
        ["links.linkedin[0].followers", "links.linkedin.followers"],
        ["links.medium[0].url", "links.medium.url"],
        ["links.medium[0].followers", "links.medium.followers"],
        ["links.twitter[0].url", "links.twitter.url"],
        ["links.twitter[0].followers", "links.twitter.followers"],
    ]
    return transfer_property(coinpaprika_member, infohub_member, member_mapping)

def transfer_property(from_object, to_object, mappings):
    for mapping in mappings:
        if len(mapping) == 2:
            from_path, to_path = mapping
            default = None
        else:
            from_path, to_path, default = mapping
        from_value = pydash.get(from_object, from_path, default)
        to_value = pydash.get(to_object, to_path)
        if not to_value and from_value:
            pydash.set_(to_object, to_path, from_value)
    return to_object

def empty_team_member():
    return {
        "name": None,
        "imagename": None,
        "position": None,
        "description": None,
        "links": {
            "github": { "url": None, "followers": None },
            "linkedin": { "url": None, "followers": None },
            "medium": { "url": None, "followers": None },
            "twitter": { "url": None, "followers": None },
        }
    }

