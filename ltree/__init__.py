import re
from functools import total_ordering
from collections import Sequence

re_ltree = re.compile('^[a-zA-Z0-9_]+$')


@total_ordering
class Ltree(tuple):
    """Wrapper for the Ltree data type."""
    __slots__ = ()

    def __new__(cls, *args):
        def _label(s):
            if s is None or s == '':
                return None
            if isinstance(s, basestring):
                if re_ltree.match(s):
                    return s
                else:
                    raise ValueError('ltree label not valid: %s' % s)
            else:
                return _label(str(s))

        labels = []

        for arg in args:
            if isinstance(arg, basestring):
                labels += map(_label, arg.split('.'))
            elif isinstance(arg, Sequence):
                labels += map(_label, arg)
            else:
                labels.append(_label(arg))

        return tuple.__new__(cls, (l for l in labels if l is not None))

    def __eq__(self, other):
        if isinstance(other, Ltree):
            return tuple.__eq__(self, other)
        elif isinstance(other, basestring):
            return str(self) == other
        else:
            return self.__eq__(Ltree(other))

    def __lt__(self, other):
        if isinstance(other, Ltree):
            return tuple.__lt__(self, other)
        elif isinstance(other, basestring):
            return str(self) < other
        else:
            return self.__lt__(Ltree(other))

    def __add__(self, other):
        return Ltree(self, other)

    def __radd__(self, other):
        return Ltree(other, self)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, '.'.join(self))

    def __str__(self):
        return '.'.join(self)
