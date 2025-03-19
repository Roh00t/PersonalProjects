# Linux Enumeration & Privilege Escalation Script

## Overview
This script is designed to perform an in-depth security audit of a Linux system. It helps penetration testers, security researchers, and system administrators identify misconfigurations, weak permissions, and potential privilege escalation paths.

## Features
- System Information Enumeration
- User & Group Information Extraction
- Environmental Variables and Path Permissions Analysis
- Cron Jobs & Systemd Timers Review
- Network and Open Ports Inspection
- Running Services & Process Analysis
- Software and Version Information Collection
- Searching for Sensitive Files & Configurations
- Identifying Potential Privilege Escalation Vectors
- Docker & LXC Container Privilege Checks

## Enhancements
This version includes three major enhancements:
1. **Service Analysis & Potential Misconfigurations Detection**
2. **Search for Hardcoded Credentials in Scripts & Configuration Files**
3. **Detection of Unprotected Private SSH Keys**

## Usage
Run the script with the following options:
```bash
./LinEnum.sh [OPTIONS]
```

### Available Options:
| Option | Description |
|--------|-------------|
| `-k` | Enter keyword to search in configuration files |
| `-e` | Specify an export location for reports |
| `-s` | Supply user password for sudo checks (INSECURE) |
| `-t` | Enable thorough tests (may take longer) |
| `-r` | Specify a report name |
| `-h` | Show help message |

### Example Usage
```bash
./LinEnum.sh -k password -r report_name -e /tmp/ -t
```

## Requirements
- Bash shell environment
- Root or privileged user permissions (recommended for full scan)

## Notes
- This script is intended for legal security auditing and penetration testing.
- Use it only on systems you have permission to test.
- Do not run this script on production environments without proper authorization.

## Disclaimer
This script is provided for educational purposes only. The author is not responsible for any misuse or damages caused by its execution.

## License
MIT License
