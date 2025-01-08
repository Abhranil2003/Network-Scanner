# Default configuration for the Network Scanner project

# Default IP range for network scanning
DEFAULT_IP_RANGE = "192.168.1.1/24"  # Replace with your subnet if needed

# Default list of common ports to scan
DEFAULT_PORTS = [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]

# Timeout for socket connections (in seconds)
SOCKET_TIMEOUT = 1

# Verbosity level (True for detailed output, False for minimal output)
VERBOSE = False

# Function to override default configurations (optional)
def set_custom_config(ip_range=None, ports=None, verbose=None):
    global DEFAULT_IP_RANGE, DEFAULT_PORTS, VERBOSE

    if ip_range:
        DEFAULT_IP_RANGE = ip_range
    if ports is not None:
        DEFAULT_PORTS = ports
    if verbose is not None:
        VERBOSE = verbose
