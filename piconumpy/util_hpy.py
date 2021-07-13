from pathlib import Path

from hpy.universal import load


def import_from_path(path):
    ext_filepath = str(path)
    m = load('_piconumpy_hpy', ext_filepath)
    m.__file__ = ext_filepath
    m.__loader__ = __loader__
    m.__name__ = __name__
    m.__package__ = __package__
    m.__spec__ = __spec__
    return m


def import_ext():
    path = Path(__file__).parent / "_piconumpy_hpy.hpy.so"
    return import_from_path(path)
