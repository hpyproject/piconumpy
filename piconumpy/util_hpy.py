from pathlib import Path

from hpy.universal import load_from_spec


class Spec:
    def __init__(self, name, origin):
        self.name = name
        self.origin = origin


def import_from_path(path):
    path = Path(path)
    return load_from_spec(Spec(path.name.split(".", 1)[0], str(path)))


def import_ext():
    path = Path(__file__).parent / "_piconumpy_hpy.hpy.so"
    return import_from_path(path)
