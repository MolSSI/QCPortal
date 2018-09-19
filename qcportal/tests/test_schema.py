"""
Tests the various schema involved in the project that are not tested elsewhere.
"""

from . import portal


def test_options():
    opts = portal.data.get_options("psi_default")

    portal.schema.validate(opts, "options")
