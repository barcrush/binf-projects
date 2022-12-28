" Test suite for the module: my_io.py"""
import os
import sys
import pytest

# absolute module imports
from assignment5 import my_io
sys.path.insert(1, '/Users/yogeshmaithania/PycharmProjects/assignment5/assignment5')


# ignore all "Missing function or method docstring" since this is a unit test
# pylint: disable=C0116
# Ignore all "Function name "test_get_fh_4_OSError" doesn't conform to snake_case naming style"
# pylint: disable=C0103

FILE_2_TEST = "/Users/get_data_from_directory/test.unigene"

def test_existing_get_fh_4_reading():
    # does it open a file for reading
    # create a test file
    _create_test_file(FILE_2_TEST)
    # test
    test = my_io.get_fh(FILE_2_TEST, "r")
    assert hasattr(test, "readline") is True, "Not able to open for reading"
    test.close()
    os.remove(FILE_2_TEST)


def test_existing_get_fh_4_writing():
    # does it open a file for writing
    # test
    test = my_io.get_fh(FILE_2_TEST, "w")
    assert hasattr(test, "write") is True, "Not able to open for writing"
    test.close()
    os.remove(FILE_2_TEST)


def test_get_fh_4_OSError():
    # does it raise on OSError
    # this should exit
    with pytest.raises(OSError):
        my_io.get_fh("does_not_exist.txt", "r")


def test_get_fh_4_ValueError():
    # does it raise on ValueError
    # this should exit
    _create_test_file(FILE_2_TEST)
    with pytest.raises(ValueError):
        my_io.get_fh("does_not_exist.txt", "rrr")
    os.remove(FILE_2_TEST)


def test_get_fh_4_TypeError():
    # does it raise on TypeError
    # this should exit
    _create_test_file(FILE_2_TEST)
    with pytest.raises(TypeError):
        my_io.get_fh([], "r")
    os.remove(FILE_2_TEST)


def test_is_valid_gene_file_name_4_FileNotFoundError():
    # does it raise on FileNotFoundError
    # create a test file path
    file = "/Users/will_not_be_able_to_find/test.unigene"
    with pytest.raises(FileNotFoundError):
        my_io.is_valid_gene_file_name(file)


def _create_test_file(file):
    # not actually run, the are just helper funnctions for the test script
    # create a test file
    open(file, "w").close()