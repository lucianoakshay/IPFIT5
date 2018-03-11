from subprocess import call

def InstallPip():
    from os import remove
    from urllib import request
    request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", "get-pip.py")
    call(["python", "get-pip.py"])
    remove("get-pip.py")

def GetPip():
    from os.path import isfile, join
    import os
    from sys     import prefix
    from subprocess import Popen, PIPE
    finder = Popen(['where' if os.name() == 'nt' else 'which', 'pip'], stdout = PIPE, stderr = PIPE)
    pipPath = finder.communicate()[0].strip()
    if not isfile(pipPath):
        InstallPip()
        if not isfile(pipPath):
            raise("Failed to find or install pip!")
    return pipPath


def installIfNeeded(moduleName, nameOnPip=None, notes="", log=print):
    """ Installs a Python library using pip, if it isn't already installed. """
    from pkgutil import iter_modules

    # Check if the module is installed
    if moduleName not in [tuple_[1] for tuple_ in iter_modules()]:
        log("Installing " + moduleName + notes + " Library for Python")
        call([GetPip(), "install", nameOnPip if nameOnPip else moduleName])
