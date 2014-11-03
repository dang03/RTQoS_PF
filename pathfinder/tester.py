#!/usr/bin/env python
# encoding: utf-8



__author__ = 'Dani'

# Import libraries
import os
import argparse
import json
import sys
import Pathfinder
import random
import re
import httplib
import time
from datetime import datetime

delta_sec = 5  # seconds to delay in time.sleep

class mcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.OKGREEN = ''
        self.FAIL = ''
        self.ENDC = ''



def request_builder_rnd(controller):

    # Get all the edges/links
    command = "curl -s http://%s//wm/topology/links/json" % controller
    rtTopo = json.loads((os.popen(command).read()))
    print rtTopo
    print command+"\n"


    for link_d in rtTopo:

                link_d['bandwidth'] = random.randrange(20, 30)
                link_d['delay'] = random.uniform(0.2, 0.8)
                link_d['jitter'] = random.uniform(0.1, 0.4)
                link_d['packet-loss'] = random.uniform(0.8, 0.9)



    return rtTopo

def forwarder(path):
    """ Given a JSON list of <switch DPID, portA, portB>, installs flowmod rules into network OpenFlow switches"""
    for device in path:

        print device

        if 'requestID' in device:
            srcIp = device['srcIP']
            dstIp = device['dstIP']
            print srcIp
            print dstIp

        else:
            pass

    for device in path:

        if 'switch' in device:
            switch = device['switch']
            Iport = device['port1']
            Eport = device['port2']


            command = "curl -s -d '{\"switch\": \"%s\", \"name\":\"%s\", \"src-ip\":\"%s\", \"dst-ip\":\"%s\", \"ether-type\":\"%s\", \"cookie\":\"0\", \"priority\":\"32768\", \"ingress-port\":\"%s\",\"active\":\"true\", \"actions\":\"enqueue=%s:1\"}' http://%s/wm/staticflowentrypusher/json" % (switch, switch+"-"+Iport+"."+Eport+".f", srcIp, dstIp, "0x800", Iport, Eport, controllerRestIp)
            result = os.popen(command).read()
            print command

            command = "curl -s -d '{\"switch\": \"%s\", \"name\":\"%s\", \"ether-type\":\"%s\", \"cookie\":\"0\", \"priority\":\"32768\", \"ingress-port\":\"%s\",\"active\":\"true\", \"actions\":\"output=%s\"}' http://%s/wm/staticflowentrypusher/json" % (switch, switch+"-"+Iport+"."+Eport+".farp", "0x806", Iport, Eport, controllerRestIp)
            result = os.popen(command).read()
            print command

            command = "curl -s -d '{\"switch\": \"%s\", \"name\":\"%s\", \"src-ip\":\"%s\", \"dst-ip\":\"%s\", \"ether-type\":\"%s\", \"cookie\":\"0\", \"priority\":\"32768\", \"ingress-port\":\"%s\",\"active\":\"true\", \"actions\":\"enqueue=%s:1\"}' http://%s/wm/staticflowentrypusher/json" % (switch, switch+"-"+Eport+"."+Iport+".r", dstIp, srcIp, "0x800", Eport, Iport, controllerRestIp)
            result = os.popen(command).read()
            print command

            command = "curl -s -d '{\"switch\": \"%s\", \"name\":\"%s\", \"ether-type\":\"%s\", \"cookie\":\"0\", \"priority\":\"32768\", \"ingress-port\":\"%s\",\"active\":\"true\", \"actions\":\"output=%s\"}' http://%s/wm/staticflowentrypusher/json" % (switch, switch+"-"+Eport+"."+Iport+".rarp", "0x806", Eport, Iport, controllerRestIp)
            result = os.popen(command).read()
            print command

        else:
            pass


    return






# if __name__ == '__main__':

# parse controller address.
# Syntax:
# *FLOODLIGHT* --controller {IP:REST_PORT}
# Usage from CLI, e.g.: python Adapter.py --input request.json

parser = argparse.ArgumentParser(description='Pathfinder tester script')
parser.add_argument('--controller', '-c', dest='controllerRestIp', action='store', default='localhost:8080',
                    help='controller IP:RESTport, e.g., localhost:8080 or A.B.C.D:8080')
parser.add_argument('--api', '-a', dest='RestAPIIp', action='store', default='127.0.0.1:5000',
                    help='controller IP:RESTport, e.g., localhost:8080 or A.B.C.D:8080')
parser.add_argument('--file', '-f', dest='topoFile', default=None,
                    help='Optional topology file path, e.g., pathfinder/topoFile.json', metavar='FILE')
args = parser.parse_args()
print args, "\n"

global topofile


# INPUT: First it checks if a local request source file exists, called request.json for testing purposes,
# that will include QoS requirements plus necessary data unavailable from the controller

controllerRestIp = args.controllerRestIp
restAPIIp = args.RestAPIIp

time.sleep(delta_sec)

'''randomize topology QoS stats'''
topology = request_builder_rnd(controllerRestIp)

"""
testRequest_body = str({"src": {"srcSwitch": "00:00:00:00:00:00:00:05", "srcPort": 3}, "dst": {"dstSwitch": "00:00:00:00:00:00:00:06", "dstPort": 3}, "requestID": "r3qu357", "parameters": { "delay": 0, "bandwidth": 8, "packet-loss": 0, "jitter": 0},)
testRequest_topo = {"topology": rtTopo}
"""

print "Creating new request file.\n"
with open('PFinput3.json', 'wb') as PFtester:
    json.dump(topology, PFtester, indent=4)
    PFtester.close()

"""
command = 'sudo python API.py'
result = os.popen(command).read()
print command + "\n"
print "QoS Request:", result
"""

with open('path.json', 'r') as PFpath:
           pathfile = json.load(PFpath)
           PFpath.close()


forwarder(pathfile)

"""
command = 'sudo curl -i -H "Content-Type: application/xml" -vX POST -d @circuitRequest.xml http://%s/pathfinder/provisioner' % args.RestAPIIp
result = os.popen(command).read()
print command + "\n"
print "QoS Request:", result
"""

"""
command = 'curl -i -H "Content-Type: application/json" -vX POST -d @PFinput2.json http://127.0.0.1:5000/pathfinder/run_app2'
result = os.popen(command).read()
print command + "\n"
print "QoS Request:", result
"""

'''GUI'''
'''codehere'''

