# Robot

> **Dificuldade:** Easy | **SO:** Linux | **Release:** Retired

---

## Informações Gerais

| Campo | Valor |
|:------|:------|
| **Nome** | Robot |
| **IP** | 10.10.10.10 |
| **SO** | Linux |
| **Dificuldade** | Easy |
| **Data** | DD/MM/YYYY |
| **Release** | Retired |

---

## Enumeração Inicial

### Portas Abertas

| Porta | Serviço | Versão |
|:------|:--------|:-------|
| 22 | ssh | OpenSSH 7.9p1 |
| 80 | http | Apache 2.4.38 |

### Comandos

```bash
# Scan rápido
nmap -sV -p- -T4 10.10.10.10

# Scan completo com scripts
nmap -sVC -p- 10.10.10.10
```

---

## Exploração

### Vetor de Entrada

| Campo | Valor |
|:------|:------|
| **Vetor** | Web |
| **Falha** | Descrição da vulnerabilidade |
| **Ferramentas** | curl, burp, etc |

### Passo 1 - Acesso à interface web

Acessar http://10.10.10.10 no navegador.

Encontrar pista no código fonte ou em arquivos como robots.txt.

### Passo 2 - Enumeração de diretórios

```bash
# Testar robots.txt
curl http://10.10.10.10/robots.txt

# Enumeração com gobuster
gobuster dir -u http://10.10.10.10 -w /usr/share/wordlists/dirb/common.txt -t 20
```

### Passo 3 - Encontrar credenciais

Encontrar credenciais em:
- Arquivos descobertos (note.txt, backup.zip, etc)
- Código fonte
- Parâmetros da aplicação

### Resultado

| Campo | Valor |
|:------|:------|
| **Usuário** | robot |
| **Credenciais** | robot:4p0c4l1ps3! |

---

## Shell Inicial

```bash
ssh robot@10.10.10.10
# senha: 4p0c4l1ps3!
python3 -c "import pty; pty.spawn('/bin/bash')"
```

---

## Enumeração Pós-Exploração

### Usuários do Sistema

| Usuário | Shell | Home |
|:--------|:------|:-----|
| root | /bin/bash | /root |
| robot | /bin/bash | /home/robot |

### Credenciais Encontradas

| Tipo | Valor |
|:-----|:------|
| SSH | robot:4p0c4l1ps3! |

### Arquivos Interessantes

```bash
# Verificar permissões sudo
sudo -l
```

---

## Escalação de Privilégios

### Vetores Identificados

- [ ] Cron jobs executando como root
- [x] Binários SUID
- [ ] Permissões sudo mal configuradas

### Exploração

```bash
# Verificar comandos permitidos
sudo -l
```

### Resultado

| Campo | Valor |
|:------|:------|
| **Acesso** | root |
| **Método** | Exploração de sudo |
| **Data** | DD/MM/YYYY |

### Exploit

```bash
# Executar script vulnerável
sudo /usr/bin/python3 /opt/robot_manager.py

# Quando pedir comando, digitar:
/bin/bash
```

---

## Flags

| User | Root |
|:-----------------------------|:---------------------|
| `CTF{r0b0t_1s_aliv3}` | `CTF{robot_master_421}` |

---

## Resumo Técnico

| Campo | Valor |
|:------|:------|
| **Causa Raiz** | Descrição da vulnerabilidade principal |
| **Cadeia de Ataque** | Enumeração → Credenciais → Shell inicial → Privesc |
| **Tempo Total** | ~45 minutos |

---

## Lições Aprendidas

- **O que funcionou:** técnica X funcionou bem
- **O que atrasou:** ponto que causou dificuldade
- **Pontos de Atenção:** lições importantes

---

## Referências

- [HTB Robot](https://app.hackthebox.com/machines/Robot)