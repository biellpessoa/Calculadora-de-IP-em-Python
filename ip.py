import socket
import struct
# IP & Subnet
def Int2Bin(integer):
    binary = '.'.join([bin(int(x)+256)[3:] for x in integer.split('.')])
    return binary

def cidr_to_netmask(cidr):
    network, net_bits = cidr.split('/')
    host_bits = 32 - int(net_bits)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return network, netmask

def netmask_to_cidr(netmask):
	return netmask.count('1')

IP = input('Insira o endereço IP: ')
Subnet = input('Insira a máscara: ')
if len(Subnet) <= 2:
	Subnet = cidr_to_netmask(IP+'/'+str(Subnet))[1]
else:
	pass
IP_binary = Int2Bin(IP)
Subnet_binary = Int2Bin(Subnet)

print('\nIP:', IP)
print('Máscara:', Subnet)

# Wild Card
def complement(number):
    if number == '0':
        number = '1'
    elif number == '.':
        pass
    else:
        number = '0'
    return number

def get_nhosts():
	return 2**(32 - netmask_to_cidr(Subnet_binary))-2

def find_wildcard(binary_subnet):
    binary_list = list(binary_subnet)
    wildcard = ''.join(complement(binary_list[y]) for y in range(len(binary_list)))
    return wildcard

def convert_decimal(wildcard_Binary):
    binary = {}
    for x in range(4):
        binary[x] = int(wildcard_Binary.split(".")[x], 2)
    dec = ".".join(str(binary[x]) for x in range(4))
    return dec

wildcard_binary = find_wildcard(Int2Bin(Subnet))
WildCard = convert_decimal(wildcard_binary)
print('Host:', WildCard)

# Network ID
def andOP(IP1, IP2):
    ID_list = {}
    for y in range(4):
        ID_list[y] = int(IP1.split(".")[y]) & int(IP2.split(".")[y])
    ID = ".".join(str(ID_list[z]) for z in range(4))
    return ID

networkID = andOP(IP, Subnet)
network_Binary = Int2Bin(networkID)
print('Subrede:', networkID)

# Broadcast IP
def orOP(IP1, IP2):
    Broadcast_list = {}
    for z in range(4):
        Broadcast_list[z] = int(IP1.split(".")[z]) | int(IP2.split(".")[z])
    broadcast = ".".join(str(Broadcast_list[c]) for c in range(4))
    return broadcast

broadcastIP = orOP(networkID, WildCard)
broadcastIP_binary = Int2Bin(broadcastIP)
print('Broadcast:', broadcastIP)

# Max IP
def maxiIP(brdcstIP):
    maxIPs = brdcstIP.split(".")
    if int(brdcstIP.split(".")[3]) - 1 == 0:
        if int(brdcstIP.split(".")[2]) - 1 == 0:
            if int(brdcstIP.split(".")[1]) - 1 == 0:
                maxIPs[0] = int(brdcstIP.split(".")[0]) - 1
            else:
                maxIPs[1] = int(brdcstIP.split(".")[1]) - 1
        else:
            maxIPs[2] = int(brdcstIP.split(".")[2]) - 1
    else:
        maxIPs[3] = int(brdcstIP.split(".")[3]) - 1
    return ".".join(str(maxIPs[x]) for x in range(4))

maxIP = maxiIP(broadcastIP)
maxIP_binary = Int2Bin(maxIP)
print('Last Host:', maxIP)

# Min IP
def miniIP(ntwrkID):
    miniIPs = ntwrkID.split(".")
    if int(ntwrkID.split(".")[3]) + 1 == 256:
        if int(ntwrkID.split(".")[2]) + 1 == 256:
            if int(ntwrkID.split(".")[1]) + 1 == 256:
                miniIPs[0] = int(ntwrkID.split(".")[0]) + 1
                miniIPs[1] = 0
                miniIPs[2] = 0
                miniIPs[3] = 0
            else:
                miniIPs[1] = int(ntwrkID.split(".")[1]) + 1
                miniIPs[2] = 0
                miniIPs[3] = 0
        else:
            miniIPs[2] = int(ntwrkID.split(".")[2]) + 1
            miniIPs[3] = 0
    else:
        miniIPs[3] = int(ntwrkID.split(".")[3]) + 1
    return ".".join(str(miniIPs[x]) for x in range(4))

minIP = miniIP(networkID)
minIP_binary = Int2Bin(networkID)
print('First Host:', minIP)
print('Hosts utilizaveis:', get_nhosts())