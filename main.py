import argparse
from network_scanner import scan_network
from port_scanner import scan_ports
from visualization import display_table
from config import DEFAULT_PORTS, DEFAULT_IP_RANGE, VERBOSE
from utils import validate_ip_range, validate_port_list, parse_port_list, print_verbose

def main():
    # Argument parser for user inputs
    parser = argparse.ArgumentParser(description="Network Scanner: Scan a network for active hosts and open ports.")
    parser.add_argument("-r", "--range", type=str, help="IP range to scan (e.g., 192.168.1.1/24).", default=DEFAULT_IP_RANGE)
    parser.add_argument("-p", "--ports", type=str, help="Comma-separated list of ports to scan (e.g., 22,80,443).", default=",".join(map(str, DEFAULT_PORTS)))
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output for detailed logging.")

    args = parser.parse_args()
    ip_range = args.range
    ports_string = args.ports
    verbose = args.verbose

    # Validate IP range
    if not validate_ip_range(ip_range):
        print("Invalid IP range format. Please provide a valid CIDR format (e.g., 192.168.1.1/24).")
        return

    # Parse and validate ports
    ports = parse_port_list(ports_string)
    if not validate_port_list(ports):
        print("Invalid port numbers. Please provide valid port numbers between 1 and 65535.")
        return

    # Verbose logging
    print_verbose(f"Scanning network: {ip_range}", verbose)
    print_verbose(f"Scanning ports: {ports}", verbose)
    
    # Step 1: Scan network for active hosts
    print_verbose(f"Sending ARP requests to the IP range: {ip_range}", verbose)
    active_hosts = scan_network(ip_range)
    if not active_hosts:
        print("No active hosts found.")
        return

    print(f"Found {len(active_hosts)} active host(s):")
    display_table(active_hosts)

    # Step 2: Scan open ports for each active host
    print_verbose("\nScanning ports on active hosts...", verbose)
    results = []
    for host in active_hosts:
        ip = host['ip']
        open_ports = scan_ports(ip, ports)
        results.append({'IP': ip, 'MAC': host['mac'], 'Open Ports': open_ports})
    
    # Step 3: Display results
    print("\nScan Results:")
    display_table(results)

if __name__ == "__main__":
    main()
