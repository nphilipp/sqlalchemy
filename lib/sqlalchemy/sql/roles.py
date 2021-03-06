# sql/roles.py
# Copyright (C) 2005-2019 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


class SQLRole(object):
    """Define a "role" within a SQL statement structure.

    Classes within SQL Core participate within SQLRole hierarchies in order
    to more accurately indicate where they may be used within SQL statements
    of all types.

    .. versionadded:: 1.4

    """


class UsesInspection(object):
    pass


class ColumnArgumentRole(SQLRole):
    _role_name = "Column expression"


class ColumnArgumentOrKeyRole(ColumnArgumentRole):
    _role_name = "Column expression or string key"


class ColumnListRole(SQLRole):
    """Elements suitable for forming comma separated lists of expressions."""


class TruncatedLabelRole(SQLRole):
    _role_name = "String SQL identifier"


class ColumnsClauseRole(UsesInspection, ColumnListRole):
    _role_name = "Column expression or FROM clause"

    @property
    def _select_iterable(self):
        raise NotImplementedError()


class LimitOffsetRole(SQLRole):
    _role_name = "LIMIT / OFFSET expression"


class ByOfRole(ColumnListRole):
    _role_name = "GROUP BY / OF / etc. expression"


class OrderByRole(ByOfRole):
    _role_name = "ORDER BY expression"


class StructuralRole(SQLRole):
    pass


class StatementOptionRole(StructuralRole):
    _role_name = "statement sub-expression element"


class WhereHavingRole(StructuralRole):
    _role_name = "SQL expression for WHERE/HAVING role"


class ExpressionElementRole(SQLRole):
    _role_name = "SQL expression element"


class ConstExprRole(ExpressionElementRole):
    _role_name = "Constant True/False/None expression"


class LabeledColumnExprRole(ExpressionElementRole):
    pass


class BinaryElementRole(ExpressionElementRole):
    _role_name = "SQL expression element or literal value"


class InElementRole(SQLRole):
    _role_name = (
        "IN expression list, SELECT construct, or bound parameter object"
    )


class FromClauseRole(ColumnsClauseRole):
    _role_name = "FROM expression, such as a Table or alias() object"

    _is_subquery = False

    @property
    def _hide_froms(self):
        raise NotImplementedError()


class StrictFromClauseRole(FromClauseRole):
    # does not allow text() or select() objects
    pass


class AnonymizedFromClauseRole(StrictFromClauseRole):
    # calls .alias() as a post processor

    def _anonymous_fromclause(self, name=None, flat=False):
        """A synonym for ``.alias()`` that is only present on objects of this
        role.

        This is an implicit assurance of the target object being part of the
        role where anonymous aliasing without any warnings is allowed,
        as opposed to other kinds of SELECT objects that may or may not have
        an ``.alias()`` method.

        The method is used by the ORM but is currently semi-private to
        preserve forwards-compatibility.

        """
        return self.alias(name=name, flat=flat)


class CoerceTextStatementRole(SQLRole):
    _role_name = "Executable SQL, text() construct, or string statement"


class StatementRole(CoerceTextStatementRole):
    _role_name = "Executable SQL or text() construct"


class ReturnsRowsRole(StatementRole):
    _role_name = (
        "Row returning expression such as a SELECT, a FROM clause, or an "
        "INSERT/UPDATE/DELETE with RETURNING"
    )


class SelectStatementRole(ReturnsRowsRole):
    _role_name = "SELECT construct or equivalent text() construct"

    def subquery(self):
        raise NotImplementedError(
            "All SelectStatementRole objects should implement a "
            ".subquery() method."
        )


class HasCTERole(ReturnsRowsRole):
    pass


class CompoundElementRole(SQLRole):
    """SELECT statements inside a CompoundSelect, e.g. UNION, EXTRACT, etc."""

    _role_name = (
        "SELECT construct for inclusion in a UNION or other set construct"
    )


class DMLRole(StatementRole):
    pass


class DMLColumnRole(SQLRole):
    _role_name = "SET/VALUES column expression or string key"


class DMLSelectRole(SQLRole):
    """A SELECT statement embedded in DML, typically INSERT from SELECT """

    _role_name = "SELECT statement or equivalent textual object"


class DDLRole(StatementRole):
    pass


class DDLExpressionRole(StructuralRole):
    _role_name = "SQL expression element for DDL constraint"


class DDLConstraintColumnRole(SQLRole):
    _role_name = "String column name or column object for DDL constraint"
