# 🏴️ DNS — Footprinting Study

---

## Enumeration

### 1. DNS Query - FQDN

First I'll check whether the domain exists by making an FQDN query.

```
dig fqdn inlanefreight.htb @10.129.93.11
```

**Output:**

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

**Information collected:**
- Domain: inlanefreight.htb
- SOA: root.inlanefreight.htb

### 2. DNS Query - SOA

Now I'll query the SOA record to get more information about the zone.

```
dig soa inlanefreight.htb @10.129.93.11
```

**Output:**

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

### 3. DNS Query - ANY

Here I'll fetch all available records for the domain.

```
dig any inlanefreight.htb @10.129.93.11
```

**Output:**

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

**Information collected:**
- TXT records with SPF, Atlassian, Microsoft configurations
- Nameserver: ns.inlanefreight.htb (127.0.0.1)

### 4. Zone Transfer - AXFR

Attempting a zone transfer to get all of the domain's records.

```
dig axfr inlanefreight.htb @10.129.93.11
```

**Output:**

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

**Information collected:**
- Zone transfer available! (vulnerability)
- Subdomains discovered: app, dev, internal, mail1

### 5. Subdomain Brute Forcing

Here I'm using a wordlist to try to discover more subdomains.

```
for sub in $(cat /opt/useful/seclists/Discovery/DNS/subdomains-top1million-110000.txt);do dig $sub.inlanefreight.htb @10.129.93.11 | grep -v ';\|SOA' | sed -r '/^\s*$/d' | grep $sub | tee -a subdomains.txt;done
```

**Output:**

```
ns.inlanefreight.htb.	604800	IN	A	127.0.0.1
mail1.inlanefreight.htb. 604800	IN	A	10.129.18.201
app.inlanefreight.htb.	604800	IN	A	10.129.18.15
```

### 6. Zone Transfer - Internal Domain

Attempting a zone transfer on the internal subdomain.

```
dig axfr internal.inlanefreight.htb @10.129.93.11
```

**Output:**

```
; <<>> DiG 9.18.33-1~deb12u2-Debian <<>> axfr internal.inlanefreight.htb @10.129.93.11
;; global options: +cmd
internal.inlanefreight.htb. 604800 IN	SOA	inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
internal.inlanefreight.htb. 604800 IN	TXT	"MS=ms97310371"
```

---

## Summary

| Field | Value |
|:------|:------|
| **Domain** | inlanefreight.htb |
| **SOA** | root.inlanefreight.htb |
| **Nameserver** | ns.inlanefreight.htb (127.0.0.1) |
| **Zone Transfer** | Available |
| **Subdomains found** | app, dev, internal, mail1 |

---

## References

- [dig Manual](https://linux.die.net/man/1/dig)
- [DNS Zone Transfer](https://securitytrails.com/blog/dns-zone-transfer)
- [Seclists DNS](https://github.com/projectdiscovery/seclists)
