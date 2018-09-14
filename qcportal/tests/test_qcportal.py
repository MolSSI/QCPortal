"""
Unit and regression test for the qcportal package.
"""

# Import package, test suite, and other packages as needed
import qcportal
import pytest
import sys

def test_qcportal_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "qcportal" in sys.modules
