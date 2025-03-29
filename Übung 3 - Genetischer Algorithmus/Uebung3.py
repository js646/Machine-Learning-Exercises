#Autor: Julian Schlee 1821112
import random
import math
import copy

volumina = []
population = []   # [50][100]

for i in range(100):
    volumina.append(random.uniform(1, 10))

for i in range(50):
    temp = []
    for j in range(100):
        temp.append(random.getrandbits(1))
    population.append(temp)


def fitness(gene):
    summe = 0
    c = 0.0003
    for i in range(len(gene)):
        summe += gene[i] * volumina[i]
    return math.exp(-c * pow((100 - summe), 2))


def volumen(gene):
    summe = 0
    for i in range(len(gene)):
        summe += gene[i] * volumina[i]
    return summe


def total_fitness(pop):
    sum = 0
    for i in range(len(pop)):
        sum += fitness(pop[i])
    return sum


def total_volumen(pop):
    sum = 0
    for i in range(len(pop)):
        sum += volumen(pop[i])
    return sum


def best_fitness(pop):
    max = 0
    for gene in pop:
        if fitness(gene) > max:
            max = fitness(gene)
    return max


def best_volumen(pop):
    min = volumen(pop[0])
    for gene in pop:
        if abs(volumen(gene) - 100) < abs(min - 100):
            min = volumen(gene)
    return min


def select_hypothesis(pop):
    rand = random.random()
    summe = 0
    index = random.randint(0, len(pop))
    while summe < rand:
        index += 1
        index = index % len(pop)
        summe += (fitness(pop[index]) / total_fitness(pop))
    return index


def crossover(parent1, parent2):
    children = []
    child1 = [0] * len(parent1)
    child2 = [0] * len(parent1)
    rand = random.randint(0, len(parent1) -1)

    for i in range(len(parent1)):
        if i <= rand:
            child1[i] = parent1[i]
        else:
            child2[i] = parent1[i]

    for i in range(len(parent1)):
        if i > rand:
            child1[i] = parent2[i]
        else:
            child2[i] = parent2[i]

    children.append(child1)
    children.append(child2)
    return children


def print_pop_info(pop):
    print("--------------------------------------------------------")
    for i, g in enumerate(pop):
        print("Gene " + str(i) + ": Fitness:" + str(fitness(g)) + " Volumen:" + str(volumen(g)))
    print("--------------------------------------------------------")
    print("average fitness: " + str(total_fitness(population) / len(population)))
    print("average volume: " + str(total_volumen(population) / len(population)))
    print("best fitness: " + str(best_fitness(population)))
    print("best volume: " + str(best_volumen(population)))
    print("--------------------------------------------------------")


# Algorithmus
p = len(population) #Populationsgröße
r = 0.6  #Crossoveranteil
m = 0.04  #Mutationsanteil
generations = 0
print_pop_info(population)

while generations < 50:
    # Selektion
    new_gen = []
    while len(new_gen) < ((1 - r) * p):
        new_gen.append(population[select_hypothesis(population)])

    # Crossover
    parents = []
    while len(parents) < (r * p):
        parents.append(population[select_hypothesis(population)])

    for i, par in enumerate(parents):
        if i % 2 == 0:
            continue
        children = crossover(parents[i-1], parents[i])
        new_gen.append(children[0])
        new_gen.append(children[1])

    # Mutation
    mutated_bits = 0
    while mutated_bits < (m * p):
        rand1 = random.randint(0, len(new_gen) - 1)
        rand2 = random.randint(0, len(new_gen[0]) - 1)
        new_gen[rand1][rand2] = abs(new_gen[rand1][rand2] - 1)
        mutated_bits += 1

    population = copy.deepcopy(new_gen)
    generations += 1
    print("Generation: " + str(generations) + ", average fitness: " + str(total_fitness(population) / len(population))
                                            + ", average volume: " + str(total_volumen(population) / len(population)) )

print_pop_info(population)
