import importlib, pkgutil


def import_submodules(package, recursive=True):
    """!
    Import all submodules of a module, recursively, including subpackages.
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = dict()
    for _, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = ".".join((package.__name__, name))
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results
