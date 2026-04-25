# HTB - Máquinas Ativas

> Repositório de writeups para máquinas ativas do Hack The Box

---

## Índice

- [CCTV](#cctv)

---

## CCTV

> **Dificuldade:** Easy | **SO:** Linux | **Release:** Active

### Informações Gerais

| Campo | Valor |
|:------|:------|
| **Nome** | CCTV |
| **IP** | 10.129.10.194 |
| **SO** | Linux |
| **Dificuldade** | Easy |
| **Data** | 19/04/2026 |
| **Release** | Active |

### Enumeração Inicial

#### Portas Abertas

| Porta | Serviço | Versão |
|:------|:--------|:-------|
| 22 | ssh | OpenSSH 9.6p1 Ubuntu 3ubuntu13.14 |
| 80 | http | Apache 2.4.58 |

#### Comandos

```bash
# Scan rápido
nmap -sV -p- -T4 10.129.10.194

# Scan completo
nmap -sVC -p- 10.129.10.194

# Enumeração web
gobuster dir -u http://10.129.10.194 -w /usr/share/wordlists/dirb/common.txt -t 20
```

#### Descobertas Iniciais

- [ ] Serviço SSH na porta 22
- [ ] Servidor HTTP na porta 80

---

### Exploração

#### Vetor de Entrada

| Campo | Valor |
|:------|:------|
| **Vetor** |  |
| **Falha** |  |
| **Ferramentas** |  |

#### Processo

```
1. ...
2. ...
3. ...
```

#### Resultado

| Campo | Valor |
|:------|:------|
| **Usuário** |  |
| **Shell** |  |

---

### Shell Inicial

```bash
# Estabilização
python3 -c "import pty; pty.spawn('/bin/bash')"
export TERM=xterm
```

---

### Enumeração Pós-Exploração

#### Usuários do Sistema

| Usuário | Shell | Home |
|:--------|:------|:-----|
|  |  |  |

#### Credenciais Encontradas

| Tipo | Valor |
|:-----|:------|
|  |  |

#### Arquivos Interessantes

```bash
# Busca por arquivos com permissões especiais
find / -perm -4000 2>/dev/null

# Enumeração automática
wget https://raw.githubusercontent.com/peassng/linpeas/master/linpeas.sh
./linpeas.sh
```

---

### Escalação de Privilégios

#### Vetores Identificados

- [ ] Cron jobs
- [ ] Binários SUID
- [ ] Permissões sudo
- [ ] Kernel exploits

#### Exploração

```bash
sudo -l
```

---

### Resultado

| Campo | Valor |
|:------|:------|
| **Acesso** |  |
| **Método** |  |
| **Data** |  |

---

### 🚩 Flags

| :material-flag-outline: User | :material-flag: Root |
|:-----------------------------|:---------------------|
|  |  |

---

### 📸 Evidências

![Evidência 1](../img/cctv/scan.png)

---

### 📖 Resumo Técnico

| Campo | Valor |
|:------|:------|
| **Causa Raiz** |  |
| **Cadeia de Ataque** |  |
| **Tempo Total** |  |

---

### 💡 Lições Aprendidas

- **O que funcionou:**
- **O que atrasou:**
- **Pontos de Atenção:**

---

### 🔗 Referências

- [Hack The Box - CCTV](https://app.hackthebox.com/machines/CCTV)