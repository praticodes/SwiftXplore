"""
This is a Python program to calculate the shortest possible path between different 'attractions'
in Toronto. It's aimed at first-year students at the University of Toronto who want to explore the
city during reading week safely, efficiently, and at low cost.
"""
import random
from sympy.combinatorics.partitions import Partition
from sympy.combinatorics.permutations import Permutation
from itertools import permutations
from pathlib import Path
import csv

"""////////////////////////////////////////////////////////////////////////////////////////////////
----------------- INITIALIZATION --------------------------------------------------------
///////////////////////////////////////////////////////////////////////////////////////////////////"""

attraction1 = "Royal Ontario Museum"
attraction2 = "Chatime Bubble Team"
attraction3 = "Scream Ice Cream"
attraction4 = "Tim Hortons"
attraction5 = "Royal Conservatory of Music"
attraction6 = "Aloette"
attraction7 = "Raku"
attraction8 = "Ozzy's Burgers"
attraction9 = "CN Tower"
attraction10 = "Dipped Donuts"
attraction11 = "St Lawrence Market"
attraction12 = "Kensington Market"
attraction13 = "High Park"
attraction14 = "Toronto Botanical Garden"
attraction15 = "Trinity Bellwoods Park"
attraction16 = "Centreville Amusement Park"
attraction17 = "Canada's Wonderland"

longitudes_and_latitudes = {attraction1: (43.66792698034359, -79.39479856014943),
                            attraction2: (43.66768747839565, -79.40077663127906),
                            attraction3: (43.67046051072736, -79.39213486014933),
                            attraction4: (43.668983327418715, -79.39768642299356),
                            attraction5: (43.668204400813615, -79.39632440247868)
                            }

cities = {attraction1: "Toronto",
          attraction2: "Toronto",
          attraction3: "Toronto",
          attraction4: "Toronto",
          attraction5: "Toronto",
          attraction6: "Toronto",
          attraction7: "Toronto",
          attraction8: "Toronto",
          attraction9: "Toronto",
          attraction10: "Toronto",
          attraction11: "Toronto",
          attraction12: "Toronto",
          attraction13: "Toronto",
          attraction14: "Toronto",
          attraction15: "Toronto",
          attraction16: "Toronto",
          attraction17: "Toronto"}

csi_scores_metropolitan_ontario = {"Toronto": 45.45,
                                   "Barrie": 45.91,
                                   "Ottawa-Gatineau": 49.23,
                                   "Hamilton": 56.85,
                                   "Guelph": 58.22,
                                   "St.Catherines-Niagra": 62.12,
                                   "Peterborough": 64.8,
                                   "Belleville": 69.33,
                                   "Kingston": 72.78,
                                   "Windsor": 74.84,
                                   "Brantford": 75.71,
                                   "Kitchner-Cambridge-Waterloo": 79.39,
                                   "London": 80.09,
                                   "Greater Sudbury": 84.39,
                                   "Thunder Bay": 101.31}

selected_attractions = [attraction1, attraction2, attraction3, attraction4, attraction5]


def get_distance_between_points(location1: tuple[float, float], location2: tuple[float, float]) -> float:
    """
    Takes in the coordinates of two points (x1, y1) and (x2, y2). Returns the distance
    between them as per the distance formula.
    """
    distance = ((location1[0] - location2[0]) ** 2 + (location1[1] - location2[1]) ** 2) ** 0.5
    return distance


def get_longitude_latitude(chosen_attractions: list[str]) -> list[tuple]:
    """Take in a list of attractions (a list of strings) and return a list of longitude
    and latitude coordinates (a list of tuples)
    """
    list_of_longitudes_latitudes = [longitudes_and_latitudes[i] for i in chosen_attractions]
    return list_of_longitudes_latitudes


def get_cities_in_route(chosen_attractions: list[str]) -> list[str]:
    """ Returns the list of cities in a route, duplicates allowed.
    """
    cities_in_route = [cities[i] for i in chosen_attractions]

    return cities_in_route


def get_csi_average(chosen_attractions: list[str]) -> float:
    """ Returns the average safety across all cities in a route. If a city appears multiple times,
    it will influence the average more.
    """
    csi_scores = []

    for city in get_cities_in_route(chosen_attractions):
        csi_scores.append(csi_scores_metropolitan_ontario[city])

    average = sum(csi_scores) / len(csi_scores)

    return average


