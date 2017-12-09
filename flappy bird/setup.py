import os
import sys
from distutils.core import setup

import py2exe, numpy

def numpy_dll_paths_fix():
    paths = set()
    np_path = numpy.__path__[0]
    for dirpath, _, filenames in os.walk(np_path):
        for item in filenames:
            if item.endswith('.dll'):
                paths.add(dirpath)

    sys.path.append(*list(paths))

numpy_dll_paths_fix()

origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
    dlls = ("libfreetype-6.dll", "libogg-0.dll", "sdl_ttf.dll")
    if os.path.basename(pathname).lower() in dlls:
        return 0
    return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL

sys.argv.append('py2exe')

setup(
    name =    'Flappy Bird',
    version = '1.0',
    author =  'Lomar Lilly',
    options = {
        'py2exe': {
            'bundle_files': 1, # doesn't work on win64
            'compressed': True,
        }
    },

    windows = [{
        'script': "flappy.py",
        'icon_resources': [
            (1, 'flappy.ico')
        ],
        'uac_info': "requireAdministrator"
    }],

    zipfile=None,
)
