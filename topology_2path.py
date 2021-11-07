#!/usr/bin/env python

import re
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call, run, PIPE


hostDict = {}

def getSwitchPortStats(sw):
    res = run(
            args = ["ovs-ofctl", "-O", "OpenFlow13", "dump-ports", sw],
            universal_newlines = True,
            stdout = PIPE)
    ports = re.split(r"port\s+", res.stdout)
    portStats = {}
    for i in range(2, len(ports)):
        match = re.search(r"(\d+): rx pkts=(\d+).*tx pkts=(\d+)", ports[i], flags=re.MULTILINE | re.DOTALL)
        if match:
            portStats[match.group(1)] = {
                "rx": match.group(2),
                "tx": match.group(3)
            }
    
    return portStats

def menu(net):
    while (True):
        print("Enter one of the following")
        print("1. Ping")
        print("2. iperf")
        print("3. switch stats")
        print("4. Print topology")
        print("q. Quit")
        inp = input()
        if inp == "1":
            inp = input("Enter hosts separated by spaces")
            count = int(input("Enter number of packets to send"))
            inp = inp.split(" ")
            inp = [hostDict[h] for h in inp]
            for i in range(count):
                net.ping(inp)
        elif inp == "2":
            inp = input("Enter hosts separated by spaces")
            count = int(input("Enter number of seconds to transmit data for"))
            inp = inp.split(" ")
            inp = [hostDict[h] for h in inp]
            net.iperf(inp, seconds=count)
        elif inp == "3":
            inp = input("Enter switches to be examined")
            sws = inp.split(" ")
            for sw in sws:
                print(sw, getSwitchPortStats(sw))
        elif inp == "4":
            for i in net.links:
                print(i)
        elif inp == "q":
            break




def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)

    hostDict["h1"] = h1
    hostDict["h2"] = h2

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(s1, s5)
    net.addLink(s5, s2)
    net.addLink(s1, s3)
    net.addLink(s3, s4)
    net.addLink(s4, s2)
    net.addLink(s2, h2)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s5').start([c0])

    info( '*** Post configure switches and hosts\n')
    # net.ping([h1, h2])
    menu(net)
    # CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

