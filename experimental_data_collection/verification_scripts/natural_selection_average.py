#!/usr/bin/env python3
# coding: utf-8

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle, Polygon
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry.polygon import Polygon as ShapelyPolygon
import sys

#for testing
import time

"""
Parameters to be changed by user
"""

# list of "hot spots" 
#     Format: (x coordinate, y coordinate, multiplicity - number of users at that location)
map_density_list = np.array([(200,100,5), (250,250,10), (400,300,10), (200,500,10), (400,500,10), (200,600,5), 
(300,800,10), (600,200,15), (700,300,5), (600,300,10), (500,400,10), (800,500,10), (600,600,5), (800,800,10), 
(300,700,15), (700,400,15), (500,100,15), (700,700,5), (300,350,5), (100,100,15), (600,100,5)])

# Minimum coverage needed to be provided by the algorithm
#     Format: decimal (1 = 100% coverage)
min_coverage = 1

#Maximum number of users a single UAV can support at a time
max_users_per_drone = 250

#Parameters for the caclulation:
wavelength = 0.125
directivity_transmitter_dBi = 14
directivity_reciever_dBi = 5
power_transmitter_dBm = -10
power_reciever_dBm = -70
beamwidth = 60

"""
Nothing below this should be changed by the user
"""
choice = input("Use pre-existing values? (Y/N): ")
default = False
if (choice == 'Y' or choice == 'y'):
    default = True

if (not default):
    #Asks user for information and creates lists
    def make_list():
        temp_list = []
        user_input = "default"
        while (user_input != ['']):
            user_input = input("Enter Coordinates: ").split(",")
            if (user_input == ['']): break
            temp_coord = []
            for string in user_input:
                temp_coord.append(int(string))
            temp = tuple(temp_coord)
            temp_list.append(temp)
        return np.array(temp_list)

    # list of "hot spots" 
    #     Format: (x coordinate, y coordinate, multiplicity - number of users at that location)
    print("Enter user cluster locations in the format: x,y,# of users. \n When finished, leave blank and tap enter.")
    map_density_list = make_list()

    # Minimum coverage needed to be provided by the algorithm
    #     Format: decimal (1 = 100% coverage)
    print("Enter minimum coverage: the minimum percentage of users that must be covered by the network.")
    min_coverage = int(input("Enter minimum coverage percentage: "))/ 100.0

    #Maximum number of users a single UAV can support at a time
    print("Enter the maximum number of users that can be provided connectivity by a single UAV.")
    max_users_per_drone = int(input("Enter maximum number of users per UAV: "))

    #Parameters for the caclulation:
    print("Enter the following parameters about the network module.")
    wavelength = float(input("Enter wavelength (in meters): "))
    directivity_transmitter_dBi = float(input("Enter transmitter directivity (in dBi): "))
    directivity_reciever_dBi = float(input("Enter reciever directivity (in dBi): "))
    power_transmitter_dBm = float(input("Enter transmitter power (in dBm): "))
    power_reciever_dBm = float(input("Enter reciever power (in dBm): "))
    beamwidth = float(input("Enter beamwidth (in degrees): "))

# The functions below make it easier to understand what information is being retrieved later in the code 
#     Defines the value to use for max() to get third entity
def get_mult(ent):
    return ent[2]
#defines the value to use for max() to get second entity
def get_y(ent):
    return ent[1]
#defines the value to use for max() to get first entity
def get_x(ent):
    return ent[0]
#defines the value for the best score currently in a population
def get_best_score(ent):
    return ent[0]
#defines the value for the index at which the best drone layout is stored in population
def get_best_index(ent):
    return ent[1]

"""
GLOBAL VARIABLES
"""
#stores the popultation - global variable so it can be accessed inside and outside functions
population = []

#Stores the list of drones for output; empty until filled by the algorithm
drone_list = []

#stores the best score currently in the population and the index at which the layout with the best score is located
best_fitness = (0, -1)

#slightly different calculations are used if 100% coverage is needed - flag for later
total_coverage_check = False
if (min_coverage == 1):
    total_coverage_check = True

#number of drones in each member of the population, starts at 1 unless changed
num_drones = 1

#population size for GA
pop_size = 400

# Mutation rate for GA
#     Format: decimal (1 = 100% (complete randomness))
mutation_rate = 0.01

#split ensures sum of 2 sections = whole pop_size on odd numbers
inherit_between_runs = int(pop_size/2)
remainder_of_pop = pop_size - inherit_between_runs

#total number of users in the network (set by loop below)
tot_users = 0
for (_,_,u) in map_density_list:
    tot_users += u

#fitness to strive for with GA
optimal_fitness = tot_users * min_coverage

