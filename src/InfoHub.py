import os
import yaml
import git


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
    def commit_and_push(coin_id: str, commit_message=None):
        """
        Pushes an update to the info hub
        :param coin_id: Coin that was updated
        :return:
        """
        repo = git.Repo(REPO_DIR)
        repo.git.add(update=True)
        msg = commit_message if commit_message else f"Initialize yml for {coin_id}"
        repo.index.commit(msg)
        origin = repo.remote(name='origin')
        origin.push()

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
            empty_yml = yaml.load(f)

        empty_yml["id"] = coin_id
        empty_yml["symbol"] = coin_id
        empty_yml["name"] = coin_id

        InfoHub.saveYML(coin_id, empty_yml)


if __name__ == "__main__":
    InfoHub().clone_or_pull()
    InfoHub.commit_and_push("egld-elrond", commit_message="Minor update for OMG (deprecated)")
