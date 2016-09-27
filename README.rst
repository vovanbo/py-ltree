Python ltree implementation
===========================

``ltree`` is a sequence of labels that can be used to represent a hierarchical
tree-like structure. The `PostgreSQL database`__ provides an `ltree data
type`__ with very powerful indexing functionalities, making it a practical way
to store tree-like information in a relational database, often more flexible
or performing than implementing an `adjacency list`__  or `nested set`__.

.. __: http://www.postgresql.org/
.. __: http://www.postgresql.org/docs/current/static/ltree.html
.. __: https://en.wikipedia.org/wiki/Adjacency_list
.. __: https://en.wikipedia.org/wiki/Nested_set_model

This extension module contains objects to help manipulating ``ltree``
in Python and interacting with the PostgreSQL data types using psycopg__

.. __: http://initd.org/psycopg/


``Ltree`` object
----------------

``Ltree`` objects can be created from a string containing a dot-separated
sequence of labels, a python sequence of labels or multiple arguments. Valid
labels are sequences of alphanumeric ascii characters and underscore. Empty
strings and ``None`` are skipped.::

    >>> from ltree import Ltree

    >>> Ltree('a.b.c')
    Ltree('a.b.c')

    >>> Ltree(['a', '', 'b', 0, None, 'c'])
    Ltree('a.b.0.c')

    >>> Ltree('a', '', 'b', 0, None, 'c')
    Ltree('a.b.0.c')

``Ltree`` objects can also be concatenated to other ltree or other objects
representing valid labels. They can be sliced as a normal Python sequence:
slicing will return a new ``Ltree`` object; accessing by index will return the
label as a string::

    >>> 'first' + Ltree('a.b') + Ltree('c') + 42
    Ltree('first.a.b.c.42')

    >>> Ltree('a.b.c.d.e.f.g')[:2]
    Ltree('a.b')

    >>> Ltree('a.b.c.d.e.f.g')[5:]
    Ltree('f.g')

    >>> Ltree('a.b.c.d.e.f.g')[1:3]
    Ltree('b.c')

    >>> Ltree('a.b.c.d.e.f.g')[2]
    'c'


``Lquery`` object
-----------------

The ``Lquery`` object works similarly to ``Ltree`` but also supports star
symbols. Sequence of stars get merged together (because PostgreSQL lquery not
always does the right thing with two stars in a row)::

    >>> from ltree import Lquery

    >>> Lquery('a.*.b')
    Lquery('a.*.b')

    >>> Lquery('a.*{1}') + Lquery('*{2}.b')
    Lquery('a.*{3}.b')

    >>> Lquery('a.*{1}') + Lquery('*.b')
    Lquery('a.*{1,}.b')


Using with psycopg2
-------------------

In order to pass ``Ltree`` and ``Lquery`` objects to psycopg2 you can register
the ltree adapters using the ``ltree.pg.register_ltree()`` function. Because
the ``ltree`` type doesn't have a fixed OID, the function takes a connection
or cursor as argument to look it up::

    >>> import psycopg2
    >>> cnn = psycopg2.connect('')

    >>> import ltree.pg
    >>> ltree.pg.register_ltree(cnn)

Once the adaptation bits are in place shuttling ``Ltree`` back and forth the
database is a breeze::

    >>> cur = cnn.cursor()
    >>> cur.execute('select %s::ltree', [Ltree('a.b.c')])
    >>> cur.fetchone()[0]
    Ltree('a.b.c')

    >>> cur.execute(
    ...     "select %s::ltree ~ %s::lquery",
    ...     [Ltree('a.b.c'), Lquery('a.*')])
    >>> cur.fetchone()[0]
    True


Using with Django
-----------------

The ``ltree.django`` module contains some Django helper. Importing it will
registers the ``lqmatch`` lookup, which can be used to filter a model for
``lquery`` matching (the ``~`` operator)::

    objs = MyModel.objects.filter(code__lqmatch=Lquery('a.b.*'))  #doctest: +SKIP
