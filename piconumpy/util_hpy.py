from importlib.util import spec_from_file_location
from pathlib import Path

from hpy.universal import load


def import_from_path(path):
    name_ext = "_piconumpy_hpy"
    ext_filepath = str(path)
    spec = spec_from_file_location(name_ext, ext_filepath)
    m = load(name_ext, ext_filepath, spec)
    m.__file__ = ext_filepath
    m.__loader__ = __loader__
    m.__name__ = __name__
    m.__package__ = __package__
    return m


def import_ext():
    path = Path(__file__).parent / "_piconumpy_hpy.hpy0.so"
    return import_from_path(path)
