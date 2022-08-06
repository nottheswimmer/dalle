"""
This package contains all the imperative parts of PyDalle.

Specifically, none of the code OUTSIDE this package will:

* import any external libraries

* perform any external I/O

* have any side effects

Even within this package, any code which directly performs
I/O will be in the :mod:`pydalle.imperative.outside` package.
"""
