"""
Functions for modelling genetic drift of different alleles in a population. Code plotting the genetic drift simulations is also included.
"""

import random
import pylab as plb

def allele_freq(allele, population):
    """
    Calculate the frequency of a specific allele in a population.

    @param:
        allele (str): The allele to be counted.
        population (list): A list of alleles in the population.

    @return:
        float: Frequency of the input allele.
    """
    return population.count(allele) / len(population)

def modelDrift_AB(pop_size, n_gens):
    """
    Model the genetic drift of alleles A and B in a population over n generations.
    Returns lists for the frequency of alleles A and B over n generations.

    @param:
        pop_size (int): Size of the population to be modeled.
        n_gens (int): Number of generations to model the population over.

    @return:
        tuple: Two lists containing the frequency of allele A and B for each n generation.
    """
    pop_A = ['A' for i in range(int(pop_size/2))]
    pop_B = ['B' for i in range(int(pop_size/2))]
    population = pop_A + pop_B

    freq_A = [allele_freq('A', population)]
    freq_B = [allele_freq('B', population)]

    for i in range(n_gens):
        population = random.choices(population, weights=None, k=pop_size)

        if 'A' in population and 'B' in population:
            f_A = allele_freq('A', population)
            freq_A.append(f_A)
            f_B = allele_freq('B', population)
            freq_B.append(f_B)
        else:
            break

    return freq_A, freq_B

freq_A, freq_B = modelDrift_AB(100, 1000)

generations = range(0, len(freq_A))
plb.plot(generations, freq_A, 'r', label='Allele A')
plb.plot(generations, freq_B, 'b', label='Allele B')
plb.axis(xmin=1, xmax=len(generations), ymin=0, ymax=1.0)
plb.xlabel("Number of Generations")
plb.ylabel("Allele frequency")
plb.title("Change in frequency of alleles 'A' and 'B' over {} generations".format(len(generations)))
plb.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plb.show()


def modelDrift_A(pop_size, n_gens):
    """
    Model the genetic drift of alleles 'A' and 'a' in a population over n generations.
    Returns lists for the frequency of homozygotes (AA or aa) and heterozygotes (Aa) over n generations.

    @param:
        pop_size (int): Size of the population to be modeled.
        n_gens (int): Number of generations to model the population over.

    @return:
        tuple: Three lists containing the frequency of homozygotes (AA or aa) and heterozygotes (Aa) over n generations.
    """
    AA = ['AA' for i in range(int(pop_size/4))]
    Aa = ['Aa' for i in range(int(pop_size/2))]
    aa = ['aa' for i in range(int(pop_size/4))]
    
    initial_pop = AA + Aa + aa
    freq_AA = [allele_freq('AA', initial_pop)]
    freq_Aa = [allele_freq('Aa', initial_pop)]
    freq_aa = [allele_freq('aa', initial_pop)]

    for i in range(n_gens):
        new_pop = []

        for ind in range(pop_size):
            pair = random.choices(initial_pop, k=2)
            offspring = pair[0][random.randint(0, 1)] + pair[1][random.randint(0, 1)]
            if offspring == 'aA':
                offspring = 'Aa'
            new_pop.append(offspring)

        a_in_pop = 0
        for individual in new_pop:
            if individual == "Aa":
                a_in_pop += 1
            if individual == "aa":
                a_in_pop += 2

        if a_in_pop == 0:
            break

        n_dead = int(0.2 * new_pop.count('aa'))

        for count in range(n_dead):
            new_pop.remove('aa')
            new_individual = random.choices(['AA', 'Aa'], k=1)
            new_pop.append(*new_individual)

        f_AA = allele_freq('AA', new_pop)
        freq_AA.append(f_AA)
        f_Aa = allele_freq('Aa', new_pop)
        freq_Aa.append(f_Aa)
        f_aa = allele_freq('aa', new_pop)
        freq_aa.append(f_aa)

        initial_pop = new_pop

    return freq_AA, freq_Aa, freq_aa

freq_AA, freq_Aa, freq_aa = modelDrift_A(100, 500)

x_data = range(0, len(freq_AA))
plb.plot(x_data, freq_AA, 'r', label='AA')
plb.plot(x_data, freq_Aa, 'b', label='Aa')
plb.plot(x_data, freq_aa, 'k', label='aa')
plb.axis(xmin=1, xmax=len(freq_AA))
plb.xlabel("Number of Generations")
plb.ylabel("Allele frequency in the population")
plb.title("Change in frequency of alleles 'A' and 'a' over {} generations".format(len(x_data)))
plb.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plb.show()
