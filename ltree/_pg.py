import sys
from ._ltree import Ltree


def register_ltree(conn_or_curs, globally=False, oid=None, array_oid=None):
    """Register the ltree adapter and typecaster on the connection or cursor.
    """
    conn, curs, conn_or_curs = _solve_conn_curs(conn_or_curs)

    import psycopg2
    import psycopg2.extensions as ext

    if oid is None:
        oid = get_oids(conn_or_curs, 'ltree')
        if oid is None or not oid[0]:
            raise psycopg2.ProgrammingError(
                "ltree type not found in the database.")
        else:
            array_oid = oid[1]
            oid = oid[0]

    if isinstance(oid, int):
        oid = (oid,)

    if array_oid is not None:
        if isinstance(array_oid, int):
            array_oid = (array_oid,)
        else:
            array_oid = tuple([x for x in array_oid if x])

    # create and register the typecaster
    def cast_ltree(s, cur):
        if s is not None:
            return Ltree(s)

    LTREE = ext.new_type(oid, "LTREE", cast_ltree)
    ext.register_type(LTREE, not globally and conn_or_curs or None)

    if array_oid:
        LTREEARRAY = ext.new_array_type(array_oid, "LTREEARRAY", LTREE)
        ext.register_type(LTREEARRAY, not globally and conn_or_curs or None)


def get_oids(conn_or_curs, type_name):
    """Return the lists of OID of a type with given name.
    """
    import psycopg2.extensions as ext
    conn, curs, conn_or_curs = _solve_conn_curs(conn_or_curs)

    # Store the transaction status of the connection to revert it after use
    conn_status = conn.status

    rv0, rv1 = [], []

    # get the oid for the ltree
    curs.execute("""\
        select t.oid, typarray
        from pg_type t join pg_namespace ns
            on typnamespace = ns.oid
        where typname = %s
        """, (type_name,))

    for oids in curs:
        rv0.append(oids[0])
        rv1.append(oids[1])

    # revert the status of the connection as before the command
    if (conn_status != ext.STATUS_IN_TRANSACTION and not conn.autocommit):
        conn.rollback()

    return tuple(rv0), tuple(rv1)


def _solve_conn_curs(conn_or_curs):
    """Return the connection and a DBAPI cursor from a connection or cursor.
    """
    import psycopg2
    import psycopg2.extensions as ext

    if conn_or_curs is None:
        raise psycopg2.ProgrammingError("no connection or cursor provided")

    if hasattr(conn_or_curs, 'execute'):
        conn = conn_or_curs.connection
        curs = conn.cursor(cursor_factory=ext.cursor)

        # Django wrapper
        mod = sys.modules.get('django.db.backends.utils')
        if mod is not None:
            if isinstance(conn_or_curs, mod.CursorWrapper):
                conn_or_curs = conn_or_curs.cursor
    else:
        conn = conn_or_curs
        curs = conn.cursor(cursor_factory=ext.cursor)
        conn_or_curs = curs.connection

    return conn, curs, conn_or_curs
