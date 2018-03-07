import sys
# if (sys.version_info < (3, 0)):
#    raise Exception('script should not be run with python2.x')

import datetime
# from time import gmtime,strftime
from datetime import date
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
# to do
# make sure that the input files are add here also make this class more fault tolerant


import socket
from collections import Counter
import User_Interface
# need to fix write function
# list of all possible dns records
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
        # self.choices = {
        #         "1": self.file_input,
        #         "2": self.back,
        #         "3": self.quit
        #         }
        print()
    # deprecated function will possibly be removed
    def display_menu(self):
                print("""
Menu
1. Input_file
2. Go_back
3. Quit
""")

    # def run_ip(self):
    #
    #     while True:
    #         self.display_menu()
    #         User_Interface.Main_program().Logging().info("testing")
    #         choice = input("Enter an option: ")
    #         action = self.choices.get(choice)
    #         if action:
    #             action()
    #         else:
    #             print("{0} is not a valid choice".format(choice))
    #
    # def back(self):
    #     User_Interface.Main_program().run()
    #
    # def quit(self):
    #     sys.exit(0)
    # also absolete class this will be handeled in the user interface class
    def file_input(self):
        lijst = []
        dictionary={}
        dictionary2={}
        aantal = int(input('Input the ammount of files'))
        #fout afhandeling
        for i in range(aantal):
            test = input('Input file: ')
            print (test)
            lijst.append(test)
        #onderstaande kan in Filter_IP script
        dictionary.update(self.Filter_IP(lijst))
        print(dictionary)
        self.write('test', dictionary)
        # determine if it's a relative path or an absolute path
    # moet in main zodat je het hier kan aanroepen voor elk input bestand.


    # class that will filter the IP adresses that resides in an pcap file
    def Filter_IP (self, bestanden):
        IP_list=Counter()
        hashes={}
        temp_ip=''
        bestanden=bestanden
        print(bestanden)
        for bestand in bestanden:
            # hashes[bestand]=User_Interface.Main_program.bereken_hash(bestand)

            # for bestand in bestanden:
            # Notice in the final program os.path.join sys.path needs to be removed.
            # Because bestand will be converted to absolute paths.
            pcap =open (os.path.join(sys.path[0], bestand),'rb')
            pcap = dpkt.pcap.Reader(pcap)
            for timestamp,buf in pcap:
                eth = dpkt.ethernet.Ethernet(buf)
                if eth.type == dpkt.ethernet.ETH_TYPE_IP6:
                    ipv6=eth.data
                    IP_list[self.convert_IP(ipv6.src)]+=1
                    IP_list[self.convert_IP(ipv6.dst)]+=1
                    # print(self.convert_IP(ipv6.src))
                    # print(self.convert_IP(ipv6.dst))
                    continue

                ip=eth.data

                if not isinstance(eth.data, dpkt.ip.IP):
                   # print('Non IP Packet type not supported %s\n' % eth.data.__class__.__name__)
                   continue
                IP_list[self.convert_IP(ip.src)]+=1
                IP_list[self.convert_IP(ip.dst)]+=1
        print( IP_list)
    # will be used to convert an hex ip to an human readable format
    def convert_IP(self,ip_adress):
        try:
            return socket.inet_ntop(socket.AF_INET, ip_adress)
        except ValueError:
            return socket.inet_ntop(socket.AF_INET6, ip_adress)

    #  will be used to write out the list of IP-adreses
    def write (self, filename, input):
        with open(os.path.join(sys.path[0],str(date.today())+'.txt'),'w+') as file:
            # file.write(filename + ':')strftime("%Y-%m-%d %H:%M", gmtime()))
            file.write('IP-address      count' +'\n')
            for ip, waarde in input.items():
                print(ip)
                print('test')
                print(waarde)
                file.write( '{0:<16} {1:>8}'.format(ip,str(waarde))+'\n')
            file.flush()
    # function that will compare the list of IP-adresses to the IP-adresses inside the pcap file
    def compare(self, input_lijst, IPlijst):
        temp_lijst = []
        match_list=[]
        print(list(IPlijst.keys())[0])
        bestand = open(os.path.join(sys.path[0],input_lijst),'r')
        for rij in bestand:
            rij = rij.strip('\n')
            temp_lijst.append(rij)
        if temp_lijst:
            for ip in list(IPlijst.keys()):
                if ip in temp_lijst:
                    match_list.append(ip)
        else:
            print("file is empty")
        if match_list:
            return match_list
        else:
            print("no match")
        bestand.close()


    def json_time_converter(self, timestamp):
        if isinstance(timestamp, datetime.datetime):
            return timestamp.__str__()
    # function to get the whois information about an
    def WHOIS(self,match_list):
        print (match_list)

        for ip in match_list:
            indicator = {}

            with open(os.path.join(sys.path[0], 'output2.json'), 'at') as file:
                obj = IPWhois(ip)
                results = obj.lookup_rdap(depth=1)
                print(results)
                indicator['Queried_IP:'] = ip
                indicator['Queried_domain'] = socket.getfqdn(ip)

                #nog opzoek naar een betere whois, kan raw evt weglaten.
                dict =(pythonwhois.get_whois(get_tld('http://'+socket.getfqdn(ip))))
                del dict["raw"]
                print(self.dig(get_tld('http://'+socket.getfqdn(ip))))
                # print (dict)
                indicator.update(dict)
                # string = string.strip('['+']'+"\\n")
                file.write(json.dumps(indicator,default=self.json_time_converter))
    # function to preform a dig on a domain
    def dig(self, domain):

        for record in self.IDS:
            try:
                answers = dns.resolver.query(domain, record)
                for rdata in answers:
                    print(record, ':', rdata.to_text())

            except Exception as e:
                continue  # or pass
    # dit is dubbel op kan waarschijnlijk verplaatst worden naar de functie die het pcap bestand opent.

    # function to create a timelin, needs to be adjusted so that it can show the ports and the protocol.
    def timeline(self, bestand, ip_list):
        pcap =open (os.path.join(sys.path[0], bestand),'rb')
        pcap = dpkt.pcap.Reader(pcap)

        for timestamp,buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            for ip in ip_list:
                if eth.type == dpkt.ethernet.ETH_TYPE_IP6:
                    ipv6=eth.data
                    if self.convert_IP(ipv6.src) == ip:
                        print( 'Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))
                        print( 'IP: %s -> %s   (len=%d ttl=%d)\n' % \
              (self.convert_IP(ipv6.src), self.convert_IP(ipv6.dst), ipv6.len, ipv6.ttl))

                if eth.type ==dpkt.ethernet.ETH_TYPE_IP:
                    ipv4 = eth.data

                    if(self.convert_IP(ipv4.src)) == ip:
                        print( 'Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))
                        print( 'IP: %s -> %s   (len=%d ttl=%d)\n' % \
                        (self.convert_IP(ipv4.src), self.convert_IP(ipv4.dst), ipv4.len, ipv4.ttl))



# if __name__ == "__main__":
#     IP_filtering().run_ip()
# timeline('003hslmwa.pcap',compare('IP.txt',Filter_IP('003hslmwa.pcap')))
    # 184.50.160.199
    # bestand =bestand
    # file = open(bestand, 'r')
    # pcap =dpkt.pcap.Reader(file)
    # for ts, buf in pcap:
    #eth = dpkt.ethernet.Ethernet(buf)
