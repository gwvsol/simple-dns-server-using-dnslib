from json import loads
from dnslib import *
from dnslib import server

def load_json():
    with open('dns.conf', 'rt') as f:
        conf = loads(f.read())
    return conf

# download the configuration file
conf = load_json()

local_dns = conf['loc_dns']             # local address dns server
local_port = conf['loc_port']           # local port dns server
ext_dns = conf['ext_dns']               # external address dns server
ext_port = conf['ext_port']             # external port dns server
bloc_forv = conf['bloc']['forward']     # address to which blocked resources are forward
restrict = conf['bloc']['restricted']   # list of blocked resources
resovl = conf['resolv']                 # local name resources


class ResolvName:
    def resolve(self, request, handler):
        d = request.reply()
        q = request.get_q()
        q_name = str(q.qname)
        
        def dns_url(name, ip):
            return '{} 60 A {}'.format(name, ip)

        if q_name[:-1] in restrict:
            d.header.rcode = dnslib.RCODE.REFUSED
            #d.add_answer(*RR.fromZone(dns_url(q_name[:-1], bloc_forv)))
        elif q_name[:-1] in resovl.keys():
            d.add_answer(*RR.fromZone(dns_url(q_name[:-1], resovl[q_name[:-1]])))
        else:
            a = DNSRecord.parse(DNSRecord.question(q_name).send(ext_dns, ext_port))
            print('===================')
            print(a)
            print('===================')
            print(a.rr)
            print('===================')
            for rr in a.rr:
                d.add_answer(rr)
        print(d)
        return d

resolver = ResolvName()
logger = server.DNSLogger()
s = server.DNSServer(resolver, port=local_port, address=local_dns, logger=logger)
s.start_thread()

while True:
    pass




