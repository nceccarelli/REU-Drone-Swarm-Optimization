# Drone Swarm Optimizer

## Overview

Efficient arrangement of UAVs in a swarm formation is essential to the functioning of such a swarm as a temporary communication network. Such a network could assist in search-and-rescue efforts by providing first responders with a means of communication. We propose a solution to creating a user-friendly and effective system for calculating and visualizing an optimal layout of UAVs to cover a minimum percentage of overall users in a given area. The calculation is computed by a genetic algorithm while the visualization outputs the results of the calculation in an easy-to-comprehend manner. An initial calculation to gather parameter information is followed by the algorithm that generates the optimal solution. This algorithm is run iteratively until a solution is found. Information is passed between iterations to reduce runtime and complexity.

An example of a UAV that this algorithm can be run for: 
![Alt text](picture_data/drone_from_side?raw=true "Example UAV")

This algorithm will output a visual such as this:
![Alt text](picture_data/ex_soln.png?raw=true "Example Solution")

In this picture, users are representad as green, yellow, and red dots, in order of increasing density. Blue dots represent UAVs with the lighter blue circles around each UAV being the coverage they can provide. The large polygon is the specified coveage polygon.

This project has been tested using Python 3.7 on Mac OS X Version 10.14.5 and Ubuntu 18.04.

**Author:** Nicholas Ceccarelli, njceccarelli@gmail.com  
**Affiliation:** SUNY University at Buffalo, *Student*; University of Nevada, Reno, *REU Participant*
<!-- add pictures and explain how it works -->

## Installation

### Dependencies

* Python 3.7
* matplotlib
* numpy
* shapely

### Building

From here on out, "DIR" will represent the directory in which it is desired for the package to be installed.

To download the software, run the following in a terminal window:  

```python
cd DIR  
git clone https://github.com/nceccarelli/REU_Drone_Swarm_Optimization.git  
cd REU_Drone_Swarm_Optimization
```

Now the software should be downloaded and opened in the terminal window.

### Setup

Before use, calculation parameters likely need to be changed. This can be done from within the Python script entitled *Drone_Swarm_Optimizer.py*. To do this, open the file in your favorite IDE or open with vim by running the following in the previous terminal window:

`vim Drone_Swarm_Optimizer.py`

If vim has not been installed previously, run the following:  

**On Linux:**  
`sudo apt install vim`  
**On Mac**  
`brew install vim`  

The following parameters pertaining to the overall algorithm may be changed:

* min_coverage
* map_density_list
* map_vertex_list
* max_users_per_drone

The following table defines the above parameters:

| Parameter | Definition |
|-----------|------------|
| min_coverage | The minimum fraction of users that must be provided network coverage. Reported in the form of a decimal. |
| map_density_list | The map density list - A list of all user clusters in the form of (x, y, number of users). |
| map_vertex_list | The coordinates of the vertices of the outside of the surrounding polygon in the form of (x,y). |
| max_users_per_drone | The maximum number of users that can be provided coverage by a single UAV. |

The following parameters pertaining to network calculations may be changed:

* wavelength
* directivity_transmitter_dBi
* directivity_reciever_dBi
* power_transmitter_dBm
* power_reciever_dBm
* aperature_angle

The above parameters are specific to the network modules specifications.

Wavelength is represented in meters, directivities are represented in dBi, powers are represented in dBm, and aperature angle is represented in degrees.

All other global variables should not be changed.

### Execution

Once all appropriate parameters are changed, the algorithm can be run. To do so, in the previously described terminal window, run the following:

`python3 Drone_Swarm_Optimizer.py`

After this line is run, the terminal window will display the progress of the algorithm. Once finished, the script will print coordinates of UAV locations, and an external window will open with a visualization of the UAVs and users in map_density_list within the polygon depicted by map_vertex_list.
