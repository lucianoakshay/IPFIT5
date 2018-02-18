import sys
# if (sys.version_info < (3, 0)):
#    raise Exception('script should not be run with python2.x')

import hashlib as hash
import datetime
from time import gmtime,strftime
import os
import json
import dns.resolver
# if 'ipwhois'or 'pythonwhois' or 'tld' or 'dpkt'in sys.modules:
from ipwhois import IPWhois
import dpkt
import pythonwhois

from tld import get_tld

# else:
#     raise ImportError('error')


import socket
from collections import Counter

def open_bestand(aantal):
    lijst = []
    #fout afhandeling
    for i in range(aantal):
        lijst.append(input('geef bestand op'))
    Filter_IP(lijst)

# moet in main zodat je het hier kan aanroepen voor elk input bestand.



def Filter_IP (bestand):
    IP_list=Counter()
    temp_ip=''
    bestand=bestand
    # for bestand in bestanden:

    pcap =open (os.path.join(sys.path[0], bestand),'rb')
    pcap = dpkt.pcap.Reader(pcap)
    for timestamp,buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip=eth.data
        if not isinstance(eth.data, dpkt.ip.IP):
           print('Non IP Packet type not supported %s\n' % eth.data.__class__.__name__)
           continue
        IP_list[convert_IP(ip.src)]+=1
        IP_list[convert_IP(ip.dst)]+=1
    return IP_list

def convert_IP(ip_adress):
    try:
        return socket.inet_ntop(socket.AF_INET, ip_adress)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, ip_adress)

def write (filename,input):
    aantal = ''
    file = open(os.path.join(sys.path[0],strftime("%Y-%m-%d %H:%M", gmtime()))+'IP', 'w+')
    file.write(filename+ ':')
    file.write('IP-address      count' +'\n')
    for ip,waarde in input.items():
        print(ip)
        file.write( '{0:<16} {1:>8}'.format(ip,str(waarde))+'\n')
    file.close()

def compare(input_lijst,IPlijst):
    temp_lijst = []
    match_list=[]
    print(list(IPlijst.keys())[0])
    bestand = open(os.path.join(sys.path[0],input_lijst),'r')
    for rij in bestand:
        rij = rij.strip('\n')
        temp_lijst.append(rij)

    for ip in list(IPlijst.keys()):
        if ip in  temp_lijst:
            match_list.append(ip)
    bestand.close()
    return(match_list)

def json_time_converter(timestamp):
    if isinstance(timestamp, datetime.datetime):
        return timestamp.__str__()

def WHOIS(match_list):
    print (match_list)

    for ip in match_list:
        indicator = {}

        with open(os.path.join(sys.path[0],'output2.json'), 'at') as file:
            obj = IPWhois(ip)
            results = obj.lookup_rdap(depth=1)
            print(results)
            indicator['Queried_IP:']=ip
            indicator['Queried_domain']=socket.getfqdn(ip)
            #nog opzoek naar een betere whois, kan raw evt weglaten.
            dict =(pythonwhois.get_whois(get_tld('http://'+socket.getfqdn(ip))))

            print(DIG(get_tld('http://'+socket.getfqdn(ip))))
            # print (dict)
            indicator.update(dict)
            # string = string.strip('['+']'+"\\n")
            file.write(json.dumps(indicator,default=json_time_converter))

def DIG(domain):
    ids = [
        'NONE',
        'A',
        'NS',
        'MD',
        'MF',
        'CNAME',
        'SOA',
        'MB',
        'MG',
        'MR',
        'NULL',
        'WKS',
        'PTR',
        'HINFO',
        'MINFO',
        'MX',
        'TXT',
        'RP',
        'AFSDB',
        'X25',
        'ISDN',
        'RT',
        'NSAP',
        'NSAP-PTR',
        'SIG',
        'KEY',
        'PX',
        'GPOS',
        'AAAA',
        'LOC',
        'NXT',
        'SRV',
        'NAPTR',
        'KX',
        'CERT',
        'A6',
        'DNAME',
        'OPT',
        'APL',
        'DS',
        'SSHFP',
        'IPSECKEY',
        'RRSIG',
        'NSEC',
        'DNSKEY',
        'DHCID',
        'NSEC3',
        'NSEC3PARAM',
        'TLSA',
        'HIP',
        'CDS',
        'CDNSKEY',
        'CSYNC',
        'SPF',
        'UNSPEC',
        'EUI48',
        'EUI64',
        'TKEY',
        'TSIG',
        'IXFR',
        'AXFR',
        'MAILB',
        'MAILA',
        'ANY',
        'URI',
        'CAA',
        'TA',
        'DLV',
    ]

    for record in ids:
        try:
            answers = dns.resolver.query(domain, record)
            for rdata in answers:
                print(record, ':', rdata.to_text())

        except Exception as e:
            continue  # or pass

WHOIS(compare('IP.txt',Filter_IP('003hslmwa.pcap')))

    # bestand =bestand
    # file = open(bestand, 'r')
    # pcap =dpkt.pcap.Reader(file)
    # for ts, buf in pcap:
    #     eth = dpkt.ethernet.Ethernet(buf)
