_instances = {}


def singleton(cls):
    def wrapper(*args, **kwargs):
        if cls in _instances.keys():
            return _instances.get(cls)

        _instances.update({cls: cls(*args, **kwargs)})
        return _instances.get(cls)

    return wrapper
