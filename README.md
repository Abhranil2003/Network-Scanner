# Network Scanner

## Overview

This project is a Network Scanner tool that scans a network for active hosts and identifies open ports. The tool is implemented in Python and uses libraries like `scapy` and `socket`. It provides functionality to visualize results in a user-friendly format and save the output to a file.

## Features

- Scan a network for active hosts using ARP requests.
- Identify open ports on active hosts using socket connections.
- Save scan results to a `.txt` or `.csv` file.
- User-friendly table visualization of results.
- Support for user-defined IP ranges and port lists.
- Verbose mode for detailed output.

## Prerequisites

Ensure you have Python 3.7 or later installed. Install the required Python libraries:

```bash
pip install scapy tabulate
```

## File Structure

```
.
├── main.py               # Entry point of the application
├── network_scanner.py    # Handles network scanning (ARP requests)
├── port_scanner.py       # Handles port scanning
├── visualization.py      # Handles visualization of results
├── config.py             # Configuration file for default settings
├── utils.py              # Utility functions for validation and logging
├── LICENSE               # License for the project
└── README.md             # Project documentation
```

## Usage

### Command-line Arguments

The tool supports the following command-line arguments:

| Argument      | Description                                                | Default Value               |
|---------------|------------------------------------------------------------|-----------------------------|
| `-r, --range` | IP range to scan (e.g., `192.168.1.1/24`).                  | `192.168.1.1/24`            |
| `-p, --ports` | Comma-separated list of ports to scan (e.g., `22,80,443`).  | Common ports (see `config`) |
| `-v, --verbose` | Enable verbose output for detailed logging.                | Disabled                    |
| `-f, --file`  | Save the results to a file (`txt` or `csv`).                | None                        |
| `-o, --output` | Specify the output file name (default: `scan_results`).     | `scan_results`              |

### Examples

#### Basic Scan

Scan the default IP range with common ports:

```bash
python main.py
```

#### Custom IP Range and Ports

Specify a custom IP range and port list:

```bash
python main.py -r 192.168.0.1/24 -p 22,80,443
```

#### Save Results to a File

Save the results in `csv` format:

```bash
python main.py -f csv -o my_scan_results
```

#### Enable Verbose Mode

Enable detailed logging:

```bash
python main.py -v
```

## Sample Output

### Command Output

```
Found 3 active host(s):
+-----------------+-------------------+-------------+
| IP Address      | MAC Address       | Open Ports |
+-----------------+-------------------+-------------+
| 192.168.1.2     | aa:bb:cc:dd:ee:ff | 22, 80     |
| 192.168.1.3     | aa:bb:cc:dd:ee:11 | 443         |
| 192.168.1.4     | aa:bb:cc:dd:ee:22 | 22, 8080    |
+-----------------+-------------------+-------------+
```

### Saved Results

#### TXT Format

```
IP Address MAC Address Open Ports
192.168.1.2 aa:bb:cc:dd:ee:ff 22,80
192.168.1.3 aa:bb:cc:dd:ee:11 443
192.168.1.4 aa:bb:cc:dd:ee:22 22,8080
```

#### CSV Format

```
IP Address,MAC Address,Open Ports
192.168.1.2,aa:bb:cc:dd:ee:ff,22,80
192.168.1.3,aa:bb:cc:dd:ee:11,443
192.168.1.4,aa:bb:cc:dd:ee:22,22,8080
```

## Configuration

Default settings can be modified in the `config.py` file:

```python
# Default IP range for network scanning
DEFAULT_IP_RANGE = "192.168.1.1/24"

# Default list of common ports to scan
DEFAULT_PORTS = [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]

# Timeout for socket connections (in seconds)
SOCKET_TIMEOUT = 1

# Verbosity level (True for detailed output, False for minimal output)
VERBOSE = False
```

## 🐜 License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Submit a pull request with a detailed description of changes.

---

## 💬 Feedback

We welcome your feedback! If you encounter any issues or have suggestions for improvement, feel free to open an issue or contribute to the project.

### How to Provide Feedback

1. **Open an Issue**: If you find a bug or have an enhancement suggestion, please open an issue in the [GitHub repository](https://github.com/your-username/NetworkScanner/issues).
2. **Submit a Pull Request**: If you've fixed a bug or added a new feature, submit a pull request for review. Please follow the contribution guidelines outlined below.

Thank you!
