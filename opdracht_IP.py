# Individuele opdracht IP
# Auteur: Koen van der sijs
# Student nr: s1090241
#
import sys
import ipaddress
import datetime
from datetime import date
import os
import dns.resolver
import dpkt
import pythonwhois
import binascii
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
            'AAAA',
            'NS',
            'CNAME',
            'SOA',
            'MX',
            'TXT',
            'SRV',
            'CERT',
            'NSEC',
            'DNSKEY',
            'SPF',
        ]

    def __init__(self):
        # Will be used to set the logger in the main function
        self.Log = None
        # Will be used to set the compare file in the main function
        self.compare_input = None
        # Will be used to
        self.pcap_files = None

        self.IP_list = None
        # Will be used to set the filename for the WHOIS output
        self.whois_filename = os.path.join(sys.path[0], 'Whois_info_' + str(date.today()) + ".csv")

        # Will be used to set the filename for the IP-adresses
        self.ip_filename = os.path.join(sys.path[0], "IP_address_"+str(date.today())+".txt")

        self.similarties_filename = os.path.join(sys.path[0], "Similarities_" + str(date.today()) + ".txt")

        # Will be used to set the name of the timeline file
        self.timeline_filename = os.path.join(sys.path[0], "Time_line output" + str(date.today()) + ".txt")

        # Protocol list, will be used to determine the protocol when creating the timeline
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

    # The main function that will be used to start the IP-script. needs 3 arguments, the location of the pcap files the location of the list with IP-addresses and a boolean value to check if there is internet access
    def main(self, pcap_files, compare_file, internet, location):

        self.whois_filename = os.path.join(location, 'Whois_info_' + str(date.today()) + ".csv")

        # Will be used to set the filename for the IP-adresses
        self.ip_filename = os.path.join(location, "IP_address_" + str(date.today()) + ".txt")

        self.similarties_filename = os.path.join(location, "Similarities_" + str(date.today()) + ".txt")

        # Will be used to set the name of the timeline file
        self.timeline_filename = os.path.join(location, "Time_line output" + str(date.today()) + ".txt")

        self.Log = User_Interface.Main_program().Logging()
        self.pcap_files = pcap_files

        self.compare_input = compare_file
        self.Log.info("Filtering files" + str(pcap_files))
        output = self.Filter_IP(pcap_files)

        if output and self.compare_input is not None:
            self.write_IP(output, self.ip_filename)
            compare_output = self.Compare(output, self.compare_input)

            if compare_output and internet:
                self.WHOIS(compare_output)
                self.timeline(compare_output)
                self.Log.info("Created files:"+"\n"+self.ip_filename + "\n" + self.whois_filename + "\n"
                              + self.similarties_filename + "\n" + self.timeline_filename)
                print("The following files have been created:" + "\n"+self.ip_filename + "\n" + self.whois_filename + "\n"
                      + self.similarties_filename + "\n"+self.timeline_filename)

            elif compare_output and not internet:
                print("No internet access")
                self.Log.info("Created files:"+"\n"+self.ip_filename + "\n" + self.similarties_filename)
                print("The following files have been created:" + "\n"+self.ip_filename + "\n" + self.similarties_filename)
            else:
                self.Log.info("No similarities found in: " + compare_file)
                print("No similarties found")

                print("The following files have been created:" + self.ip_filename)
        elif output and self.compare_input is None:
            self.write_IP(output, self.ip_filename)
            self.Log.info("Will only filter For IP-addresses and will not compare")
            print("Only filtered out IP-addresses")
            print("Created file:"+"\n"+self.ip_filename)
        else:
            self.Log.info("No IP-addresses found in the files:" + str(pcap_files))
            print("No IP addresses could be found in the files:" + str(pcap_files))

    # class that will filter the IP adresses that resides in an pcap file
    def Filter_IP(self, bestanden):

        IP_list = Counter()

        self.bestanden = bestanden
        for bestand in self.bestanden:
            self.Log.info("Opening file: " + bestand)
            pcap = open(bestand, 'rb')
            pcap = dpkt.pcap.Reader(pcap)
            for timestamp, buf in pcap:
                eth = dpkt.ethernet.Ethernet(buf)

                if eth.type == dpkt.ethernet.ETH_TYPE_IP6:
                    ipv6 = eth.data

                    IP_list[self.convert_IP(ipv6.src)] += 1
                    IP_list[self.convert_IP(ipv6.dst)] += 1

                elif eth.type == dpkt.ethernet.ETH_TYPE_IP:
                    ip=eth.data
                    IP_list[self.convert_IP(ip.src)] += 1
                    IP_list[self.convert_IP(ip.dst)] += 1

                if not isinstance(eth.data, dpkt.ip.IP):
                    continue

        return IP_list

    # will be used to convert an hex ip to an human readable format
    def convert_IP(self, ip_adress):
        try:
            return socket.inet_ntop(socket.AF_INET, ip_adress)
        except ValueError:
            return socket.inet_ntop(socket.AF_INET6, ip_adress)

    #  will be used to write out the list of IP-adreses
    def write_IP(self, input, filename):
        self.Log.info("Writing IP_addresses to file:" + self.ip_filename)

        with open(filename, 'w+') as file:
            file.write('IP-address      count' + '\n')
            for ip, value in input.items():

                file.write('{0:<16} {1:>8}'.format(ip, str(value)) + '\n')
            file.flush()
        file.close()

    # function that will compare the list of IP-adresses to the IP-adresses inside the pcap file
    def Compare(self, IPlist, compare_input):
        temp_list = []
        match_list = []
        # print(list(IPlijst.keys())[0])
        self.Log.info("Reading the IP-list file: " + str(os.path.abspath(compare_input)))
        bestand = open(os.path.abspath(compare_input), 'r')
        for rij in bestand:
            rij = rij.strip('\n')
            try:
                ipaddress.ip_address(rij)
                temp_list.append(rij)
            except ValueError:
                self.Log.error("File seem to contain none valid IP-address")
                self.Log.error("IP-address:" + str(rij) + " Will not be used to compare")
                print("File seem to contain none valid IP-address")
                print("IP-address:" + str(rij) + " Will not be used to compare")
                print(temp_list)
                continue

        for ip in list(IPlist.keys()):
            if ip in temp_list:
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

    def write_compare(self, similarties):
        self.Log.info("Writing simalarites file to: " + self.similarties_filename)
        with open(self.similarties_filename, 'w+')as file:
            file.write("IP_addresses: \n")
            for ip in similarties:
                file.write(ip + "\n")

    # function to get the whois information about an IP
    def WHOIS(self, match_list):
        print(match_list)
        whoisdict = {}
        dig_dictionary = {}
        for ip in match_list:
            indicator = {}
            self.Log.info("Writing WHOIS info to: " + self.whois_filename)
            with open(self.whois_filename, 'at', newline='') as file:
                writer = csv.writer(file)
                indicator['Queried_IP:'] = ip
                # check if IP is private address.
                if ipaddress.ip_address(ip).is_private:
                    indicator['Queried_domain'] = "Private address space"
                    dig_dictionary['DIG:'] = "No values"
                else:
                    self.Log.info("Quering WHOIS lookup for IP: " + str(ip))
                    try:
                        indicator['Queried_domain'] = socket.getfqdn(ip)
                        tld = get_tld('http://'+socket.getfqdn(ip))
                        whoisdict = (pythonwhois.get_whois(tld))

                        print(tld)
                        dig_dictionary = self.dig(tld)
                    except TldDomainNotFound as e:
                        print("TLD of IP couldn't be found, check your internet access")
                        continue
                # nog opzoek naar een betere whois, kan raw evt weglaten.

                    del whoisdict["raw"]
                indicator.update(whoisdict)
                # string = string.strip('['+']'+"\\n")
                for key, value in indicator.items():
                    writer.writerow([key, value])

                for key, value in dig_dictionary.items():
                    writer.writerow([key, value])
                writer.writerow(['___________']*10)

    # function to preform a dig on a domain
    def dig(self, domain):
        output = ''
        dig_dictionary = dict()
        self.Log.info("Preforming DIG on domain:" + domain)
        for record in self.IDS:
            try:

                answers = dns.resolver.query(domain, record)
                for rdata in answers:
                    print(record + ':' + rdata.to_text()+"\n")
                    output += (record + ':' + rdata.to_text()+"\n")
                dig_dictionary["DIG: "] = output

            except Exception as e:
                print(e)
                continue  # or pass
        return dig_dictionary

    def timeline(self, ip_list):
        print(self.bestanden)
        for bestand in self.bestanden:
            self.Log.info("Opening pcap file" + os.path.join(sys.path[0], bestand))
            pcap = open(os.path.join(sys.path[0], bestand), 'rb')
            pcap = dpkt.pcap.Reader(pcap)
            print("Preforming timeline analyses:")
            # need to change the for loop because now it isn't sorted on IP-adress, but on date..
            for timestamp, buf in pcap:
                eth = dpkt.ethernet.Ethernet(buf)
                for ip in ip_list:

                    if eth.type == dpkt.ethernet.ETH_TYPE_IP or eth.type == dpkt.ethernet.ETH_TYPE_IP6:
                        ipv4 = eth.data
                        # also check if IP.dst is equal to ip
                        if(self.convert_IP(ipv4.src)) == ip:
                            with open(self.timeline_filename,  'at') as file:
                                print('Timestamp: ' + str(datetime.datetime.utcfromtimestamp(timestamp)))
                                file.write('Timestamp: ' + str(datetime.datetime.utcfromtimestamp(timestamp)) + '\n')
                                file.write('Mac Address: ' + self.convert_to_mac(binascii.hexlify(eth.src)) + "->"
                                           + self.convert_to_mac(binascii.hexlify(eth.dst)) + "\n")

                                if eth.type == dpkt.ethernet.ETH_TYPE_IP:
                                    print('IP: %s -> %s   (len=%d ttl=%d)' % \
                                          (self.convert_IP(ipv4.src), self.convert_IP(ipv4.dst), ipv4.len, ipv4.ttl))
                                    file.write('IP: %s -> %s   (len=%d ttl=%d)' % \
                                               (self.convert_IP(ipv4.src), self.convert_IP(ipv4.dst), ipv4.len, ipv4.ttl))

                                else:
                                    file.write('IP: %s -> %s ' % \
                                               (self.convert_IP(ipv4.src), self.convert_IP(ipv4.dst)))

                                if ipv4.p == dpkt.ip.IP_PROTO_UDP:
                                    udp = ipv4.data
                                    udp_source_port = udp.sport
                                    udp_destination_port = udp.dport
                                    file.write("Protocol: UDP\n"
                                               "Source port: " + self.check_protocol(udp_source_port) + "\n"
                                               "Destination port: " + self.check_protocol(udp_destination_port) + '\n')

                                elif ipv4.p == dpkt.ip.IP_PROTO_TCP:
                                    tcp = ipv4.data
                                    tcp_source_port = tcp.sport
                                    tcp_destination_port = tcp.dport

                                    file.write("Protocol: TCP\n"
                                               "Source port: " + self.check_protocol(tcp_source_port) + "\n"
                                               "Destination port:" + self.check_protocol(tcp_destination_port) + '\n')

                                elif ipv4.p == dpkt.ip.IP_PROTO_ICMP:
                                    print("Protocol: ICMP")
                                else:
                                    print(ipv4.p)
                                file.write("\n")

    # will be used to check the protocol of an IP-package
    def check_protocol(self, port):
        if int(port) < 1024:
            if int(port) in self.protocol_list:
                protocol = str(port) + " "+str(self.protocol_list[port])

            else:
                protocol = str(port + ' Unknown protocol')
        elif int(port) < 49151:
            protocol = (str(port) + ' Registered port')
        else:
            protocol = (str(port) + ' Dynamic port')
        return protocol

    # will be used to convert hex mac adresses to printable characters
    def convert_to_mac(self, macadress):
        s = list()
        for i in range(int(12/2)):
                s.append(macadress[i*2:i*2+2].decode("utf-8"))
        r = ":".join(s)
        return r
