

def alias(cls, alias):
    def set_func(func):
        setattr(cls, alias, func)
    return set_func
