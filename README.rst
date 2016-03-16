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
