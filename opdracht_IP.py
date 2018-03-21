# Individuele opdracht IP
# Auteur: Koen van der sijs
# Student nr: s1090241
#
import sys
import ipaddress
import datetime
from datetime import date
import os
import json
import dns.resolver
# if 'ipwhois'or 'pythonwhois' or 'tld' or 'dpkt'in sys.modules:
from ipwhois import IPWhois
import dpkt
import pythonwhois
import binascii
import berserker_resolver as Resolver
from tld import get_tld
from tld.exceptions import TldDomainNotFound
import csv

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
            'PTR',
            'MX',
            'TXT',
            'AFSDB',
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
            'DNAME',
            'APL',
            'SSHFP',
            'IPSECKEY',
            'NSEC',
            'DNSKEY',
            'NSEC3',
            'NSEC3PARAM',
            'CDS',
            'CDNSKEY',
            'CSYNC',
            'SPF',
            'UNSPEC',
            'TSIG',
            'IXFR',
            'AXFR',
            'MAILA',
            'CAA',
        ]
    IDS2=['A',
            'NS',
            'MD',
            'MF',
            'CNAME'

    ]
    #Log = User_Interface.Main_program().Logging()

    def __init__(self):
        self.Log = None
        self.compare_input= None
        self.bestanden = None
        self.IP_list = None
        self.whois_filename=os.path.join(sys.path[0], 'Whois_info_' + str(date.today())+ ".csv")
        self.ip_filename=os.path.join(sys.path[0],"IP_address_"+str(date.today())+".txt")
        self.similarties_filename= os.path.join(sys.path[0], "Similarities_"+ str(date.today())+ ".txt")
        self.protocol_list = {
            20: 'FTP',
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            67: 'DHCP',
            68: 'DHCP',
            69: 'TFTP',
            80: 'HTTP',
            110: 'POP',
            119: 'NNTP',
            123: 'NTP',
            137: 'NETBIOS',
            138: 'NETBIOS',
            139: 'NETBIOS',
            143: 'IMAP',
            161: 'SNMP',
            162: 'SNMP',
            389: 'LDAP',
            443: 'HTTPS',
            445: 'SMB',
            485: 'SMTP/SSL',
            546: 'DHCP ipv6',
            547: 'DHCP ipv6',
            990: 'FTPS',
            993: 'IMAP',
            995: 'POP3 /ssl'
        }

    def quit(self):
        sys.exit(0)
    # need to create a main function, so that the whole script will tune tihout the need to call the different functions.

    def main(self,bestanden,compare_file, internet):

        self.Log = User_Interface.Main_program().Logging()
        self.bestanden = bestanden

        self.compare_input = compare_file
        self.Log.info("Filtering files" + str(bestanden))
        output =self.Filter_IP(bestanden)
        if output and self.compare_input is not None:
            self.write_IP(output,self.ip_filename)
            compare_output =self.Compare(output,self.compare_input)
            if compare_output and internet:
                self.WHOIS(compare_output)
                self.timeline(compare_output)
                self.Log.info ( "Created files:"+"\n"+self.ip_filename + "\n"+ self.whois_filename+  "\n" + self.similarties_filename)
                print("The following files has been created:" + "\n"+self.ip_filename + "\n"+ self.whois_filename+  "\n" + self.similarties_filename)

            elif compare_output and not internet:
                print("No internet access")
                self.Log.info ( "Created files:"+"\n"+self.ip_filename +  "\n" + self.similarties_filename)
                print("The following files has been created:" + "\n"+self.ip_filename +  "\n" + self.similarties_filename)
            else:
                self.Log.info ("No similarities found in: " + compare_file)
                print("No similarties found")

                print("The following files has been created:" + self.ip_filename )
        elif output and self.compare_input is None:
            self.Log.info("Will only filter For IP-addresses and will not compare")
            print("Only filtering for IP-adress")
        else:
            self.Log.info("No IP-addresses found.")
            print("No IP addresses could be found in the files:" +str(bestanden))

    # also absolete class this will be handeled in the user interface class

    def set_compare(self,input_compare):
        self.compare_input = input_compare


        # determine if it's a relative path or an absolute path
    # moet in main zodat je het hier kan aanroepen voor elk input bestand.


    # class that will filter the IP adresses that resides in an pcap file
    def Filter_IP (self, bestanden):

        IP_list=Counter()

        self.bestanden=bestanden
        # compare_bestand = open(os.path.join(sys.path[0],self.compare_input),'r')
        for bestand in self.bestanden:
            self.Log.info("Opening file: "+ bestand)
            pcap =open (bestand,'rb')
            pcap = dpkt.pcap.Reader(pcap)
            for timestamp,buf in pcap:
                eth = dpkt.ethernet.Ethernet(buf)



                if eth.type == dpkt.ethernet.ETH_TYPE_IP6:
                    ipv6=eth.data
                    # for compare_ip in compare_bestand:
                    #     if compare_ip == self.convert_IP(ipv6.src):
                    #         match_list[os.path.join(sys.path[0],bestand)]=compare_ip
                    # print(self.convert_IP(ipv6.src))
                    # print(self.convert_IP(ipv6.dst))
                    IP_list[self.convert_IP(ipv6.src)]+=1
                    IP_list[self.convert_IP(ipv6.dst)]+=1


                    # print(self.convert_IP(ipv6.src))
                    # print(self.convert_IP(ipv6.dst))
                elif eth.type == dpkt.ethernet.ETH_TYPE_IP:
                    ip=eth.data
                    IP_list[self.convert_IP(ip.src)]+=1
                    IP_list[self.convert_IP(ip.dst)]+=1

                if not isinstance(eth.data, dpkt.ip.IP):
                   # print('Non IP Packet type not supported %s\n' % eth.data.__class__.__name__)
                   continue

        return IP_list
    # will be used to convert an hex ip to an human readable format
    def convert_IP(self,ip_adress):
        try:
            return socket.inet_ntop(socket.AF_INET, ip_adress)
        except ValueError:
            return socket.inet_ntop(socket.AF_INET6, ip_adress)

    #  will be used to write out the list of IP-adreses
    def write_IP (self,input, filename):
        self.Log.info("Writing IP_addresses to file:" + self.ip_filename)

        with open(filename,'w+') as file:
            file.write('IP-address      count' +'\n')
            for ip, waarde in input.items():
                # print(ip)
                # print(waarde)
                file.write( '{0:<16} {1:>8}'.format(ip,str(waarde))+'\n')
            file.flush()
        file.close()

    # function that will compare the list of IP-adresses to the IP-adresses inside the pcap file
    def Compare(self, IPlijst,compare_input):
        temp_lijst = []
        match_list=[]
        # print(list(IPlijst.keys())[0])
        self.Log.info("Reading the IP-list file: " + str(os.path.abspath(compare_input)))
        bestand = open(os.path.abspath(compare_input),'r')
        for rij in bestand:
            rij = rij.strip('\n')
            try:
                ipaddress.ip_address(rij)
                temp_lijst.append(rij)
            except ValueError:
                self.Log.error("File seem to contain none valid IP-address")
                self.Log.error("IP-address:" +str(rij) +" Will not be used to compare")
                print("File seem to contain none valid IP-address")
                print ("IP-address:" +str(rij) +" Will not be used to compare")
                print (temp_lijst)
                continue


        for ip in list(IPlijst.keys()):
            # print(ip)
            if ip in temp_lijst:
                # print(ip)
                match_list.append(ip)

        if match_list:
            print("The following similarties have been found:")
            for ip in match_list:
                print(ip)

            self.write_compare(match_list)
            return match_list

        else:
            self.Log.info("No matches found")
        bestand.close()
        # else:
        #     User_Interface.Main_program().run()
    def write_compare(self,similarties):
        self.Log.info("Writing simalarites file to: " + self.similarties_filename)
        with open(self.similarties_filename, 'w+')as file:
            file.write("IP_addresses: \n")
            for ip in similarties:
                file.write(ip+ "\n")


    # absolete
    def json_time_converter(self, timestamp):
        if isinstance(timestamp, datetime.datetime):
            return timestamp.__str__()

    # function to get the whois information about an IP
    def WHOIS(self,match_list):
        print (match_list)
        dict= {}
        dig_dictionary={}
        for ip in match_list:
            indicator = {}
            self.Log.info("Writing WHOIS info to: "+ self.whois_filename)
            with open(self.whois_filename, 'at',newline='') as file:
                writer = csv.writer(file)
                indicator['Queried_IP:'] = ip
                # check if IP is private address.
                if ipaddress.ip_address(ip).is_private:
                    indicator['Queried_domain'] = "Private address space"
                    dig_dictionary[ 'DIG']= "No values"
                else:
                    self.Log.info("Quering WHOIS lookup for IP: "+ str(ip))
                    try:
                        indicator['Queried_domain'] = socket.getfqdn(ip)
                        tld= get_tld('http://'+socket.getfqdn(ip))
                        dict =(pythonwhois.get_whois(tld))

                        print (tld)
                        dig_dictionary =self.dig(tld)
                    except TldDomainNotFound as e:
                        print("TLD of IP couldn't be found, check your internet access")
                        continue


                #nog opzoek naar een betere whois, kan raw evt weglaten.

                    del dict["raw"]
                indicator.update(dict)
                # string = string.strip('['+']'+"\\n")
                for key,value in indicator.items():
                    writer.writerow([key,value])

                writer.writerow( "DIG results")
                for key,value in dig_dictionary.items():
                    writer.writerow([key,value])
                writer.writerow( ['___________']*10)
    # function to preform a dig on a domain
    def dig(self, domain):
        dig_dictionary = dict()
        self.Log.info("Preforming DIG on domain:"+ domain)
        for record in self.IDS:
            try:
                answers = dns.resolver.query(domain, record)
                for rdata in answers:
                    print(record, ':', rdata.to_text())
                    if record in dig_dictionary:
                        dig_dictionary[record] += "\n"+ rdata.to_text()
                    else:
                        dig_dictionary[record]=rdata.to_text()

            except Exception as e:
                print (e)
                continue  # or pass
        print(dig_dictionary)
        return dig_dictionary
    # dit is dubbel op kan waarschijnlijk verplaatst worden naar de functie die het pcap bestand opent.

    # function to create a timelin, needs to be adjusted so that it can show the ports and the protocol.
    # note to self ip_list is an list object and is not a file location. Maybe it would be useful to read the
    def timeline(self, ip_list):
        print(self.bestanden)
        for bestand in self.bestanden:
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
                        if(self.convert_IP(ipv6.src)) == ip or self.convert_IP(ipv6.dst)==ip:
                            # get src and dst ip address
                            # src_ip = socket.inet_ntop( ipv6.src)
                            # dst_ip = socket.inet_ntop(ipv6.dst)
                            print( 'Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))
                            print('Ethernet Frame: ', self.convert_to_mac(binascii.hexlify(eth.src)), self.convert_to_mac(binascii.hexlify(eth.dst)), eth.type)
                            print( 'IP: %s -> %s   \n' % \
                                (self.convert_IP(ipv6.src), self.convert_IP(ipv6.dst)))
                            if ipv6.p== dpkt.ip.IP_PROTO_UDP :
                                udp =ipv6.data
                                udp_source_port = udp.sport
                                udp_destination_port = udp.dport
                                print("Protocol: UDP\n"
                                      "Source port: "+ str(udp_source_port)+ "\n"
                                      "Destination port: "+ str(udp_destination_port) +  '\n')
                            elif ipv6.p == dpkt.ip.IP_PROTO_TCP:
                                tcp = ipv6.data
                                tcp_source_port = tcp.sport
                                tcp_destination_port = tcp.dport

                                print ("Protocol: TCP\n"
                                       "Source port: "+ self.check_protocol(tcp_source_port)+ "\n"
                                       "Destination port:"+ self.check_protocol(tcp_destination_port) +  '\n')

                    elif eth.type == dpkt.ethernet.ETH_TYPE_IP:
                        ipv4 = eth.data
                        # also check if IP.dst is equal to ip
                        if(self.convert_IP(ipv4.src)) == ip:
                            print( 'Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))
                            print('Ethernet Frame: ', self.convert_to_mac(binascii.hexlify(eth.src)), self.convert_to_mac(binascii.hexlify(eth.dst)))
                            print( 'IP: %s -> %s   (len=%d ttl=%d)' % \
                            (self.convert_IP(ipv4.src), self.convert_IP(ipv4.dst), ipv4.len, ipv4.ttl))
                            if ipv4.p== dpkt.ip.IP_PROTO_UDP :
                                udp =ipv4.data
                                udp_source_port = udp.sport
                                udp_destination_port = udp.dport
                                print("Protocol: UDP\n"
                                      "Source port: "+ str(udp_source_port)+ "\n"
                                      "Destination port: "+ str(udp_destination_port) +  '\n')
                            elif ipv4.p == dpkt.ip.IP_PROTO_TCP:
                                tcp = ipv4.data
                                tcp_source_port = tcp.sport
                                tcp_destination_port = tcp.dport

                                print ("Protocol: TCP\n"
                                       "Source port: "+ self.check_protocol(tcp_source_port)+ "\n"
                                       "Destination port:"+ self.check_protocol(tcp_destination_port) +  '\n')

                            elif ipv4.p == dpkt.ip.IP_PROTO_ICMP:
                                print("Protocol: ICMP")
                            else:
                                print( ipv4.p)
                    # elif eth.type ==dpkt.ethernet.ETH_TYPE_ARP:
                    #     arp = eth.arp
                    #     print(self.convert_to_mac(binascii.hexlify(arp.sha)))
                    #     print(self.convert_to_mac(binascii.hexlify(arp.tha)))
                    # else:
                    #     print('Non IP Packet type not supported %s\n' % eth.data.__class__.__name__)


    def check_protocol(self, port):
        protocol = ''
        if int(port) < 1024:
            if int(port) in self.protocol_list:
               protocol= str(port) + " "+str(self.protocol_list[port])

            else:
                protocol = str(port + ' Unknown protocol')
        elif int(port) > 1024 and int(port) <49151:
            protocol = (str(port)+ ' Registered port')
        else:
            protocol= (str(port) + ' Dynamic port')
        return protocol


    def convert_to_mac(self, macadress):
        s = list()
        for i in range(int(12/2)) :  # mac_addr should always be 12 chars, we work in groups of 2 chars
                s.append( macadress[i*2:i*2+2].decode("utf-8") )
        r = ":".join(s)
        return r

    # def output_to_string(self,):
