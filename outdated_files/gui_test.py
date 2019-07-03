import numpy as np

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

print("Enter user cluster locations in the format: x,y,# of users. \n When finished, leave blank and tap enter.")
map_density_list = make_list()

print("Enter vertices for the search polygon *in order of connection* in the format: x,y. \n When finished, leave blank and tap enter.")
map_vertex_list = make_list()

print("Enter minimum coverage: the minimum percentage of users that must be covered by the network.")
min_coverage = int(input("Enter minimum coverage percentage: "))/ 100.0

print("Enter the maximum number of users that can be provided connectivity by a single UAV.")
max_users_per_drone = int(input("Enter maximum number of users per UAV: "))

print(str(map_density_list), "\n\n", str(map_vertex_list), "\n\n", str(min_coverage), "\n\n", str(max_users_per_drone))