import dpkt
import hashlib as hash
import os
import sys
BUFFERSIZE =65536
def open_bestand(bestanden, aantal):
    lijst = []
    #fout afhandeling
    for i in range(aantal):
        lijst.append(input('geef bestand op'))

def bereken_hash(bestand):

    sha256hash = hash.sha3_256()
    with open(os.path.join(sys.path[0]+ '\\'+ bestand),'rb') as file:
        file_buffer = file.read(BUFFERSIZE)
        while len(file_buffer)>0:
            sha256hash.update(file_buffer)
            file_buffer= file.read(BUFFERSIZE)
    print(sha256hash.hexdigest())




    # bestand =bestand
    # file = open(bestand, 'r')
    # pcap =dpkt.pcap.Reader(file)
    # for ts, buf in pcap:
    #     eth = dpkt.ethernet.Ethernet(buf)

bereken_hash('test.py')
