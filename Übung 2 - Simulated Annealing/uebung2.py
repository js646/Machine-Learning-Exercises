#Autor: Julian Schlee, Matrikelnummer: 1821112
import numpy
import random
import copy
import math


class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


# Liste aus n Städten erstellen
def create_cities(n):
    new_cities = []
    for i in range(0, n):
        new_cities.append(City(str(i), random.randint(1, 500), random.randint(1, 500)))
    return new_cities


# Distanz zwischen 2 Städten
def get_distance(city1, city2):
    return numpy.sqrt(numpy.abs(city1.x - city2.x) + numpy.abs(city1.y - city2.y))


# Distanz-Tabelle ausgeben
def print_distance_table(city_arr):
    print("Distance-Table:")
    for i in range(0, len(city_arr)+1):
        end = "__|" if i < 10 else "_|"
        print("|___", end="__|") if i == 0 else print("__"+str(i), end=end)
    print("")

    for j in range(0, len(city_arr)):
        start = "|__" if j+1 < 10 else "|_"
        print(start+str(j+1), end="__|")
        for k in range(0, len(city_arr)):
            print(" "+str(round(get_distance(city_arr[j], city_arr[k]), 1)), end=" |")
        print("")


# Zufällige Route aus n Städten generieren
def create_route(cities):
    new_route = []
    for i in range(0, len(cities)-1):
        new_route.append(cities[i])
    random.shuffle(new_route)
    return new_route


# Gesamtdistanz der Rundreise
def get_total_distance(route):
    distance = 0

    for first, second in zip(route[:-1], route[1:]):
        distance += get_distance(first, second)

    distance += get_distance(route[0], route[-1])
    return distance


# Vertauschungsfunktion
def swap_random_cities(route):
    city_to_swap1 = random.randint(0, len(route)-1)
    city_to_swap2 = random.randint(0, len(route)-1)
    tmp = route[city_to_swap1]
    route[city_to_swap1] = route[city_to_swap2]
    route[city_to_swap2] = tmp
    return route


# Optimierungsalgorithmus (Simulated Annealing)
def optimize(route):
    temperature = 180
    last_fitness = -get_total_distance(route)
    epsilon = 0.008
    while temperature > epsilon:
        old_route = copy.deepcopy(route)
        swap_random_cities(route)
        new_fitness = -get_total_distance(route)
        probability = math.exp((new_fitness - last_fitness) / temperature)
        rand = random.uniform(0, 1)
        if new_fitness > last_fitness:
            last_fitness = new_fitness
        else:
            print(probability)
            if rand < probability:
                print("Accepted Backstep: Probability:" +str(probability)+" Random:"+str(rand)+" Delta: "+str(new_fitness - last_fitness))
                last_fitness = new_fitness
            else:
                print("Rejected Backstep: Probability:" +str(probability)+" Random:"+str(rand)+ "Delta: "+str(new_fitness - last_fitness))
                route = old_route
        temperature = temperature - epsilon

    return route


def main():
    cities = create_cities(100)
    route = create_route(cities)
    #print_distance_table(cities)
    print("")

    print("Starting with route: "+str(route))
    print("Initial route distance: "+str(get_total_distance(route)))
    print("_____________________________________")

    final_route = optimize(route)

    print("_____________________________________")
    print("Initial route: "+str(route))
    print("Final route: "+str(final_route))
    print("")
    print("Initial route distance: "+str(get_total_distance(route)))
    print("Final route distance: "+str(get_total_distance(final_route)))

main()