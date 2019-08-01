from sklearn.cluster import KMeans
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle, Polygon
import sys
import time

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


# list of "hot spots" 
#     Format: (x coordinate, y coordinate, multiplicity - number of users at that location)
#     Format: (x coordinate, y coordinate, multiplicity - number of users at that location)
map_density_list = np.array([(773,585,5),(581,207,10),(738,685,5), (844,236,10),(1610,457,15),(1800,15,10),(992,153,5),
(1593,975,10),(1195,948,5),(1868,301,10),(1944,158,10),(1169,793,10),(287,8,5),(1429,56,15)])

# List of vertices in the polygon (in order of drawing)
#     Also calculates the minimum and maximum x and y values for the polygon
xmin = get_x(min(map_density_list, key=get_x))
xmax = get_x(max(map_density_list, key=get_x))
ymin = get_y(min(map_density_list, key=get_y))
ymax = get_y(max(map_density_list, key=get_y))


#Creates a polygon object used for later calculations
#map_poly = Polygon(map_vertex_list, True)

"""
The section below calculates the height and coverage radius of the network module on the drone
"""
#Parameters for the caclulation:
wavelength = 0.125
directivity_transmitter_dBi = 14
directivity_reciever_dBi = 5
power_transmitter_dBm = -10
power_reciever_dBm = -70
aperature_angle = 60

#convert angle in degrees to radians
theta = aperature_angle*(np.pi/180)

#calculations
height = wavelength / (4 * np.pi * 10**((power_reciever_dBm - 
                                         (power_transmitter_dBm + directivity_transmitter_dBi + 
                                          directivity_reciever_dBi))/20))
coverage_radius = int(height * np.tan(theta))
height = int(height)

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

start_time = time.time()
#remakes map_density_list without densities
map_list = []
for item in map_density_list:
    map_list.append(item[0:2])

#performs clustering
kmeans = KMeans(n_clusters=9)
kmeans.fit(map_list)

#checks if *any* user is outside all coverage 
for cluster in map_density_list:
    mini = 50000
    for center in kmeans.cluster_centers_:
        dist = np.sqrt((get_x(center)-get_x(cluster))**2 + (get_y(center)-get_y(cluster))**2)
        if (dist < mini):
            mini = dist
    if (mini > coverage_radius):
        print("FAILFAILFAILFAIFLAIFLALILFAIFAILFAILFAILFAILFAIL")
        sys.exit()

#Display options
#print(kmeans.cluster_centers_)
print('\nThe algorithm took', time.time()-start_time, 'seconds.')
draw_map(map_density_list, kmeans.cluster_centers_)
print("success")