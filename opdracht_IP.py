# Individuele opdracht IP
# Auteur: Koen van der sijs
# Student nr: s1090241
#
import sys
# if (sys.version_info < (3, 0)):
#    raise Exception('script should not be run with python2.x')
import ipaddress
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
from ipwhois.exceptions import IPDefinedError
import logging
from dpkt.udp import UDP
from tld import get_tld
from tld.exceptions import TldDomainNotFound

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
    #Log = User_Interface.Main_program().Logging()

    def __init__(self):
        self.Log = None
        self.compare_input= None
        self.bestanden = None
        self.IP_list = None
        # self.user = User_Interface.Main_program()
        # self.Logger = User_Interface.Main_program().Logging()


        print()
        # self.choices = {
        #         "1": self.file_input,
        #         "2": self.back,
        #         "3": self.quit
        #         }



    #     User_Interface.Main_program().run()

    def quit(self):
        sys.exit(0)
    # need to create a main function, so that the whole script will tune tihout the need to call the different functions.

    def main(self,bestanden,compare_file):

        self.Log = User_Interface.Main_program().Logging()
        self.bestanden = bestanden
        self.compare_input = compare_file
        output =self.Filter_IP(bestanden)
        print(output)
        if output and self.compare_input is not None:
            compare_output =self.Compare(output,self.compare_input)
            if compare_output:
                self.WHOIS(compare_output)
                self.timeline(compare_output)
            else:
                print ("Not available")
        else:
            print("No input given")
    # also absolete class this will be handeled in the user interface class

    def set_compare(self,input_compare):
        self.compare_input = input_compare

    def file_input(self):
        lijst = []
        dictionary={}
        aantal = int(input('Input the ammount of files'))
        #fout afhandeling
        for i in range(aantal):
            test = input('Input file: ')
            print (test)
            lijst.append(test)
        #onderstaande kan in Filter_IP script
        dictionary.update(self.Filter_IP(lijst))
        print(dictionary)
        self.write( dictionary)

        # determine if it's a relative path or an absolute path
    # moet in main zodat je het hier kan aanroepen voor elk input bestand.


    # class that will filter the IP adresses that resides in an pcap file
    def Filter_IP (self, bestanden):

        IP_list=Counter()
        temp_list =[]
        match_list ={}
        hashes={}
        temp_ip=''
        self.bestanden=bestanden
        print(self.bestanden)
        # compare_bestand = open(os.path.join(sys.path[0],self.compare_input),'r')
        for bestand in self.bestanden:
            # hashes[bestand]=User_Interface.Main_program.bereken_hash(bestand)

            # for bestand in bestanden:
            # Notice in the final program os.path.join sys.path needs to be removed.
            # Because bestand will be converted to absolute paths.
            pcap =open (bestand,'rb')
            pcap = dpkt.pcap.Reader(pcap)
            for timestamp,buf in pcap:
                eth = dpkt.ethernet.Ethernet(buf)
                if not isinstance(eth.data, dpkt.ip.IP):
                   # print('Non IP Packet type not supported %s\n' % eth.data.__class__.__name__)
                   continue


                if eth.type == dpkt.ethernet.ETH_TYPE_IP6:
                    ipv6=eth.data
                    # for compare_ip in compare_bestand:
                    #     if compare_ip == self.convert_IP(ipv6.src):
                    #         match_list[os.path.join(sys.path[0],bestand)]=compare_ip

                    IP_list[self.convert_IP(ipv6.src)]+=1
                    IP_list[self.convert_IP(ipv6.dst)]+=1


                    # print(self.convert_IP(ipv6.src))
                    # print(self.convert_IP(ipv6.dst))
                ip=eth.data
                IP_list[self.convert_IP(ip.src)]+=1
                IP_list[self.convert_IP(ip.dst)]+=1

        return IP_list
    # will be used to convert an hex ip to an human readable format
    def convert_IP(self,ip_adress):
        try:
            return socket.inet_ntop(socket.AF_INET, ip_adress)
        except ValueError:
            return socket.inet_ntop(socket.AF_INET6, ip_adress)

    #  will be used to write out the list of IP-adreses
    def write (self,input):
        with open(os.path.join(sys.path[0],str(date.today())+'.txt'),'w+') as file:
            # file.write(filename + ':')strftime("%Y-%m-%d %H:%M", gmtime()))
            file.write('IP-address      count' +'\n')
            for ip, waarde in input.items():
                print(ip)
                print(waarde)
                file.write( '{0:<16} {1:>8}'.format(ip,str(waarde))+'\n')
            file.flush()
        file.close()
    # function that will compare the list of IP-adresses to the IP-adresses inside the pcap file
    def Compare(self, IPlijst,compare_input):
        print(compare_input)
        temp_lijst = []
        match_list=[]
        # print(list(IPlijst.keys())[0])

        bestand = open(os.path.join(sys.path[0],compare_input),'r')
        for rij in bestand:
            print(rij)
            rij = rij.strip('\n')
            temp_lijst.append(rij)
        if temp_lijst:
            for ip in list(IPlijst.keys()):
                # print(ip)
                if ip in temp_lijst:
                    # print(ip)
                    match_list.append(ip)

        else:
            print("file is empty")
        if match_list:
            print(match_list)
            print(self.bestanden)
            return match_list
        else:
            print("no match")
        bestand.close()
        # else:
        #     User_Interface.Main_program().run()


    def json_time_converter(self, timestamp):
        if isinstance(timestamp, datetime.datetime):
            return timestamp.__str__()

    # function to get the whois information about an IP
    def WHOIS(self,match_list):
        print (match_list)

        for ip in match_list:
            indicator = {}

            with open(os.path.join(sys.path[0], 'output3.json'), 'at') as file:
                indicator['Queried_IP:'] = ip
                # check if IP is private address.
                if ipaddress.ip_address(ip).is_private:
                    indicator['Queried_domain'] = "Private address space"
                else:
                    obj = IPWhois(ip)
                    results = obj.lookup_rdap(depth=1)
                    print(results)

                    try:
                        indicator['Queried_domain'] = socket.getfqdn(ip)
                        tld= get_tld('http://'+socket.getfqdn(ip))
                        dict =(pythonwhois.get_whois(tld))
                    except TldDomainNotFound as e:
                        print(e)
                        continue


                #nog opzoek naar een betere whois, kan raw evt weglaten.

                    del dict["raw"]
                    print(self.dig(get_tld('http://'+socket.getfqdn(ip))))
                print (dict)
                indicator.update(dict)
                print(indicator)
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
    # note to self ip_list is an list object and is not a file location. Maybe it would be useful to read the
    def timeline(self, ip_list):
        print(self.bestanden)
        for bestand in self.bestanden:
            print(bestand)
            pcap =open (os.path.join(sys.path[0], bestand),'rb')
            pcap = dpkt.pcap.Reader(pcap)
            # need to change the for loop because now it isn't sorted on IP-adress, but on date..
            for timestamp,buf in pcap:
                eth = dpkt.ethernet.Ethernet(buf)
                for ip in ip_list:
                    # tcp = ip.data
                    # print (ip)
                  #   if eth.type == dpkt.ethernet.ETH_TYPE_IP6:
                  #       ipv6=eth.data
                  #       if self.convert_IP(ipv6.src) == ip:
                  #           print( 'Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))
                  #           print( 'IP: %s -> %s   (len=%d ttl=%d)\n' % \
                  # (self.convert_IP(ipv6.src), self.convert_IP(ipv6.dst), ipv6.len, ipv6.ttl))
                  # will now print ipv6 address, still need to implement that the function will print source and destination port.

                    if eth.type == dpkt.ethernet.ETH_TYPE_IP6:
                        ipv6 = eth.data
                        fh = dpkt.ip.IP_PROTO_FRAGMENT
                        ic = dpkt.ip.IP_PROTO_ICMP6
                        icmpv6 = ipv6.data


                        # get src and dst ip address
                        # src_ip = socket.inet_ntop( ipv6.src)
                        # dst_ip = socket.inet_ntop(ipv6.dst)
                        print(self.convert_IP(ipv6.src))
                    elif eth.type !=dpkt.ethernet.ETH_TYPE_IP:
                        print("Not supported eth type")
                        continue
                    else:
                        ipv4 = eth.data
                        # also check if IP.dst is equal to ip
                        if(self.convert_IP(ipv4.src)) == ip:
                            print( 'Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))
                            print( 'IP: %s -> %s   (len=%d ttl=%d)\n' % \
                            (self.convert_IP(ipv4.src), self.convert_IP(ipv4.dst), ipv4.len, ipv4.ttl))
                            if ipv4.p== dpkt.ip.IP_PROTO_UDP:
                                udp =ipv4.data
                                udp_source_port = udp.sport
                                udp_destination_port = udp.dport
                                print("Protocol: UDP\n"
                                      "Source port: "+ str(udp_source_port)+ "\n"
                                      "Destination port: "+ str(udp_destination_port))

                            elif ipv4.p==dpkt.ip.IP_PROTO_TCP:
                                tcp=ipv4.data
                                tcp_source_port = tcp.sport
                                tcp_destination_port = tcp.dport
                                print("Protocol: TCP\n"
                                      "Source port: "+ str(tcp_source_port)+ "\n"
                                      "Destination port: "+ str(tcp_destination_port))

                            elif ipv4.p == dpkt.ip.IP_PROTO_ICMP:
                                print("Protocol: ICMP")
                            else:
                                print( ipv4.p)


# test = IP_filtering()
# IP_filtering.timeline(test,"C:\\Users\\kvandersijs\\PycharmProjects\\IPFIT5\\003hslmwa.pcap","C:\\Users\\kvandersijs\\PycharmProjects\\IPFIT5\\IP.txt")


# if __name__ == "__main__":
#     IP_filtering().run_ip()
#     # self.timeline('003hslmwa.pcap',compare('IP.txt',Filter_IP('003hslmwa.pcap')))
#
#     # 184.50.160.199
#     # bestand =bestand
#     # file = open(bestand, 'r')
#     # pcap =dpkt.pcap.Reader(file)
#     # for ts, buf in pcap:
#     #eth = dpkt.ethernet.Ethernet(buf)
