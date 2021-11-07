

Multipath TCP in SDN
===


## Environment setup

Following are the requirements to be setup before running this project

1. Python 3
2. [Mininet from source](!http://mininet.org/download/)
3. [Ryu Controller](https://ryu.readthedocs.io/en/latest/getting_started.html)


Code Usage
---
1. Clone this repository
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

#### Flow dump
![flow dump](https://github.com/PSIB0T/Multipath-Routing/blob/main/Screenshot/flow_dump_s1.png?raw=true)

#### Group dump
![group dump](https://github.com/PSIB0T/Multipath-Routing/blob/main/Screenshot/group_dump_s1.png?raw=true)

Controller generates a new flow table entry whose action corresponds to a group table entry. Group table entry in itself has 3 entries, each corresponding to an output port. Weights are assigned based on the logic discussed in previous section. 



#### IPERF Client - Host 1
![Host 1](https://github.com/PSIB0T/Multipath-Routing/blob/main/Screenshot/host1.png?raw=true)

#### IPERF Server - Host 2
![Host 2](https://github.com/PSIB0T/Multipath-Routing/blob/main/Screenshot/host2.png?raw=true)


#### Port dump
![Run commands](https://github.com/PSIB0T/Multipath-Routing/blob/main/Screenshot/mininet_interface.png?raw=true)

