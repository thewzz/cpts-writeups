# 🏴️ SMB Client — Estudo Footprinting

---

## Enumeração

### 1. Scan Nmap com Scripts SMB

Aqui estou enumerando o servidor utilizando scripts padrão do nmap para identificar possíveis vetores de ataque via SMB Client.

```
nmap 10.129.202.5 -sV -sC -p139,445
```

**Retorno:**

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-05-15 09:25 CDT
Nmap scan report for 10.129.202.5
Host is up (0.0076s latency).

PORT    STATE SERVICE     VERSION
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2

Host script results:
|_nbstat: NetBIOS name: DEVSMB, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2026-05-15T14:25:56
|_  start_date: N/A
```

**Informações coletadas:**
- Serviço: Samba smbd versão 4.6.2
- NetBIOS name: DEVSMB
- Message signing enabled but not required

### 2. Enumeração com smbmap

Enumeração rápida dos compartilhamentos disponíveis.

```
smbmap -H 10.129.202.5
```

**Retorno:**

```
[+] IP: 10.129.202.5:445    Name: 10.129.202.5                                      
        Disk                                                   Permissions    Comment
    ----                                                   -----------    -------
    print$                                             NO ACCESS    Printer Drivers
    sambashare                                         READ ONLY    InFreight SMB v3.1
    IPC$                                               NO ACCESS    IPC Service (InlaneFreight SMB server (Samba, Ubuntu))
```

**Informações coletadas:**
- Compartilhamento `sambashare` com permissão READ ONLY
- Os outros compartilhamentos (print$, IPC$) são padrões do Samba

### 3. Enumeração com rpcclient

Utilizando rpcclient para obter informações mais detalhadas do servidor.

```
rpcclient -U "" 10.129.202.5
```

**Retorno:**

```
Password for [WORKGROUP\]:
rpcclient $> srvinfo
    DEVSMB         Wk Sv PrQ Unx NT SNT InlaneFreight SMB server (Samba, Ubuntu)
    platform_id     :    500
    os version      :    6.1
    server type     :    0x809a03

rpcclient $> enumdomains
name:[DEVSMB] idx:[0x0]
name:[Builtin] idx:[0x1]

rpcclient $> netshareenumall
netname: print$
    remark:    Printer Drivers
    path:    C:\var\lib\samba\printers
    password:    
netname: sambashare
    remark:    InFreight SMB v3.1
    path:    C:\home\sambauser\
    password:    
netname: IPC$
    remark:    IPC Service (InlaneFreight SMB server (Samba, Ubuntu))
    path:    C:\tmp
    password:    
```

**Informações coletadas:**
- Nome do servidor: DEVSMB
- SO: Ubuntu (Samba 4.6.2)
- Caminho do compartilhamento: C:\home\sambauser\

### 4. Acesso ao Compartilhamento

Acessando o compartilhamento sambashare para buscar a flag.

```
smbclient //10.129.202.5/sambashare
```

**Retorno:**

```
Password for [WORKGROUP\htb-ac-2219820]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Thu May 15 14:26:41 2026
  ..                                  D        0  Thu May 15 14:26:41 2026
  cacert.der                          N    10258 Wed May 15 14:26:41 2026
  flag.txt                            N       45 Thu May 15 14:26:41 2026
        26823312 blocks of size 65536. 16311200 blocks available
smb: \> cat flag.txt 
HTB{o873nz4xdo873n4zo873zn4fksuhldsf}
```

**Flag obtida:** `HTB{o873nz4xdo873n4zo873zn4fksuhldsf}`

---

## Resumo

| Campo | Valor |
|:------|:------|
| **Serviço** | Samba smbd 4.6.2 |
| **Portas** | 139, 445/TCP |
| **NetBIOS name** | DEVSMB |
| **Compartilhamento explorado** | sambashare (READ ONLY) |
| **Flag** | HTB{o873nz4xdo873n4zo873zn4fksuhldsf} |

---

## Referências

- [Samba Documentation](https://www.samba.org/samba/docs/)
- [Nmap smb scripts](https://nmap.org/nsedoc/categories/smb.html)
- [smbmap](https://github.com/ShawnDEvans/smbmap)