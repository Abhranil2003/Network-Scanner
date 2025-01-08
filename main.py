import argparse
import os
from network_scanner import scan_network
from port_scanner import scan_ports
from visualization import display_table
from config import DEFAULT_PORTS, VERBOSE, set_custom_config
from utils import validate_ip_range, validate_port_list, parse_port_list, print_verbose

def save_results_to_file(results, file_format="txt", filename="scan_results"):
    """
    Save the scan results to a file in either txt or csv format.

    Args:
        results (list): The list of results to save.
        file_format (str): The file format to save in ('txt' or 'csv').
        filename (str): The name of the file to save results in.
    """
    file_path = f"{filename}.{file_format}"

    if file_format == "txt":
        with open(file_path, "w") as file:
            file.write("IP Address\tMAC Address\tOpen Ports\n")
            for result in results:
                file.write(f"{result['IP']}\t{result['MAC']}\t{','.join(map(str, result['Open Ports']))}\n")
    elif file_format == "csv":
        import csv
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["IP Address", "MAC Address", "Open Ports"])
            for result in results:
                writer.writerow([result['IP'], result['MAC'], ','.join(map(str, result['Open Ports']))])
    else:
        print("Invalid file format. Please choose either 'txt' or 'csv'.")
        return

    print(f"Results saved to {file_path}")

def main():
    # Argument parser for user inputs
    parser = argparse.ArgumentParser(description="Network Scanner: Scan a network for active hosts and open ports.")
    parser.add_argument("-r", "--range", type=str, help="IP range to scan (e.g., 192.168.1.1/24).", default=None)
    parser.add_argument("-p", "--ports", type=str, help="Comma-separated list of ports to scan (e.g., 22,80,443).", default=",".join(map(str, DEFAULT_PORTS)))
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output for detailed logging.")
    parser.add_argument("-f", "--file", type=str, help="Save the results to a file (txt or csv).", choices=["txt", "csv"], default=None)
    parser.add_argument("-o", "--output", type=str, help="Specify the output file name (default: 'scan_results').", default="scan_results")

    args = parser.parse_args()

    # Set custom configurations based on user input
    ip_range = args.range if args.range else "192.168.1.1/24"  # Default IP range if not provided
    ports_string = args.ports
    verbose = args.verbose
    file_format = args.file
    output_filename = args.output

    # Set configurations dynamically
    set_custom_config(ip_range=ip_range, ports=parse_port_list(ports_string), verbose=verbose)

    # Validate IP range
    if not validate_ip_range(ip_range):
        print("Invalid IP range format. Please provide a valid CIDR format (e.g., 192.168.1.1/24).")
        return

    # Validate ports
    if not validate_port_list(DEFAULT_PORTS):
        print("Invalid port numbers. Please provide valid port numbers between 1 and 65535.")
        return

    # Verbose logging
    print_verbose(f"Scanning network: {ip_range}", verbose)
    print_verbose(f"Scanning ports: {DEFAULT_PORTS}", verbose)
    
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
        open_ports = scan_ports(ip, DEFAULT_PORTS)
        results.append({'IP': ip, 'MAC': host['mac'], 'Open Ports': open_ports})
    
    # Step 3: Display results
    print("\nScan Results:")
    display_table(results)

    # Step 4: Save results to file (if the user requested it)
    if file_format:
        save_results_to_file(results, file_format, output_filename)

if __name__ == "__main__":
    main()
