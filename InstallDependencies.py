import pip
import os
import sys
from subprocess import STDOUT, check_call

def installer (requirements):
    os.system('sudo apt-get install python3-tk')
    if os.path.isfile(requirements):
        pip.main(["install", "-r", str(requirements)])
    else:
        print("requirements.txt couldn't be found")

installer("requirements.txt")
