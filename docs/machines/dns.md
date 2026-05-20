# 🏴️ DNS — Estudo Footprinting

---

## Enumeração

### 1. Consulta DNS - FQDN

Primeiro vou verificar se o domínio existe fazendo uma consulta FQDN.

```
dig fqdn inlanefreight.htb @10.129.93.11
```

**Retorno:**

```
; <<>> DiG 9.18.33-1~deb12u2-Debian <<>> fqdn inlanefreight.htb @10.129.93.11
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 21913
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; QUESTION SECTION:
;fqdn.				IN	A

;; AUTHORITY SECTION:
.			86400	IN	SOA	a.root-servers.net. nstld.verisign-grs.com. 2026051501 1800 900 604800 86400

;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 65233
;; flags: qr aa rd; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;inlanefreight.htb.		IN	A

;; AUTHORITY SECTION:
inlanefreight.htb.	604800	IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
```

**Informações coletadas:**
- Domínio: inlanefreight.htb
- SOA: root.inlanefreight.htb

### 2. Consulta DNS - SOA

Agora vou consultar o registro SOA para obter mais informações sobre a zona.

```
dig soa inlanefreight.htb @10.129.93.11
```

**Retorno:**

```
; <<>> DiG 9.18.33-1~deb12u2-Debian <<>> soa inlanefreight.htb @10.129.93.11
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 21635
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;inlanefreight.htb.		IN	SOA

;; ANSWER SECTION:
inlanefreight.htb.	604800	IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
```

### 3. Consulta DNS - ANY

Aqui vou buscar todos os registros disponíveis para o domínio.

```
dig any inlanefreight.htb @10.129.93.11
```

**Retorno:**

```
; <<>> DiG 9.18.33-1~deb12u2-Debian <<>> any inlanefreight.htb @10.129.93.11
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 16037
;; flags: qr aa rd; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 2
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;inlanefreight.htb.		IN	ANY

;; ANSWER SECTION:
inlanefreight.htb.	604800	IN	TXT	"atlassian-domain-verification=t1rKCy68JFszSdCKVpw64A1QksWdXuYFUeSXKU"
inlanefreight.htb.	604800	IN	TXT	"MS=ms97310371"
inlanefreight.htb.	604800	IN	TXT	"v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.124.8 ip4:10.129.127.2 ip4:10.129.42.106 ~all"
inlanefreight.htb.	604800	IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
inlanefreight.htb.	604800	IN	NS	ns.inlanefreight.htb.

;; ADDITIONAL SECTION:
ns.inlanefreight.htb.	604800	IN	A	127.0.0.1
```

**Informações coletadas:**
- TXT records com configurações de SPF, Atlassian, Microsoft
- Nameserver: ns.inlanefreight.htb (127.0.0.1)

### 4. Zone Transfer - AXFR

Tentando fazer um zone transfer para obter todos os registros do domínio.

```
dig axfr inlanefreight.htb @10.129.93.11
```

**Retorno:**

```
; <<>> DiG 9.18.33-1~deb12u2-Debian <<>> axfr inlanefreight.htb @10.129.93.11
;; global options: +cmd
inlanefreight.htb.	604800	IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
inlanefreight.htb.	604800	IN	TXT	"MS=ms97310371"
inlanefreight.htb.	604800	IN	TXT	"atlassian-domain-verification=t1rKCy68JFszSdCKVpw64A1QksWdXuYFUeSXKU"
inlanefreight.htb.	604800	IN	TXT	"v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.124.8 ip4:10.129.127.2 ip4:10.129.42.106 ~all"
inlanefreight.htb.	604800	IN	NS	ns.inlanefreight.htb.
app.inlanefreight.htb.	604800	IN	A	10.129.18.15
dev.inlanefreight.htb.	604800	IN	A	10.12.0.1
internal.inlanefreight.htb. 604800 IN	A	10.129.1.6
mail1.inlanefreight.htb. 604800	IN	A	10.129.18.201
ns.inlanefreight.htb.	604800	IN	A	127.0.0.1
inlanefreight.htb.	604800	IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
;; Query time: 6 msec
;; SERVER: 10.129.93.11#53(10.129.93.11) (TCP)
;; WHEN: Fri May 15 14:03:25 CDT 2026
;; XFR size: 11 records (messages 1, bytes 560)
```

**Informações coletadas:**
- Zone transfer disponível! (vulnerabilidade)
- Subdomínios descobertos: app, dev, internal, mail1

### 5. Brute Force de Subdomínios

Aqui estou usando um wordlist para tentar descobrir mais subdomínios.

```
for sub in $(cat /opt/useful/seclists/Discovery/DNS/subdomains-top1million-110000.txt);do dig $sub.inlanefreight.htb @10.129.93.11 | grep -v ';\|SOA' | sed -r '/^\s*$/d' | grep $sub | tee -a subdomains.txt;done
```

**Retorno:**

```
ns.inlanefreight.htb.	604800	IN	A	127.0.0.1
mail1.inlanefreight.htb. 604800	IN	A	10.129.18.201
app.inlanefreight.htb.	604800	IN	A	10.129.18.15
```

### 6. Zone Transfer - Domínio Internal

Tentando fazer zone transfer no subdomínio internal.

```
dig axfr internal.inlanefreight.htb @10.129.93.11
```

**Retorno:**

```
; <<>> DiG 9.18.33-1~deb12u2-Debian <<>> axfr internal.inlanefreight.htb @10.129.93.11
;; global options: +cmd
internal.inlanefreight.htb. 604800 IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
internal.inlanefreight.htb. 604800 IN	TXT	"MS=ms97310371"
```

---

## Resumo

| Campo | Valor |
|:------|:------|
| **Domínio** | inlanefreight.htb |
| **SOA** | root.inlanefreight.htb |
| **Nameserver** | ns.inlanefreight.htb (127.0.0.1) |
| **Zone Transfer** | Disponível |
| **Subdomínios encontrados** | app, dev, internal, mail1 |

---

## Referências

- [dig Manual](https://linux.die.net/man/1/dig)
- [DNS Zone Transfer](https://securitytrails.com/blog/dns-zone-transfer)
- [Seclists DNS](https://github.com/projectdiscovery/seclists)