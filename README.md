<h1>Drone Swarm Optimizer </h1>

<h2>Overview</h2>

Efficient arrangement of UAVs in a swarm formation is essential to the functioning of such a swarm as a temporary communication network. Such a network could assist in search-and-rescue efforts by providing first responders with a means of communication. We propose a solution to creating a user-friendly and effective system for calculating and visualizing an optimal layout of UAVs to cover a minimum percentage of overall users in a given area. The calculation is computed by a genetic algorithm while the visualization outputs the results of the calculation in an easy-to-comprehend manner. An initial calculation to gather parameter information is followed by the algorithm that generates the optimal solution. This algorithm is run iteratively until a solution is found. Information is passed between iterations to reduce runtime and complexity.

<table style="width:100%;">
    <tr>
        <th>An example of a UAV for which this algorithm can be run:</th>
        <th>This algorithm will output a visual such as:</th>
    </tr>
    <tr>
        <th><img src="picture_data/drone_from_side.jpg" alt="Example UAV" width="500"/></th>
        <th><img src="picture_data/ex_soln.png" alt="Example Solution"/></th>
    </tr>
</table>

In the picture on the left, users are representad as green, yellow, and red dots, in order of increasing density. Blue dots represent UAVs with the lighter blue circles around each UAV being the coverage they can provide. The large polygon is the specified coveage polygon.

This project has been tested using Python 3.7 on Mac OS X Version 10.14.5 and Ubuntu 18.04.

<b>Author:</b> Nicholas Ceccarelli, njceccarelli@gmail.com  
<b>Affiliation:</b> SUNY University at Buffalo: *Student*; University of Nevada, Reno: *REU Participant*

<h2>Installation</h2>

<h3>Dependencies</h3>

<ul>
    <li>Python 3.7</li>
    <li>matplotlib</li>
    <li>numpy</li>
    <li>shapely</li>
</ul>

To install Python, run the following command:

<b>On Linux:</b>

```bash
sudo apt install python3
```

<b>On Mac:</b>

```bash
brew install python3
```

To install the other dependencies, run the command:

```bash
pip3 install matplotlib numpy shapely
```

<h3>Building</h3>

From here on out, "DIR" will represent the path to the directory in which it is desired for the package to be installed, for example "Desktop" or "Desktop/Github_packages".

To download the software, run the following in a terminal window:  

```bash
cd DIR  
git clone https://github.com/nceccarelli/REU_Drone_Swarm_Optimization.git  
cd REU_Drone_Swarm_Optimization
```

Now the software should be downloaded and opened in the terminal window.

<h3>Setup</h3>

Before use, calculation parameters likely need to be changed. This can be done from within the Python script entitled *Drone_Swarm_Optimizer.py*. To do this, open the file in your favorite IDE or open with nano by running the following in the previous terminal window:

```bash
nano Drone_Swarm_Optimizer.py
```

The following parameters pertaining to the overall algorithm may be changed:

<ul>
    <li>min_coverage</li>
    <li>map_density_list</li>
    <li>map_vertex_list</li>
    <li>max_users_per_drone</li>
</ul>

The following table defines the above parameters:

<table style="width:100%;">
    <tr>
        <th>Parameter</th>
        <th>Definition</th>
    </tr>
    <tr>
        <td>min_coverage</td>
        <td>The minimum fraction of users that must be provided network coverage. Reported in the form of a decimal.</td>
    </tr>
    <tr>
        <td>map_density_list</td>
        <td>The map density list - A list of all user clusters in the form of (x, y, number of users).</td>
    </tr>
    <tr>
        <td>map_vertex_list</td>
        <td>The coordinates of the vertices of the outside of the surrounding polygon in the form of (x,y).</td>
    </tr>
    <tr>
        <td>max_users_per_drone</td>
        <td>The maximum number of users that can be provided coverage by a single UAV.</td>
    </tr>
</table>

The following parameters pertaining to network calculations may be changed:

<ul>
    <li>wavelength</li>
    <li>directivity_transmitter_dBi</li>
    <li>directivity_reciever_dBi</li>
    <li>power_transmitter_dBm</li>
    <li>power_reciever_dBm</li>
    <li>aperature_angle</li>
</ul>

The above parameters are specific to the network modules specifications.

Wavelength is represented in meters, directivities are represented in dBi, powers are represented in dBm, and aperature angle is represented in degrees.

<b><i>All other global variables should not be changed.</b></i>

<h3>Execution</h3>

Once all appropriate parameters are changed, the algorithm can be run. To do so, in the previously described terminal window, run the following:

```bash
python3 Drone_Swarm_Optimizer.py
```

After this line is run, the terminal window will display the progress of the algorithm. Once finished, the script will print coordinates of UAV locations, and an external window will open with a visualization of the UAVs and users in map_density_list within the polygon depicted by map_vertex_list.
