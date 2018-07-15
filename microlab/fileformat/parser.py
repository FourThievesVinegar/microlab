from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def validate(data):
    """
    Ensure the file format is correct for its version and that
    the steps, etc, are sane.
    """
    pass


def load_data(filepath):
    with open(filepath, "r") as f:
        return load(f, Loader=Loader)

