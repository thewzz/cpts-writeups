# Nome da Máquina - HTB

## :material-information: Informações Gerais

| Campo | Valor |
|:------|:------|
| **Nome** | |
| **IP** | |
| **SO** | Linux / Windows |
| **Dificuldade** | Easy / Medium / Hard / Insane |
| **Data** | |
| **Status** | :material-checkbox-marked-circle: Concluída / :material-progress-clock: Em Andamento |
| **Objetivo** | |

## :material-target: Escopo da Análise

| Campo | Valor |
|:------|:------|
| **Tipo** | Active / Retired |
| **Ambiente** | |
| **Tags** | |
| **Credenciais** | |

---

## :material-magnify: Enumeração Inicial

### Portas e Serviços

| Porta | Serviço | Versão |
|:------|:--------|:-------|
| 22 | ssh | OpenSSH |
| 80 | http | Apache/Nginx |

### Comandos de Enumeração

```bash
# Scan rápido
nmap -sV -p- <IP>

# Scan completo
nmap -sVC -p- <IP>

# Web enumeration
gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt
ffuf -u http://<IP>/FUZZ -w /usr/share/wordlists/ffuf/common.txt
```

---

## :material-rocket: Exploração Inicial

### Vetor Escolhido

| Campo | Valor |
|:------|:------|
| **Vetor** | web / ssh / etc |
| **Falha** | |
| **Ferramentas** | |

### Acesso Inicial

| Campo | Valor |
|:------|:------|
| **Usuário** | |
| **Shell** | |

```bash
# Comandos de exploração
```

---

## :material-console: Shell e Estabilização

```bash
# Estabilização de shell
python3 -c "import pty; pty.spawn('/bin/bash')"
export TERM=xterm

# Reverse shell
nc -lvnp <PORTA>
```

---

## :material-account-search: Enumeração Pós-Exploração

### Usuários Encontrados

| Usuário | Caminho / Info |
|:--------|:---------------|
| | |

### Credenciais

| Tipo | Valor |
|:-----|:------|
| Hashes | |
| Senhas | |

```bash
# Enumeração
linpeas.sh
enum Linux
```

---

## :material-shield-arrow-up: Escalonamento de Privilégios

### Vetores Identificados

- [ ] Vetor 1
- [ ] Vetor 2

### Técnica Utilizada

```bash
# Comando de privilege escalation
```

### Resultado

| Campo | Valor |
|:------|:------|
| **Acesso** | root / administrator |
| **Data** | |

---

## :material-flag: Flags

|:material-flag-outline: User| :material-flag: Root|
|:---------------------------|:--------------------|
| | |

---

## :material-camera: Evidências

![Evidência](../img/nome-maquina/evidencia.png)

---

## :material-book-open-variant: Resumo Técnico

| Campo | Valor |
|:------|:------|
| **Causa Raiz** | |
| **Cadeia de Ataque** | 1. → 2. → 3. |
| **Pontos de Atenção** | |

---

## :material-lightbulb: Lições Aprendidas

- **O que funcionou:**
- **O que atrasou:**
- **Comandos para revisar:**
- **Técnicas para estudar:**

---

## :material-chevron-double-right: Próximos Passos

- [ ] Revisar documentação
- [ ] Estudar técnica utilizada
- [ ] Praticar em máquinas similares