#calculates the minimum and maximum x and y values for the polygon
if (len(map_density_list) > 0):
    xmin = get_x(min(map_density_list, key=get_x))
    xmax = get_x(max(map_density_list, key=get_x))
    ymin = get_y(min(map_density_list, key=get_y))
    ymax = get_y(max(map_density_list, key=get_y))
else:
    print("No map to create: no users on map.")
    exit(0)


#Creates two polygon objects used for later calculations
#map_poly = Polygon(map_vertex_list, True)
map_vertex_list = np.array([(xmin,ymin), (xmin,ymax), (xmax,ymax), (xmax, ymin)])
shapely_poly = ShapelyPolygon(map_vertex_list)

print("~~~~Algorithm Calculation Beginning~~~~~")
print("Minimum Coverage:", str(min_coverage * 100) + "%")
print("Total users in this map:", str(tot_users))

"""
The section below calculates the height and coverage radius of the network module on the drone
"""
#convert angle in degrees to radians
theta = beamwidth*(np.pi/180)

#calculations
height = wavelength / (4 * np.pi * 10**((power_reciever_dBm - 
                                         (power_transmitter_dBm + directivity_transmitter_dBi + 
                                          directivity_reciever_dBi))/20))
coverage_radius = int(height * np.tan(theta))
height = int(height)

print("Height:", str(height), "meters")
print("Coverage Radius:", str(coverage_radius), "meters")


# checks if a point is within the map polygon
#     returns boolean: true or false

def polygon_contains_point(point):
    point_to_check = ShapelyPoint(get_x(point), get_y(point))
    return shapely_poly.contains(point_to_check)

#draws appropriate map - make more flexible with different polygons
def draw_map(map_density_list, drone_list):
    
    patches = []
    
    max_mult = get_mult(max(map_density_list, key=get_mult))
    #handle drone selection circles
    for coord in drone_list:

        temp_circle = Circle(coord, radius=coverage_radius)
        patches.append(temp_circle)

    fig, ax = plt.subplots()
    p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
    ax.add_collection(p)

    for coord in drone_list:
        plt.scatter(get_x(coord),get_y(coord),c='b')
    
    for (x, y, m) in map_density_list:
        if (m/max_mult <= 1/3):
            plt.scatter(x, y, c='g')
        elif (m/max_mult <= 2/3):
            plt.scatter(x, y, c='y')
        else:
            plt.scatter(x, y, c='r')    
            
    plt.axis([xmin-10,xmax+10,ymin-10,ymax+10])
    plt.axis('scaled')
    plt.show()
    
"""
GA SETUP
"""
#fills population with pop_size random but appropriate entries
for _ in range(pop_size):
    temp_pop = []
    for _ in range(num_drones):
        if (xmax == xmin and ymin == ymax):
            add_to_pop = (xmin,ymin)
        elif (xmax == xmin):
            add_to_pop = (xmin, np.random.randint(ymin,ymax))
            while (not polygon_contains_point(add_to_pop)):
                add_to_pop = (xmin, np.random.randint(ymin,ymax))
        elif (ymax == ymin):
            add_to_pop = (np.random.randint(xmin, xmax), ymin)
            while (not polygon_contains_point(add_to_pop)):
                add_to_pop = (np.random.randint(xmin, xmax), ymin)
        else: 
            add_to_pop = (np.random.randint(xmin, xmax), np.random.randint(ymin,ymax))
            while (not polygon_contains_point(add_to_pop)):
                add_to_pop = (np.random.randint(xmin, xmax), np.random.randint(ymin,ymax))
        temp_pop.append(add_to_pop)

    population.append(temp_pop)

def setup_intermediate():
    global population, drone_list, best_fitness, inherit_between_runs, remainder_of_pop
    add_to_pop = population[get_best_index(best_fitness)]
    population = []
    
    drone_list = []
    best_fitness = (0, -1)
    
    #fill some of the population with the winning entry from before
    for _ in range(inherit_between_runs):
        if (xmax == xmin and ymax == ymin):
            append = (xmin, ymin)
        elif (xmax == xmin):
            append = (xmin, np.random.randint(ymin,ymax))
            while (not polygon_contains_point(add_to_pop)):
                append = (xmin, np.random.randint(ymin,ymax))
        elif (ymax == ymin):
            append = (np.random.randint(xmin, xmax), ymin)
            while (not polygon_contains_point(add_to_pop)):
                append = (np.random.randint(xmin, xmax), ymin)
        else:
            append = (np.random.randint(xmin, xmax), np.random.randint(ymin,ymax))
            while (not polygon_contains_point(append)):
                append = (np.random.randint(xmin, xmax), np.random.randint(ymin,ymax))
        temp = add_to_pop.copy()
        temp.append(append)
        population.append(temp)
    
    #fills remainder of the population with random but appropriate entries
    for _ in range(remainder_of_pop):
        temp_pop = []
        for _ in range(num_drones):
            add_to_pop = (np.random.randint(xmin, xmax), np.random.randint(ymin,ymax))
            while (not polygon_contains_point(add_to_pop)):
                add_to_pop = (np.random.randint(xmin, xmax), np.random.randint(ymin,ymax))
            temp_pop.append(add_to_pop)
        population.append(temp_pop)
    np.random.shuffle(population)

