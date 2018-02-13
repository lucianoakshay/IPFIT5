import dpkt
import hashlib

def open_bestand(bestanden, aantal):
    lijst = []
    #fout afhandeling
    for i in range(aantal):
        lijst.append(input('geef bestand op'))

def bereken_hash(bestand):






    bestand =bestand
    file = open(bestand, 'r')
    pcap =dpkt.pcap.Reader(file)
    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)

