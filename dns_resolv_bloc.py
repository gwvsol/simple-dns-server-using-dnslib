# -*- coding: utf-8 -*-

from json import loads
from dnslib import *
from dnslib import server

def load_json():
    with open('dns.conf', 'rt') as f:
        conf = loads(f.read())
    return conf

# download the configuration file
conf = load_json()
print(conf)

local_dns = conf['loc_dns']             # local address dns server
local_port = conf['loc_port']           # local port dns server
ext_dns = conf['ext_dns']               # external address dns server
ext_port = conf['ext_port']             # external port dns server
restrict = conf['bloc']                 # list of blocked resources
resovl = conf['resolv']                 # local name resources


class ResolvName:
    """
    DNS query processing. Requests to resources that are 
    restricted are blocked. Processing resolver name on 
    the local network.
    """
    def resolve(self, request, handler):
        d = request.reply()
        q = request.get_q()
        q_name = str(q.qname)
        
        if q_name[:-1] in restrict:
            d.truncate()                        # handling resource limits
        elif q_name[:-1] in resovl.keys():      # local network name resolver
            d.add_answer(*RR.fromZone('{} 60 A {}'.format(q_name[:-1], resovl[q_name[:-1]])))
        else:                                   # processing other requests
            a = DNSRecord.parse(DNSRecord.question(q_name).send(ext_dns, ext_port))
            for rr in a.rr:
                d.add_answer(rr)
        return d

resolver = ResolvName()
logger = server.DNSLogger()
s = server.DNSServer(resolver, port=local_port, address=local_dns, logger=logger)
s.start_thread()

while True:
    pass




