"""
File: gene_information_query.py

This program checks for the existence of directory of host and file of genes
if the gene file exists it displays that gene is expressed in which all organs.

Sample command for executing the program:
python3 gene_information_query.py --host Homo_sapiens --gene TGM1

"""
import argparse
import os
import sys
import re
from operator import methodcaller

# Absolute Module Imports
from helper import my_io, config


def main():
    """ Business logic  """
    args = get_cli_args()
    host, gene = args.host, args.gene
    # making our user input case-sensitive
    temp_host = host
    temp_host = temp_host.replace("_", " ")  # update the host
    gene_exp = gene.upper()
    # get the modified host name from the host dictionary
    host = modify_host_name(temp_host)
    # creating gene file path name
    file = os.path.join(config.get_unigene_directory(),
                        host, gene_exp + "." + config.get_unigene_extension())
    # check for the existence of file
    if my_io.is_valid_gene_file_name(file):
        # using f-strings to print the statements
        print(f"\nFound Gene {gene_exp} for {temp_host}")
    else:
        print("Not found")
        print(f"Gene {gene_exp} does not exist for {temp_host}. "
              f"Exiting now...", file=sys.stderr)
        sys.exit(1)

    # getting the list of tissues expressed by the gene
    tissue_list = get_gene_data(file=file)
    # printing the final output result
    print_output(host=host, gene=gene, list_vals=tissue_list)


def modify_host_name(host_name: str) -> [str]:
    # Optional tells the type checker that either an object of
    """
    Takes: 1 argument i.e. a host name and maps it to the dictionary of
    host keywords and returns its corresponding scientific name
    :param host_name: a host name
    :return: a scientific name
    """
    # get host name dictionary
    if host_name is not None:
        host_name = host_name.replace("_", " ")
        host_name = host_name.lower()
    host_keyword = config.get_host_keywords()
    # test if the host was found
    # getting the appropriate host name from the host dictionary
    if host_name in host_keyword:
        host_name = host_keyword[host_name]  # get scientific name
    else:
        _print_host_directories()
        sys.exit(2)

    return host_name

def _print_host_directories() -> None:
    """
    function that prints out the host directories that do exists,
    thereby giving a message for the user to look for an appropriate
    host name for their use
    :return: None
    """
    hostlist1 = ['Homo_sapiens', 'Bos_taurus', 'Equss_caballus',
                 'Mus_musculus', 'Ovis_aries', 'Rattus_norvegicus']
    hostlist2 = ['Bos taurus', 'Cow', 'Cows', 'Equus caballus', 'Homo sapiens',
                 'Horse', 'Horses', 'Human', 'Humans', 'Mice', 'Mouse',
                 'Mus musculus', 'Ovis aries', 'Rat', 'Rats',
                 'Rattus norvegicus', 'Sheep', 'Sheeps']
    print("\nEither the Host Name you are searching "
          "for is not in the database\n")
    print("or If you are trying to use the scientific please put the name in "
          "double quotes:\n")
    print(f'"Scientific name"\n')
    print("Here is a (non-case sensitive) list of available Hosts "
          "by scientific name\n")
    for idx, common_names in enumerate(hostlist1):
        print("{:3d}. {}".format(idx + 1, common_names))
    print("\n\nHere is a (non-case sensitive) list of "
          "available Hosts by common name\n")
    for idx, sci_names in enumerate(hostlist2):
        print("{:3d}. {}".format(idx + 1, sci_names))


def get_gene_data(file) -> list:
    """
    Takes: 1 argument as a gene file and parses through the file to curate
    a list of tissues expressed by the corresponding gene
    :param file: a gene file name
    :return: list of genes expressed
    """
    # initialize a list
    get_list = []
    with my_io.get_fh(file, "r") as fh_in:
        for line in fh_in:
            line = line.rstrip()
            # using compile to create our match in the unigene file
            reg_exp = re.compile(r'^EXPRESS\s+(.*)$')
            match = re.search(reg_exp, line)
            if match:
                tissue_string = match.group(1).split('|')  # grouping
                for idx in map(methodcaller('lstrip'), tissue_string):
                    get_list.append(idx)

    return get_list


def print_output(host, gene, list_vals) -> list:
    """
    Takes : 3 arguments and prints out the final output
    which is based user-dependent input for the host name
    and gene they are looking for
    :param host: host name
    :param gene: gene name
    :param list_vals: list of tissues expressed by the gene
    :return: None
    """
    print(f"In {host}, there are {len(list_vals)} tissues that "
          f"{gene} is expressed in:\n")
    for idx, tissue_name in enumerate(sorted(list_vals)):
        print("{:3d}. {}".format(idx + 1, tissue_name))


def get_cli_args():
    """
    Just get the command line options using argparse
    :return: Instance of argparse arguments
    """
    parser = argparse.ArgumentParser(description='Give the Host and Gene name')

    parser.add_argument('-host', dest='host', type=str,
                        help='Name of Host', required=False,
                        default='Human')

    parser.add_argument('-gene', dest='gene', type=str,
                        help='Name of Gene', required=False,
                        default='TGM1')

    return parser.parse_args()


if __name__ == '__main__':
    main()