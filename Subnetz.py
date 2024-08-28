import ipaddress

ip_adress = input("Geben Sie die ip Adresse an: ")
sub_mask = input("Geben Sie die Subnetzmaske oder präfix an: ")
network_ip = 0
broadcast = 0
first_host = 0
last_host = 0
jump = 0
possible_hosts = 0

cidr_to_subnet = {
    "1": "128.0.0.0",
    "2": "192.0.0.0",
    "3": "224.0.0.0",
    "4": "240.0.0.0",
    "5": "248.0.0.0",
    "6": "252.0.0.0",
    "7": "254.0.0.0",
    "8": "255.0.0.0",
    "9": "255.128.0.0",
    "10": "255.192.0.0",
    "11": "255.224.0.0",
    "12": "255.240.0.0",
    "13": "255.248.0.0",
    "14": "255.252.0.0",
    "15": "255.254.0.0",
    "16": "255.255.0.0",
    "17": "255.255.128.0",
    "18": "255.255.192.0",
    "19": "255.255.224.0",
    "20": "255.255.240.0",
    "21": "255.255.248.0",
    "22": "255.255.252.0",
    "23": "255.255.254.0",
    "24": "255.255.255.0",
    "25": "255.255.255.128",
    "26": "255.255.255.192",
    "27": "255.255.255.224",
    "28": "255.255.255.240",
    "29": "255.255.255.248",
    "30": "255.255.255.252",
    "31": "255.255.255.254",
    "32": "255.255.255.255"
}

if sub_mask.isdigit():
    subnet_mask = cidr_to_subnet.get(sub_mask)
else:
    subnet_mask = sub_mask

network = ipaddress.IPv4Network(f"{ip_adress}/{subnet_mask}", strict=False)


network_ip = network.network_address
broadcast = network.broadcast_address
first_host = network[1] if network.prefixlen < 31 else network[0]
last_host = network[-2] if network.prefixlen < 31 else network[-1]
possible_hosts = network.num_addresses - 2 if network.prefixlen < 31 else network.num_addresses  # Korrektur der Berechnung der möglichen Hosts


print(f"Netzwerk IP: {network_ip}")
print(f"Erster Host: {first_host}")
print(f"Letzter Host: {last_host}")
print(f"Broadcast IP: {broadcast}")
print(f"Anzahl der möglichen Host: {possible_hosts}")



