import sys
# if (sys.version_info < (3, 0)):
#    raise Exception('script should not be run with python2.x')

import datetime
from time import gmtime,strftime
import os
import json
import dns.resolver
# if 'ipwhois'or 'pythonwhois' or 'tld' or 'dpkt'in sys.modules:
from ipwhois import IPWhois
import dpkt
import pythonwhois
import logging

from tld import get_tld

# else:
#     raise ImportError('error')


import socket
from collections import Counter
import Main


class IP_filtering:

    IDS = [
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

    def __init__(self):

        self.choices = {
                "1": self.file_input,
                "2": self.back
                }
        print()

    def display_menu(self):
                print("""
Menu
1. Input_file
2. Go_back
""")

    def run_ip(self):

        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def back(self):
        Main.Main_program().run()

    def file_input(self):
        lijst = []
        aantal =input('Input the ammount of files')
        #fout afhandeling
        for i in range(aantal):
            lijst.append(input('geef bestand op'))


        self.Filter_IP(lijst)

    # moet in main zodat je het hier kan aanroepen voor elk input bestand.



    def Filter_IP (self,bestand):
        IP_list=Counter()
        temp_ip=''
        bestand=bestand
        # for bestand in bestanden:
        pcap =open (os.path.join(sys.path[0], bestand),'rb')
        pcap = dpkt.pcap.Reader(pcap)
        for timestamp,buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if eth.type == dpkt.ethernet.ETH_TYPE_IP6:
                ipv6=eth.data
                IP_list[self.convert_IP(ipv6.src)]+=1
                IP_list[self.convert_IP(ipv6.dst)]+=1
                print(self.convert_IP(ipv6.src))
                print(self.convert_IP(ipv6.dst))
                continue

            ip=eth.data

            if not isinstance(eth.data, dpkt.ip.IP):
               print('Non IP Packet type not supported %s\n' % eth.data.__class__.__name__)
               continue
            IP_list[self.convert_IP(ip.src)]+=1
            IP_list[self.convert_IP(ip.dst)]+=1
        return IP_list

    def convert_IP(ip_adress):
        try:
            return socket.inet_ntop(socket.AF_INET, ip_adress)
        except ValueError:
            return socket.inet_ntop(socket.AF_INET6, ip_adress)

    def write (filename,input):
        file = open(os.path.join(sys.path[0],strftime("%Y-%m-%d %H:%M", gmtime()))+'IP', 'w+')
        file.write(filename+ ':')
        file.write('IP-address      count' +'\n')
        for ip,waarde in input.items():
            print(ip)
            file.write( '{0:<16} {1:>8}'.format(ip,str(waarde))+'\n')
        file.close()

    def compare(self,input_lijst,IPlijst):
        temp_lijst = []
        match_list=[]
        print(list(IPlijst.keys())[0])
        bestand = open(os.path.join(sys.path[0],input_lijst),'r')
        for rij in bestand:
            rij = rij.strip('\n')
            temp_lijst.append(rij)
        if temp_lijst:
            for ip in list(IPlijst.keys()):
                if ip in  temp_lijst:
                    match_list.append(ip)
        else:
            print("file is empty")
        if match_list:
            return(match_list)
        else:
            print("no match")
        bestand.close()


    def json_time_converter(self,timestamp):
        if isinstance(timestamp, datetime.datetime):
            return timestamp.__str__()

    def WHOIS(self,match_list):
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

                print(self.DIG(get_tld('http://'+socket.getfqdn(ip))))
                # print (dict)
                indicator.update(dict)
                # string = string.strip('['+']'+"\\n")
                file.write(json.dumps(indicator,default=self.json_time_converter))

    def DIG(self,domain):


        for record in self.IDS:
            try:
                answers = dns.resolver.query(domain, record)
                for rdata in answers:
                    print(record, ':', rdata.to_text())

            except Exception as e:
                continue  # or pass
    def timeline(self,bestand,ip_list):
        pcap =open (os.path.join(sys.path[0], bestand),'rb')
        pcap = dpkt.pcap.Reader(pcap)

        for timestamp,buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            for ip in ip_list:
                if eth.type == dpkt.ethernet.ETH_TYPE_IP6:
                    ipv6=eth.data
                    if self.convert_IP(ipv6.src)==ip:
                        print( 'Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))
                        print( 'IP: %s -> %s   (len=%d ttl=%d)\n' % \
              (self.convert_IP(ipv6.src), self.convert_IP(ipv6.dst), ipv6.len, ipv6.ttl))
                if eth.type ==dpkt.ethernet.ETH_TYPE_IP:
                    ipv4 = eth.data
                    if(self.convert_IP(ipv4.src))==ip:
                        print( 'Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))
                        print( 'IP: %s -> %s   (len=%d ttl=%d)\n' % \
              (self.convert_IP(ipv4.src), self.convert_IP(ipv4.dst), ipv4.len, ipv4.ttl))
if __name__ == "__main__":
    IP_filtering().run()
# timeline('003hslmwa.pcap',compare('IP.txt',Filter_IP('003hslmwa.pcap')))
    # 184.50.160.199
    # bestand =bestand
    # file = open(bestand, 'r')
    # pcap =dpkt.pcap.Reader(file)
    # for ts, buf in pcap:
    #     eth = dpkt.ethernet.Ethernet(buf)
