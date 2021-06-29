import requests
from os import path
import sys
import subprocess


def download():
    print("[INFO]: Downloading requirements")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("[INFO]: Downloading missing config file.")

    url = "https://cdn.edb.tools/Mobius/default_config.ini"
    r = requests.get(url)

    if str(r.status_code) == "200":
        with open('./config.ini', 'wb') as f:
            f.write(r.content)
        print("[INFO]: Please configure config.ini then boot the bot again")
        print("[INFO]: Shutting down program...")
        sys.exit()
    else:
        print("[ERROR]: There was an issue retrieving the config file.\n"
              "Please try downloading the file manually here:\n"
              "https://cdn.edb.tools/Mobius/default_config.ini\n"
              "or consult the repository maintainer.")
        sys.exit()


def check():
    if path.exists("config.ini"):
        return True
    else:
        print("[WARN]: No config detected.")
        download()

