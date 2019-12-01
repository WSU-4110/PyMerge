import subprocess
import sys


def check():
    try:
        import PyQt5
        print("PyQt5 dependency satisfied.")
    except ImportError:
        print("Couldn't find PyQt5 dependency, attempting to install...")
        install("PyQt5")


def install(package):
    try:
        subprocess.call([sys.executable, "-m", "pip", "install", package])
    except:
        print(f"There was an error trying to install {package}")