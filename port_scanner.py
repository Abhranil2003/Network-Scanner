import socket

def scan_ports(host, ports):
    """
    Scans a list of ports on a given host to identify open ports.

    Args:
        host (str): The target host IP address.
        ports (list): A list of port numbers to scan.

    Returns:
        list: A list of open ports.
    """
    print(f"Scanning ports on host: {host}")
    open_ports = []
    
    for port in ports:
        try:
            # Create a socket object
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # Timeout for connection attempt
                result = s.connect_ex((host, port))  # Attempt to connect to the port
                if result == 0:  # Port is open
                    open_ports.append(port)
        except Exception as e:
            print(f"Error scanning port {port} on {host}: {e}")
    
    return open_ports
