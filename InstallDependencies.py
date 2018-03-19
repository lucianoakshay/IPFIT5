import pip
import os
import sys

def installer (requirements):
    if os.path.isfile(requirements):
        pip.main(["install", "-r", str(requirements)])
    else:
        print("requirements.txt couldn't be found")

installer("requirements.txt")
