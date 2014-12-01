# -*- coding: utf-8 -*-

from helpers import identity


class Chain(object):
    """
    Allows to chain methods of mutable builtins or custom classes,
    without the hassle of derivating classes, wich can be quite tricky for builtins,
    see: http://yauhen.yakimovich.info/blog/2011/08/12/wrapping-built-in-python-types/
    This class does not recast immutable results, it simply changes inner instance.
    Seems useless to use on immutable builtins.
    """

    def __init__(self, obj):
        self.wrapped = obj

    def __getattr__(self, item):
        def method(*args, **kwarsg):
            ret = getattr(self.wrapped, item)(*args, **kwarsg)
            # methods returning None or self are chained with same wrapper/object
            if ret is None or ret is self.wrapped:
                return self
            # muted result instances are set as new wrapped object
            if isinstance(ret, self.wrapped.__class__):
                return self._push(ret)
            return ret
        return method

    def _push(self, obj):
        self.wrapped = obj
        return self

    def reveal(self, cls=None):
        cls = cls or self._reveal_class
        return cls(self.wrapped)

    def __str__(self):
        return str(self.wrapped)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.wrapped)


class RecastingChain(Chain):
    """
    This class recasts immutable results.
    """

    def _push(self, obj):
        return self.__class__(obj)


class HistoryChain(Chain):
    """
    This class changes inner instance and records past instances.
    """

    def __init__(self, obj):
        Chain.__init__(self, obj)
        self.history = [obj]

    def _push(self, obj):
        self.wrapped = obj
        self.history.append(obj)
        return self

    def backward(self):
        self.history.pop()
        self.wrapped = self.history[-1]
        return self


class SequenceMixin(object):

    _reveal_class = list

    def __iter__(self):
        return iter(self.wrapped)

    def all(self, f=bool):
        return all(f(x) for x in self)

    def any(self, f=bool):
        return any(f(x) for x in self)

    def first(self, f=bool):
        for x in self:
            if f(x):
                return x

    def aggregate(self, f=identity, op=identity):
        return reduce(op, (f(x) for x in self))

    def where(self, f=bool):
        return self._push(x for x in self if f(x))

    def select(self, f=identity):
        return self._push(f(x) for x in self)


class MappingMixin(object):

    _reveal_class = dict

    def __iter__(self):
        try:
            return self.wrapped.iteritems()
        except AttributeError:
            return iter(self.wrapped)

    def all(self, f=identity):
        return all(f(k, v) for k, v in self)

    def any(self, f=identity):
        return any(f(k, v) for k, v in self)

    def aggregate(self, f=identity, op=identity):
        return reduce(op, (f(k, v) for k, v in self))

    def where(self, f=identity):
        return self._push((k, v) for k, v in self if f(k, v))

    def select(self, f=identity):
        return self._push(f(k, v) for k, v in self)


class SequenceChain(SequenceMixin, Chain):
    pass


class MappingChain(MappingMixin, Chain):
    pass
