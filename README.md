# Check_ports.py
Simple TCP port scanner for a host.

It supports:
- Single ports (for example: 22)
- Comma-separated ports (for example: 22,80,443)
- Port ranges (for example: 8000-8100)
- Mixed values (for example: 22,80,443,8000-8100)

The script scans ports in parallel using threads, which makes large scans much faster.

## Requirements

- Python 3.9+ (works on most Python 3 versions with type hints support)
- Standard library only (no external packages)

## File

- check_ports.py

## Usage

From the project folder:

python3 check_ports.py <host> "<ports>" [timeout_seconds] [workers]

### Arguments

1. host (required)
- Hostname or IP address
- Examples: 127.0.0.1, localhost, scanme.nmap.org

2. ports (required)
- Port list and/or ranges as a string
- Examples: "22", "22,80,443", "1-1024", "22,80,443,8000-8010"

3. timeout_seconds (optional)
- Per-port timeout in seconds
- Default: 1.0
- Lower values are faster but may miss slow responses

4. workers (optional)
- Number of parallel threads
- Default: 200
- Higher values can speed up scans but use more CPU/network resources

## Examples

Basic:

python3 check_ports.py 127.0.0.1 "22,80,443"

Range scan:

python3 check_ports.py 127.0.0.1 "1-1024"

Large scan with faster timeout:

python3 check_ports.py 127.0.0.1 "1-65000" 0.1 400

Scan a hostname:

python3 check_ports.py scanme.nmap.org "22,80,443" 0.2 200

## Output

Each line is printed as:

<host>:<port> open
or
<host>:<port> closed

Example output:

127.0.0.1:22 open
127.0.0.1:80 closed
127.0.0.1:443 closed

## Notes on Large Port Ranges

- Valid TCP ports are 1 to 65535.
- Scanning 1-65000 is supported.
- Total scan time depends on timeout and workers.
- If a scan is too slow:
  - Reduce timeout (for example 0.05 to 0.2)
  - Increase workers carefully (for example 200 to 800)

## Common Errors

- timeout_seconds must be > 0
  - Use a positive number like 0.1 or 1.0

- workers must be > 0
  - Use a positive integer like 100 or 400

## Security and Permission Notes

- Port scanning systems you do not own or have permission to test may be illegal or against policy.
- Some networks/firewalls may block or rate-limit scan traffic.

## Quick Start
python3 check_ports.py 127.0.0.1 "1-1000" 0.1 300
