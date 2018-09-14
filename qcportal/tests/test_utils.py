"""
Tests for the interface utility functions.
"""

from ... import interface as portal


def test_replace_dict_keys():

    ret = portal.dict_utils.replace_dict_keys({5: 5}, {5: 10})
    assert ret == {10: 5}

    ret = portal.dict_utils.replace_dict_keys({5: 5}, {10: 5})
    assert ret == {5: 5}

    ret = portal.dict_utils.replace_dict_keys([{5: 5}], {10: 5})
    assert ret == [{5: 5}]

    ret = portal.dict_utils.replace_dict_keys({5: {5: 10}}, {5: 10})
    assert ret == {10: {10: 10}}
