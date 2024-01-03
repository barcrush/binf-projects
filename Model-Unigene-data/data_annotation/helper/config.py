#!/usr/bin/env python3

"""
This short module is used for configuration
"""

# Error" doesn't conform to snake_case naming style
# pylint: disable=invalid-name

# This convention, starting with '_variable_name' is used for declaring private
# variables, functions, methods and classes in a module.
# Anything with this convention are ignored in from module import *.
# But technically, Python does not supports truly private
_UNIGENE_DIR = "/Family"
_UNIGENE_FILE_ENDING = "unigene"


def get_error_string_4_ValueError():  # error when used get_fh(file, "1234")
    """
    Print the invalid argument message for ValueError
    """
    print("Invalid argument Value for opening a file for reading/writing")


def get_error_string_4_TypeError():  # error when used get_fh(file, "r", "w")
    """
    Print the invalid argument message for TypeError
    """
    print("Invalid argument Type passed in")


def get_error_string_4_FileNotFoundError(file=None):
    """
    Print the invalid argument message for FileNotFoundError
    @param file: The file name
    """
    print(f"Could not create the directory (invalid argument): {file}")


def get_error_string_4_opening_file_OSError(file=None, mode=None):
    """
    Print the invalide argument message for OSError
    @param file: The file name
    @param mode: The mode to open the file
    """
    print(f"Could not open the file (os error): {file} with mode '{mode}'")


def get_error_string_4_opening_directory_OSError(directory=None):
    """
    Print the invalid argument message for OSError when open/making a directory
    @param directory: The directory opened
    """
    print(f"Could not open/make directory (os error): {directory}")


def get_unigene_directory():
    """
    function that returns an absolute path to working directory for the
    program (directory for unigene data)
    :return: The path to the unigene directory
    """
    return _UNIGENE_DIR


def get_unigene_extension():
    """
    function that gives a file extension for any unigene data file
    :return: Returns "unigene" variable
    """
    return _UNIGENE_FILE_ENDING


def get_host_keywords():
    """
    function that gives a dictionary for mapping common names
    with scientific names
    :return: A dictionary of host names
    """
    # assigning directory names
    homo_sapiens = "Homo_sapiens"
    bos_taurus = "Bos_taurus"
    equus_caballus = "Equus_caballus"
    mus_musculus = "Mus_musculus"
    ovis_aries = "Ovis_aries"
    rattus_norvegicus = "Rattus_norvegicus"

    # dictionary for mapping common names with scientific names
    host_keywords = {
        "homo sapiens": homo_sapiens,
        "human": homo_sapiens,
        "humans": homo_sapiens,

        "bos taurus": bos_taurus,
        "cow": bos_taurus,
        "cows": bos_taurus,

        "equus caballus": equus_caballus,
        "horse": equus_caballus,
        "horses": equus_caballus,

        "mus musculus": mus_musculus,
        "mouse": mus_musculus,
        "mice": mus_musculus,

        "ovis aries": ovis_aries,
        "sheep": ovis_aries,
        "sheeps": ovis_aries,

        "rattus norvegicus": rattus_norvegicus,
        "rat": rattus_norvegicus,
        "rats": rattus_norvegicus
    }
    return host_keywords
