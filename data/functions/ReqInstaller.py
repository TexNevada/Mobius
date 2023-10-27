import os
import sys
import subprocess


def installer():
    print("[INFO]: Installing requirements")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("[INFO]: Checking for any additional requirements by the cogs")
    install_requirements_in_directory("data/cogs")
    print("\n[INFO]: Rerun the program to continue"
          "\n[INFO]: Exiting...")
    sys.exit()


def install_requirements_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'requirements.txt':
                requirements_path = os.path.join(root, file)
                if os.path.exists(requirements_path):
                    print(f"[INFO]: Installing requirements in {requirements_path}")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
                else:
                    print(f"[INFO]: Installer not found in {root}")


def check():
    # try:
    #     import discord
    #     import aiohttp
    #     import requests
    #     import mysql.connector
    #     import colorama
    #     import topgg
    # except ImportError:
    #     installer()
    installer()
