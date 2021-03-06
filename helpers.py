# -*- coding: utf-8 -*-


def mixin_factory(name, base, *mixins):
    return type(name, (base,) + mixins, {})


def add_attributes(**kwargs):
    def wrapped(obj):
        obj.__dict__.update(kwargs)
        return obj
    return wrapped


def add_attribute_self(name):
    """
    Use to set a class attribute refering to the class itself
    This can't be done simply in Python
    """
    def wrapped(obj):
        setattr(obj, name, obj)
        return obj
    return wrapped


def yesman(*arsg):
    return True


def identity(*args):
    if len(args) == 1:
        return args[0]
    return args
