from scapy.all import ARP, Ether, srp  # type: ignore
from typing import List, Dict

def scan_network(ip_range: str) -> List[Dict[str, str]]:
    """
    Scans the specified IP range for active devices using ARP requests.

    Args:
        ip_range (str): The IP range to scan (e.g., "192.168.1.1/24").

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing IP and MAC addresses.
    """

    # Create ARP request packet
    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    try:
        # Send packet and receive responses
        answered_list = srp(packet, timeout=2, verbose=False)[0]
    except PermissionError:
        # Scapy requires admin/root privileges
        raise PermissionError(
            "ARP scanning requires administrative/root privileges."
        )

    devices = []
    for _, received in answered_list:
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc
        })

    return devices
