import sys
import subprocess


def installer():
    print("[INFO]: Downloading requirements")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("\n[INFO]: Rerun the program to continue"
          "\n[INFO]: Exiting...")
    sys.exit()


def check():
    try:
        import discord
        import requests
    except ImportError:
        installer()
