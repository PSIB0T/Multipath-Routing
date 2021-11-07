

Multipath TCP in SDN
===

## Environment setup

Following are the requirements to be setup before running this project

1. Python 3
2. [Mininet from source](!http://mininet.org/download/)
3. [Ryu Controller](https://ryu.readthedocs.io/en/latest/getting_started.html)


Code Usage
---
1. Clone [this](https://github.com/PSIB0T/Multipath-Routing) repository
2. Start the controller by
`ryu-manager --observe-links controller_multipath.py`
3. Start one of the topologies by
`sudo python3 topology_3path.py`

Results
---

#### Topology

![Topology](https://github.com/PSIB0T/Multipath-Routing/blob/main/Screenshot/3path_topo.png?raw=true)

![Topology diagram](https://github.com/PSIB0T/Multipath-Routing/blob/main/Screenshot/topology_diagram.png?raw=true)

#### Path calculation 
![Controller](https://github.com/PSIB0T/Multipath-Routing/blob/main/Screenshot/controller.png?raw=true)

When the first packet is sent from h1 to h2, the path between these hosts get calculated using **OSPF** and weight metrics are calculated depending on number of links between hosts and bandwith of those links. 
Weight calculation is done using the following equation


<center>
<img src="https://latex.codecogs.com/png.image?\dpi{110}&space;1&space;-&space;\frac{pw(p)}{\sum_{i=0}^npw(i)}&space;*&space;10" title="1 - \frac{pw(p)}{\sum_{i=0}^npw(i)} * 10" />
</center>


Where
- pw\(p\) is the path weight/cost (uses OSPF cost in previous step)
- n is the total number of paths available.
#### Flow dump
![flow dump](https://github.com/PSIB0T/Multipath-Routing/blob/main/Screenshot/flow_dump_s1.png?raw=true)

#### Group dump
![group dump](https://github.com/PSIB0T/Multipath-Routing/blob/main/Screenshot/group_dump_s1.png?raw=true)

Controller generates a new flow table entry whose action corresponds to a group table entry. Group table entry in itself has 3 entries, each corresponding to an output port. Weights are assigned based on the logic discussed in previous section. 



#### IPERF Client - Host 1
![Host 1](https://github.com/PSIB0T/Multipath-Routing/blob/main/Screenshot/host1.png?raw=true)

#### IPERF Server - Host 2
![Host 2](https://github.com/PSIB0T/Multipath-Routing/blob/main/Screenshot/host2.png?raw=true)


Now we are testing the capabilities of multipath routing by establishing parallel TCP connections between h1 and h2. In this case, the number of parallel connections is 5. 


#### Port dump
![Run commands](https://github.com/PSIB0T/Multipath-Routing/blob/main/Screenshot/mininet_interface.png?raw=true)

By examining the ports of s1 and s2, we can see that the flow is mostly directed to ports s3 and s2 where the weights are more (7) in comparison to s1 (6). Similarly in the receiver side, port 3 is connected to h2 while packets are being received from 1,2 and 4. rx of port 4 is lesser compared to 1 and 2
