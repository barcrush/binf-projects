""" Test suite for the module: config.py"""
import sys

from assignment5 import config
sys.path.insert(1, '/Users/yogeshmaithania/PycharmProjects/assignment5/assignment5')

# ignore all "Missing function or method docstring" since this is a unit test
# pylint: disable=C0116
# Ignore all "Function name "test_get_fh_4_OSError" doesn't conform to snake_case naming style"
# pylint: disable=C0103

def test_get_unigene_directory():
     assert isinstance(config.get_unigene_directory(), str) is True, \
         "Not able get unigene directory"


def test_get_unigene_extension():
     assert isinstance(config.get_unigene_extension(), str) is True, \
        "Not able get unigene extension"


def test_get_host_keywords():
    # testing for the host name dictionaries
    assert isinstance(config.get_host_keywords(), dict) is True, \
        "Not able get unigene keyword dict"