import ipaddress

def validate_ip_range(ip_range):
    """
    Validates whether the given IP range is in a valid CIDR format.

    Args:
        ip_range (str): The IP range to validate (e.g., "192.168.1.1/24").

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        ipaddress.IPv4Network(ip_range, strict=False)
        return True
    except ValueError:
        return False

def validate_port_list(ports):
    """
    Validates whether the provided list of ports is valid.

    Args:
        ports (list): A list of port numbers to validate.

    Returns:
        bool: True if all ports are valid, False otherwise.
    """
    for port in ports:
        if not (1 <= port <= 65535):
            return False
    return True

def parse_port_list(port_string):
    """
    Parses a comma-separated string of ports into a list of integers.

    Args:
        port_string (str): Comma-separated port numbers (e.g., "22,80,443").

    Returns:
        list: A list of integers representing the ports.
    """
    try:
        return [int(port.strip()) for port in port_string.split(",")]
    except ValueError:
        return []

def print_verbose(message, verbose):
    """
    Prints a message if verbosity is enabled.

    Args:
        message (str): The message to print.
        verbose (bool): Flag indicating whether to print the message.
    """
    if verbose:
        print(message)
