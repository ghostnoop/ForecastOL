def pprint(*args, **kwargs):
    pass


def singleton(cls):
    singletons = {}

    def get_instance(*args, **kwargs):
        if cls not in singletons:
            singletons[cls] = cls(*args, **kwargs)
        return singletons[cls]

    return get_instance
