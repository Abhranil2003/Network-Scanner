from scapy.all import ARP, Ether, srp # type: ignore

def scan_network(ip_range):
    """
    Scans the specified IP range for active devices using ARP requests.

    Args:
        ip_range (str): The IP range to scan (e.g., "192.168.1.1/24").

    Returns:
        list: A list of dictionaries, each containing 'ip' and 'mac' of an active device.
    """
    print(f"Sending ARP requests to IP range: {ip_range}")
    
    # Create an ARP request packet and broadcast it
    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    # Send the packet and collect responses
    answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]

    # Parse responses to extract IP and MAC addresses
    devices = []
    for sent, received in answered_list:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    return devices