"""
 GA functions
"""

# create new data structure with the number of entries equivalent to the fitness
#     fitness is defined as the number of users covered under a given map
def fitness():
    global best_fitness, population
    adj_population = []
    index = -1
    for proposed_map in population:
        score = 0
        cluster_exclusion_list = []
        for drone in proposed_map:
            users_per_drone = 0
            for (x, y, m) in map_density_list:
                hot_spot = (x, y, m)
                dist = np.sqrt((get_x(hot_spot)-get_x(drone))**2 + (get_y(hot_spot)-get_y(drone))**2)
                if ((dist <= coverage_radius) and (hot_spot not in cluster_exclusion_list)):
                    if (users_per_drone + get_mult(hot_spot) <= max_users_per_drone):
                        if (total_coverage_check):
                            adj_population.append(proposed_map)
                        else:
                            for _ in range(get_mult(hot_spot)):
                                adj_population.append(proposed_map)
                        cluster_exclusion_list.append(hot_spot)
                        score += get_mult(hot_spot)
                        users_per_drone += get_mult(hot_spot)
                    
        index += 1
        if (score >= get_best_score(best_fitness)):
            best_fitness = (score, index)
    return adj_population

# Computes the next generation for the GA
#     also handles mutation
def draw(adj_population):
    global population
    population = []
    mutation_check = 0
    for _ in range(pop_size):
        add_to_pop = []
        for m in range(num_drones):
            rand1 = np.random.randint(0, len(adj_population))
            rand2 = np.random.randint(0, len(adj_population))
            if (mutation_check == 1/mutation_rate):
                sys.stdout.write('~')
                sys.stdout.flush()
                mut_rand = np.random.randint(0,2)
                if (mut_rand == 0):
                    add_to_pop.append((np.random.randint(xmin, xmax), get_y(adj_population[rand2][m])))
                else:
                    add_to_pop.append((get_x(adj_population[rand1][m]), np.random.randint(ymin, ymax)))
                mutation_check = 0
            else:
                x_avg = (get_x(adj_population[rand1][m]) + get_x(adj_population[rand2][m]))/2
                y_avg = (get_y(adj_population[rand1][m]) + get_y(adj_population[rand2][m]))/2
                add_to_pop.append((x_avg, y_avg))
        
        mutation_check += 1
        population.append(add_to_pop)
        
#graphically displays final result
def illustrate_final():
    global drone_list, population, best_fitness
    drone_list = population[get_best_index(best_fitness)]
    list_ = [list(elem) for elem in population[get_best_index(best_fitness)]]
    for tup in list_:
        tup.append(height)
    print("\nBest fitness: " + str(get_best_score(best_fitness)) + " \nProposed Map: ")

    for tup in list_:
        print("(" + str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + ")")
    #illustrate solution
    draw_map(map_density_list, drone_list)

#displays intermediate results (failures)
def illustrate_intermediate():
    global best_fitness, num_drones
    if (num_drones == 1):
        print("\n" + str(num_drones), "drone failed | Best fitness:", str(get_best_score(best_fitness)/optimal_fitness * 100), '%',
              "\n\nContinuing with", str(num_drones+1), "drones")
    else:
        print("\n" + str(num_drones), "drones failed | Best fitness:", str(get_best_score(best_fitness)/optimal_fitness * 100), '%',
              "\n\nContinuing with", str(num_drones+1), "drones")

"""
Control loop for GA
"""
# optimize: instead of max iterations, use for how many generations the fitness stays the same 
#     if score stays the same for 50 iterations, move on

#for testing
start_time = time.time()

intermediate = False

while(get_best_score(best_fitness) < optimal_fitness):
    if (intermediate):
        setup_intermediate()
    same_fitness_count = 0
    fit = fitness()
    #makes calculation time a function of these 2 variables
    #allows for more iterations for harder solutions
    calc_limit = int(num_drones * len(map_density_list) /2)
    while(get_best_score(best_fitness) < optimal_fitness and same_fitness_count < calc_limit):
        prev_fitness = get_best_score(best_fitness)
        draw(fit)
        fit = fitness()
        if (get_best_score(best_fitness) == prev_fitness):
            same_fitness_count += 1
        else:
            same_fitness_score = 0
    if (get_best_score(best_fitness) < optimal_fitness):
        illustrate_intermediate()
    num_drones += 1
    intermediate = True

#for testing
print('\nThe algorithm took', time.time()-start_time, 'seconds.')
illustrate_final()