def get_safety_score(route: list[str]) -> float:
    """Calculates the safety of each route. The safest route is the one where the most dangerous places
    are visited earlier on in the day.
    """
    disorder = 0

    for i in range(0, len(route)):
        for j in range(i + 1, len(route)):
            if csi_scores_metropolitan_ontario[cities[route[i]]] < csi_scores_metropolitan_ontario[cities[route[j]]]:
                disorder += 1

    if disorder == 0:
        safety_score = len(route) + 1
    else:
        safety_score = len(route) / disorder

    return safety_score


def get_distance_score(route: list[str]) -> float:
    """ The routes which require travelling the least should have the highest distance scores.
    Each distance score is calculated as the quotient of the total number of cities
    and the length of the route.
    """
    route_coordinates = get_longitude_latitude(route)
    total_distance = 0

    for i in range(0, len(route_coordinates) - 1):
        total_distance += get_distance_between_points(route_coordinates[i], route_coordinates[i + 1])

    return len(route) / total_distance


def get_fitness_score(route: list[str]) -> float:
    """
    Returns the fitness score of a route.

    Fitness score is 90% dependent on distance score and 10% on safety.

    Since efficient travel can prevent excessive time on the road and related risks, and since
    it can also prevent ending up travelling late at night, distance score will carry a higher weight
    than safety score when calculating fitness.
    """

    fitness_score = get_distance_score(route) * 0.9 + get_safety_score(route) * 0.1

    return fitness_score


def create_routes(chosen_attractions: list[str]) -> list[list[str]]:
    """Creates the initial population of routes randomly by simply permuting the list of selected
    attractions.
    """
    routes = []
    for _ in range(0, population_size):
        routes.append(random.sample(chosen_attractions, len(chosen_attractions)))

    return routes


population_size = 50

"""////////////////////////////////////////////////////////////////////////////////////////////////
----------------- SELECTION --------------------------------------------------------
///////////////////////////////////////////////////////////////////////////////////////////////////"""


def roulette_wheel_selection(routes: list[list[str]]) -> list[list[str]]:
    """ We will use roulette wheel selection to create our mating pool.
    This means we will select a new population of routes. Each routes probability of selection
    will be proportional to its fitness.
    """

    aggregate_fitness = sum([get_fitness_score(route) for route in routes])
    selection_probabilities = [get_fitness_score(route) / aggregate_fitness for route in routes]

    selected = random.choices(routes, weights=selection_probabilities, k=(population_size // 2))

    return selected


"""////////////////////////////////////////////////////////////////////////////////////////////////
----------------- CROSSOVER --------------------------------------------------------
///////////////////////////////////////////////////////////////////////////////////////////////////"""


def partially_mapped_crossover(route1: list[str], route2: list[str]) -> list[str]:
    """Use partially mapped crossover to return an offspring
    """

    cross1 = random.randint(0, len(route1))
    cross2 = random.randint(cross1, len(route1))

    child = route1

    for i in range(0, len(route1)):
        for j in range(0, len(route1)):
            if i < cross1 or i > cross2:
                if route2[j] not in child:
                    child[i] = route2[j]

        return child


def repeat_crossover(routes: list[list[str]]) -> list[list[str]]:
    """ Repeat crossover multiple times with each element and another random element. Do
    this until we have 50 offspring.
    """

    routes = create_routes(selected_attractions)
    offsprings = []

    for route1 in routes:
        while len(offsprings) < population_size:
            offsprings.append(partially_mapped_crossover(route1, routes[random.randint(0, len(routes) - 1)]))

    return offsprings


"""////////////////////////////////////////////////////////////////////////////////////////////////
----------------- GENETIC ALGORITHM --------------------------------------------------------
///////////////////////////////////////////////////////////////////////////////////////////////////"""


def genetic_algorithm() -> list[str]:
    """Put everything together into one genetic algorithm that goes through 1000 evolutions.
    """
    population = create_routes(selected_attractions)

    for integer in range(0, 1000):
        selected_routes = roulette_wheel_selection(population)
        population = repeat_crossover(selected_routes)

    optimum = selected_attractions

    for k in (0, len(population) - 1):
        if get_fitness_score(population[k]) > get_fitness_score(optimum):
            optimum = population[k]

    return optimum


if __name__ == '__main__':
    data = genetic_algorithm()
    print(data)

with open("csv_algo.csv", "w") as f:
    writer = csv.writer(f)
    f.write("[")
    for data_piece in data:
        f.write(data_piece)
        f.write(", ")
    f.write("]")
