import ipaddress
from typing import List


def validate_ip_range(ip_range: str) -> bool:
    """
    Validate whether the given IP range is in valid CIDR format.

    Args:
        ip_range (str): IP range (e.g., "192.168.1.1/24")

    Returns:
        bool: True if valid CIDR, False otherwise
    """
    try:
        ipaddress.IPv4Network(ip_range, strict=False)
        return True
    except ValueError:
        return False


def validate_port_list(ports: List[int]) -> bool:
    """
    Validate whether all ports are within valid TCP/UDP range.

    Args:
        ports (List[int]): List of port numbers

    Returns:
        bool: True if all ports are valid, False otherwise
    """
    if not ports:
        return False

    for port in ports:
        if not isinstance(port, int) or not (1 <= port <= 65535):
            return False

    return True
