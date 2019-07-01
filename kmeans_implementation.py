from sklearn.cluster import KMeans
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle, Polygon
import sys

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

map_vertex_list = np.array([(0,0), (250, 1000), (500, 750), (1000,1000), (750, 0)])
xmin = get_x(min(map_vertex_list, key=get_x))
xmax = get_x(max(map_vertex_list, key=get_x))
ymin = get_y(min(map_vertex_list, key=get_y))
ymax = get_y(max(map_vertex_list, key=get_y))

map_density_list = np.array([(200,100,5), (250,250,10), (400,300,10), (200,500,10), (400,500,10), (200,600,5), 
(300,800,10), (600,200,15), (700,300,5), (600,300,10), (500,400,10), (800,500,10), (600,600,5), (800,800,10), 
(300,700,15), (700,400,15), (500,100,15), (700,700,5), (300,350,5), (100,100,15), (600,100,5)])

map_poly = Polygon(map_vertex_list, True)

coverage_radius = 153

def draw_map(map_vertex_list, map_density_list, drone_list):
    
    patches = [map_poly]
    
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



X = np.array([(200,100), (250,250), (400,300), (200,500), (400,500), (200,600), 
(300,800), (600,200), (700,300), (600,300), (500,400), (800,500), (600,600), (800,800), 
(300,700), (700,400), (500,100), (700,700), (300,350), (100,100), (600,100)])

kmeans = KMeans(n_clusters=7)
kmeans.fit(X)

for cluster in map_density_list:
    mini = 50000
    for center in kmeans.cluster_centers_:
        dist = np.sqrt((get_x(center)-get_x(cluster))**2 + (get_y(center)-get_y(cluster))**2)
        if (dist < mini):
            mini = dist
    if (mini > coverage_radius):
        sys.exit()


#print(kmeans.cluster_centers_)
#draw_map(map_vertex_list, map_density_list, kmeans.cluster_centers_)
print("success")