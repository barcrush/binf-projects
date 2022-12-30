"""
A script that generates a nested dictionary from the Unigene files downloaded from the web.
"""

import re
from operator import methodcaller

def get_unigene_data_structure(file):  # noqa: C901 this if for flake8 ignoring
    """
    function that draws the gene data into a dictionary
    @param file: a file and parses with regular expression
    @return: Complex nested data structure of the data
    """

    # values to get
    expression_list, protsim_list, seq_list = [], [], []

    dictionary_2_return = _init_dictionary_2_return()
    reg_exps = _get_compiled_regex()
    # go over lines and store
    with open(file, "r") as in_fh:

        for line in in_fh:
            line = line.rstrip()
            # the first three regex are good to match first, since they have the most lines
            # in the file to match, so we will hit them the most, so we want to move them at the top
            if _is_match_to_protsim(line=line, reg_exps=reg_exps, list_vals=protsim_list):
                pass
            elif _is_match_to_sequence(line=line, reg_exps=reg_exps, list_vals=seq_list):
                pass
            elif _is_match_to_express(line=line, reg_exps=reg_exps, list_vals=expression_list):
                 pass
            else:
                _match_to_generic_key(line=line, reg_exps=reg_exps, dictionary_2_return=dictionary_2_return)

    # set these at the end to create the complex data structure
    dictionary_2_return['PROTSIM'] = protsim_list
    dictionary_2_return['SEQUENCE'] = seq_list
    dictionary_2_return['EXPRESS'] = expression_list
    # now return the data structure
    return dictionary_2_return


def _get_compiled_regex():
    """
    You can speed up your searches and matches by 'compiling' the regex,
    Note the keyword compile: This just return a dictionary of those compiled matches.
    What's nice about having them in a dictionary, you have all regexps all in one place, adn then
    you can look up a given regular expression by a key when you come the need for it when parsing
    @return: Complex nested data structure of the data
     """

    return {
     'CHROMOSOME': re.compile(r'^CHROMOSOME\s+(.*)$'),
     'CYTOBAND': re.compile(r'^CYTOBAND\s+(.*)$'),
     'GENE': re.compile(r'^GENE\s+(.*)$'),
     'GENE_ID': re.compile(r'^GENE_ID\s+(.*)$'),
     'HOMOL': re.compile(r'^HOMOL\s+(.*)$'),
      'ID': re.compile(r'^ID\s+(.*)$'),
      'LOCUSLINK': re.compile(r'^LOCUSLINK\s+(.*)$'),
      'TITLE': re.compile(r'^TITLE\s+(.*)$'),

      # extra processing was needed for these three keys
     'PROTSIM': re.compile(r'^PROTSIM\s+(.*)$'),
      'SEQUENCE': re.compile(r'^SEQUENCE\s+(.*)$'),
      'EXPRESS': re.compile(r'^EXPRESS\s+(.*)$')
    }


def _is_match_to_protsim(line=None, reg_exps=None, list_vals=None):
    """
    Just update the list_vals if there was a match to PROTSIM
    @param line: New line to parse
    @param reg_exps: The Dictionary of regular expression
    @param list_vals: The reference to the list to store
    @return: Boolean
    """

    # re.search find something anywhere in the string and return a match object.
    # re.match find something at the beginning of the string and return a match object.
    # so, re.match is faster if you can use it!

    # match nested key-value values below here:
    match = reg_exps['PROTSIM'].match(line)
    # more complex data wrangling needed
    if match:
        dict_ = _get_dictionary(match)

        # then fix some of the string values
        dict_['ORG'] = int(dict_['ORG'])
        dict_['PROTGI'] = int(dict_['PROTGI'])
        dict_['PCT'] = float(dict_['PCT'])
        dict_['ALN'] = int(dict_['ALN'])
        # finally store
        list_vals.append(dict_)
        return True
    return False


def _is_match_to_sequence(line=None, reg_exps=None, list_vals=None):
    """
    Just update the list_vals if there was a match to SEQUENCE
    @param line: New line to parse
    @param reg_exps: The Dictionary of regular expression
    @param list_vals: The reference to the list to store
    @return: Boolean
    """
    match = reg_exps['SEQUENCE'].match(line)
    # more complex data wrangling needed
    if match:
        dict_ = _get_dictionary(match)

    # then fix some of the string values
        if 'TRACE' in dict_.keys():
            dict_['TRACE'] = int(dict_['TRACE'])
            if 'LID' in dict_.keys():
                dict_['LID'] = int(dict_['LID'])
        # finally store
        list_vals.append(dict_)
        return True
    return False


def _is_match_to_express(line=None, reg_exps=None, list_vals=None):
    """
    Just update the list_vals if there was a match to EXPRESS
    @param line: New line to parse
    @param reg_exps: The Dictionary of regular expression
    @param list_vals: The reference to the list to store
    @return: Boolean
    """
    # more complex data wrangling needed
    match = reg_exps['EXPRESS'].match(line)
    if match:
        # get a list
        temp = match.group(1).split('|')
        # strip of white space on the left,
        for i in map(methodcaller('lstrip'), temp):
            list_vals.append(i)

       #You can replace the loop with:
        list_vals[:] = list(map(methodcaller('lstrip'), temp))
        # Note the list_vals[:], since assignment would create a new label if you did list_vals =
        # So I prefer the loop
        return True
    return False


def _match_to_generic_key(line=None, reg_exps=None, dictionary_2_return=None):
    """
    Just update the dictionary_2_return if there was a match to one of the keys
    @param line: New line to parse
    @param reg_exps: The Dictionary of regular expression
    @param dictionary_2_return: The reference to the list to store
    @return: None
    """
    # looop through and do the rest of these simpler mathces
    for key, reg_exp in reg_exps.items():
        # match single key-value values below here:
        match = reg_exp.match(line)
        if match:
            dictionary_2_return[key] = match.group(1)


def _init_dictionary_2_return():
    """Simple function to initialize the data structure"""
    return {
     'CHROMOSOME': None,
     'CYTOBAND': None,
     'EXPRESS': None,
     'GENE': None,
     'GENE_ID': None,
     'HOMOL': None,
     'ID': None,
     'LOCUSLINK': None,
     'PROTSIM': None,
     'TITLE': None,
     'SEQUENCE': None
    }


def _get_dictionary(match):
    """
    @param match: object form a regular expression
    @return: dictionary of the values that were mapped in the match string
    """
    temp = match.group(1)
    # create the list on the first split
    values = temp.strip().split('; ')

    # then create a dictionary from the list, key value pairs
    return dict(item.split("=") for item in values)
