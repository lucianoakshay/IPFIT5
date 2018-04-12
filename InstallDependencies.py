import pip
import os
import sys
from subprocess import STDOUT, check_call

def installer (requirements):
    check_call(['apt-get', 'install', '-y', 'python3-tk'],
     stdout=open(os.devnull,'wb'), stderr=STDOUT)
    if os.path.isfile(requirements):
        pip.main(["install", "-r", str(requirements)])
    else:
        print("requirements.txt couldn't be found")

installer("requirements.txt")
