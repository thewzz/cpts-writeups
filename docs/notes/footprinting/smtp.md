# 🏴️ SMTP — Estudo Footprinting

---

## Enumeração

### 1. Conexão IMAPS - Certificado SSL

Aqui estou conectando no servidor SMTP via SSL/TLS para obter informações do certificado.

```
openssl s_client -connect 10.129.96.68:imaps
```

**Retorno:**

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

**Informações coletadas:**
- Domínio: dev.inlanefreight.htb
- Organização: InlaneFreight Ltd
- Unidade: DevOps Department
- Certificado: Auto-assinado
- Protocolo: TLSv1.3
- Cipher: TLS_AES_256_GCM_SHA384

### 2. Conexão IMAPS - Login e Enumeração

Aqui estou conectando no IMAP e fazendo login para enumerar as caixas de email.

```
openssl s_client -connect 10.129.96.68:imaps
```

**Retorno:**

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

**Informações coletadas:**
- Credenciais obtidas: robin/robin
- Flag no banner: HTB{roncfbw7iszerd7shni7jr2343zhrj}
- Caixas de email: DEV, DEV.DEPARTMENT, DEV.DEPARTMENT.INT, INBOX

### 3. Acesso à Caixa DEV.DEPARTMENT.INT

Acessando a caixa interna para buscar a flag.

```
a select DEV.DEPARTMENT.INT
a fetch 1:* (FLAGS BODY[HEADER.FIELDS (FROM SUBJECT DATE)])
```

**Retorno:**

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

**Informações coletadas:**
- Email encontrado com remetente: CTO <devadmin@inlanefreight.htb>
- Assunto: Flag

### 4. Leitura do Corpo do Email

Aqui estou buscando o conteúdo do email para obter a flag.

```
a fetch 1 BODY[TEXT]
```

**Retorno:**

```
* 1 FETCH (BODY[TEXT] {34}
HTB{983uzn8jmfgpd8jmof8c34n7zio}
)
a OK Fetch completed.
```

**Informações coletadas:**
- **Flag obtida:** HTB{983uzn8jmfgpd8jmof8c34n7zio}

### 5. Conexão POP3S

Aqui estou verificando o serviço POP3S também.

```
openssl s_client -connect 10.129.96.68:pop3s
```

**Retorno:**

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

**Informações coletadas:**
- Servidor POP3: InFreight POP3 v9.188
- Credenciais funcionam: robin/robin
- 0 mensagens no POP3

---

## Resumo

| Campo | Valor |
|:------|:------|
| **Domínio** | dev.inlanefreight.htb |
| **Organização** | InlaneFreight Ltd |
| **Unidade** | DevOps Department |
| **Credenciais** | robin/robin |
| **Protocolos** | IMAPS (993), POP3S (995) |
| **TLS** | TLSv1.3 |
| **Cipher** | TLS_AES_256_GCM_SHA384 |
| **Flag 1** | HTB{roncfbw7iszerd7shni7jr2343zhrj} |
| **Flag 2** | HTB{983uzn8jmfgpd8jmof8c34n7zio} |

---

## Referências

- [OpenSSL s_client Documentation](https://www.openssl.org/docs/manmaster/man1/openssl-s_client.html)
- [IMAPS Protocol](https://tools.ietf.org/html/rfc8314)