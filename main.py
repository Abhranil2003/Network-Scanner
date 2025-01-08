import argparse
from network_scanner import scan_network
from port_scanner import scan_ports
from visualization import display_table
from config import DEFAULT_PORTS, DEFAULT_IP_RANGE

def main():
    # Argument parser for user inputs
    parser = argparse.ArgumentParser(description="Network Scanner: Scan a network for active hosts and open ports.")
    parser.add_argument("-r", "--range", type=str, help="IP range to scan (e.g., 192.168.1.1/24).", default=DEFAULT_IP_RANGE)
    parser.add_argument("-p", "--ports", type=str, help="Comma-separated list of ports to scan (e.g., 20,21,80).", default=",".join(map(str, DEFAULT_PORTS)))
    
    args = parser.parse_args()
    ip_range = args.range
    ports = list(map(int, args.ports.split(',')))

    print(f"Scanning network: {ip_range}")
    print(f"Scanning ports: {ports}")
    
    # Step 1: Scan network for active hosts
    active_hosts = scan_network(ip_range)
    if not active_hosts:
        print("No active hosts found.")
        return

    print(f"Found {len(active_hosts)} active host(s):")
    display_table(active_hosts)

    # Step 2: Scan open ports for each active host
    print("\nScanning ports on active hosts...")
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
