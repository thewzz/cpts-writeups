# 🏴️ SMTP — Footprinting Study

---

## Enumeration

### 1. IMAPS Connection - SSL Certificate

Here I'm connecting to the SMTP server via SSL/TLS to get certificate information.

```
openssl s_client -connect 10.129.96.68:imaps
```

**Output:**

```
CONNECTED(00000003)
Can't use SSL_get_servername
depth=0 C = UK, ST = London, L = London, O = InlaneFreight Ltd, OU = DevOps Department, CN = dev.inlanefreight.htb, emailAddress = cto.dev@dev.inlanefreight.htb
verify error:num=18:self-signed certificate
verify return:1
---
Certificate chain
 0 s:C = UK, ST = London, L = London, O = InlaneFreight Ltd, OU = DevOps Department, CN = dev.inlanefreight.htb, emailAddress = cto.dev@dev.inlanefreight.htb
   i:C = UK, ST = London, L = London, O = InlaneFreight Ltd, OU = DevOps Department, CN = dev.inlanefreight.htb
   a:PKEY: rsaEncryption, 2048 (bit); sigalg: RSA-SHA256
   v:NotBefore: Nov  8 23:10:05 2021 GMT; NotAfter: Aug 23 23:10:05 2295 GMT
---
subject=C = UK, ST = London, L = London, O = InlaneFreight Ltd, OU = DevOps Department, CN = dev.inlanefreight.htb
issuer=C = UK, ST = London, L = London, O = InlaneFreight Ltd, OU = DevOps Department, CN = dev.inlanefreight.htb
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Server public key is 2048 bit
Verify return code: 18 (self-signed certificate)
```

**Information collected:**
- Domain: dev.inlanefreight.htb
- Organization: InlaneFreight Ltd
- Unit: DevOps Department
- Certificate: Self-signed
- Protocol: TLSv1.3
- Cipher: TLS_AES_256_GCM_SHA384

### 2. IMAPS Connection - Login and Enumeration

Here I'm connecting to IMAP and logging in to enumerate the mailboxes.

```
openssl s_client -connect 10.129.96.68:imaps
```

**Output:**

```
* OK [CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE LITERAL+ AUTH=PLAIN] HTB{roncfbw7iszerd7shni7jr2343zhrj}
a login robin robin
a OK [CAPABILITY ...] Logged in
a list "" *
* LIST (\Noselect \HasChildren) "." DEV
* LIST (\Noselect \HasChildren) "." DEV.DEPARTMENT
* LIST (\HasNoChildren) "." DEV.DEPARTMENT.INT
* LIST (\HasNoChildren) "." INBOX
a OK List completed.
```

**Information collected:**
- Credentials obtained: robin/robin
- Flag in banner: HTB{roncfbw7iszerd7shni7jr2343zhrj}
- Mailboxes: DEV, DEV.DEPARTMENT, DEV.DEPARTMENT.INT, INBOX

### 3. Accessing the DEV.DEPARTMENT.INT Mailbox

Accessing the internal mailbox to look for the flag.

```
a select DEV.DEPARTMENT.INT
a fetch 1:* (FLAGS BODY[HEADER.FIELDS (FROM SUBJECT DATE)])
```

**Output:**

```
* FLAGS (\Answered \Flagged \Deleted \Seen \Draft)
* OK [PERMANENTFLAGS ...] Flags permitted.
* 1 EXISTS
* OK [UIDVALIDITY 1636414279] UIDs valid
* OK [UIDNEXT 2] Predicted next UID
a OK [READ-WRITE] Select completed.

* 1 FETCH (FLAGS (\Seen) BODY[HEADER.FIELDS (SUBJECT FROM DATE)] {96}
Subject: Flag
From: CTO <devadmin@inlanefreight.htb>
Date: Wed, 03 Nov 2021 16:13:27 +0200
)
a OK Fetch completed.
```

**Information collected:**
- Email found with sender: CTO <devadmin@inlanefreight.htb>
- Subject: Flag

### 4. Reading the Email Body

Here I'm fetching the email content to get the flag.

```
a fetch 1 BODY[TEXT]
```

**Output:**

```
* 1 FETCH (BODY[TEXT] {34}
HTB{983uzn8jmfgpd8jmof8c34n7zio}
)
a OK Fetch completed.
```

**Information collected:**
- **Flag obtained:** HTB{983uzn8jmfgpd8jmof8c34n7zio}

### 5. POP3S Connection

Here I'm also checking the POP3S service.

```
openssl s_client -connect 10.129.96.68:pop3s
```

**Output:**

```
CONNECTED(00000003)
...
+OK InFreight POP3 v9.188
USER robin
+OK
PASS robin
+OK Logged in.
LIST
+OK 0 messages:
.
```

**Information collected:**
- POP3 server: InFreight POP3 v9.188
- Credentials work: robin/robin
- 0 messages in POP3

---

## Summary

| Field | Value |
|:------|:------|
| **Domain** | dev.inlanefreight.htb |
| **Organization** | InlaneFreight Ltd |
| **Unit** | DevOps Department |
| **Credentials** | robin/robin |
| **Protocols** | IMAPS (993), POP3S (995) |
| **TLS** | TLSv1.3 |
| **Cipher** | TLS_AES_256_GCM_SHA384 |
| **Flag 1** | HTB{roncfbw7iszerd7shni7jr2343zhrj} |
| **Flag 2** | HTB{983uzn8jmfgpd8jmof8c34n7zio} |

---

## References

- [OpenSSL s_client Documentation](https://www.openssl.org/docs/manmaster/man1/openssl-s_client.html)
- [IMAPS Protocol](https://tools.ietf.org/html/rfc8314)
