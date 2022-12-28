"""
A module that helps in opening the any input or output file and provide
necessary error messages if there is any exception encountered
Here, we have a connection between submodules, i.e. my_io is using config and
we are using Absolute Module Imports
"""

import os
import config


def get_fh(file=None, mode=None):
    """
    filehandle : get_fh(infile, "r")
    Takes : 2 arguments file name and mode i.e. what is needed to be done
    with this file. This function open the file based on the mode
    passed in the argument
    and returns filehandle.
    :param file: The file to open for the mode
    :param mode: The way to open the file, for e.g. reading, writing, etc.
    :return: filehandle
    """
    try:
        file_obj = open(file, mode)
        return file_obj
    except OSError:  # using submodules to handle exceptions gracefully
        config.get_error_string_4_opening_file_OSError(file, mode)
        raise
    except ValueError:
        # test something like my_io.get_fh("does_not_exist.txt", "rr")
        config.get_error_string_4_ValueError()
        raise
    except TypeError:
        # test something like my_io.get_fh([], "r")
        config.get_error_string_4_TypeError()
        raise


def is_valid_gene_file_name(file=None):
    """
    function that checks whether the given file name exists
    :param file: the file name
    :return: True or False
    """
    try:
        get_file_status = os.path.exists(file)
    except FileNotFoundError:
        # if the file is only a string with no /, you'll get :
        # No such file or directory: ''
        config.get_error_string_4_FileNotFoundError(file)
        raise

    return get_file_status