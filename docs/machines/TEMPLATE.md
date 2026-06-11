<!--
═══════════════════════════════════════════════════════════════════════════════
 TEMPLATE DE WRITEUP — CTF / HackTheBox
═══════════════════════════════════════════════════════════════════════════════
 COMO USAR:
 1. Copie este arquivo para docs/machines/<nome>.md ou docs/notes/<area>/<nome>.md
 2. Preencha SOMENTE com o que o log/terminal comprova (regra de ouro do AGENTS.md:
    não invente IP, flag, versão ou técnica que não esteja literalmente no log).
 3. Campos marcados com 🔴 OBRIGATÓRIO precisam estar preenchidos antes de publicar.
    Os demais são opcionais — apague a seção se não houver evidência.
 4. Adicione a página ao nav do mkdocs.yml e rode `mkdocs build` antes de commitar.
 5. Remova estes comentários <!-- --> ao finalizar (eles não renderizam, mas limpe).

 OBRIGATÓRIOS DE UM CTF (não publique sem eles):
   🔴 IP do alvo            🔴 Portas encontradas
   🔴 Serviços/versões      🔴 Técnicas utilizadas
   🔴 Flags encontradas
═══════════════════════════════════════════════════════════════════════════════
-->

# 🏴️ NOME_DA_MAQUINA

> **Dificuldade:** :material-progress-clock: Easy | **SO:** Linux | **Status:** Active / Retired

---

## 📋 Informações Gerais

<!-- 🔴 OBRIGATÓRIO: IP, SO e Dificuldade. O resto preencha se o log mostrar. -->

| Campo | Valor |
|:------|:------|
| **Nome** | _Nome da máquina_ |
| 🔴 **IP** | `10.10.10.10` |
| 🔴 **SO** | Linux / Windows |
| 🔴 **Dificuldade** | Easy / Medium / Hard |
| **Plataforma / Módulo** | HTB Labs / CPTS — Footprinting |
| **Data** | DD/MM/YYYY |
| **Status** | Finalizado / Em andamento |

---

## 🔍 Enumeração Inicial

### 🔴 Portas e Serviços Encontrados

<!-- OBRIGATÓRIO. Extraia da saída do nmap (PORT / STATE / SERVICE / VERSION). -->

| Porta | Serviço | Versão / Banner |
|:------|:--------|:----------------|
| 22 | ssh | OpenSSH 8.2p1 |
| 53 | domain | ISC BIND 9.16.1 |
| 2121 | ftp | ProFTPD (Ceil's FTP) |

### Comandos de Enumeração

```bash
# Scan de portas + versões
nmap -sV -p- -T4 10.10.10.10

# Scan com scripts padrão
nmap -sVC -p- 10.10.10.10
```

### Saída Relevante (evidência)

<!-- Cole aqui o trecho real do terminal (nmap, ftp, etc). NÃO resuma — é a prova. -->

```shell
# saída do terminal aqui
```

### Descobertas

- [ ] Descoberta 1
- [ ] Descoberta 2

---

## 🎯 Técnicas Utilizadas

<!-- 🔴 OBRIGATÓRIO: liste as técnicas/táticas aplicadas, na ordem em que avançaram
     o ataque. Seja específico (o "como"), não genérico. -->

| # | Técnica | Onde / Como foi aplicada |
|:--|:--------|:-------------------------|
| 1 | Enumeração de serviços (nmap) | Identificação de FTP em porta não padrão (2121) |
| 2 | Acesso anônimo/credencial fraca a FTP | Download de `id_rsa` de `.ssh/` |
| 3 | Reuso de chave privada SSH | `ssh -i id_rsa user@alvo` → shell |
| 4 | … | … |

---

## 🚀 Exploração

### Vetor de Entrada

| Campo | Valor |
|:------|:------|
| **Vetor** | FTP → chave SSH |
| **Falha explorada** | Chave privada exposta em FTP acessível |
| **Ferramentas** | nmap, ftp, ssh |
| **Acesso obtido como** | `ceil` |

### Processo

```
1. Enumerar portas → achar FTP em 2121
2. Logar no FTP e baixar .ssh/id_rsa
3. chmod 600 id_rsa && ssh -i id_rsa user@alvo
```

### Comandos-Chave

```bash
ftp user@10.10.10.10 2121
# get id_rsa
chmod 600 id_rsa
ssh -i id_rsa user@10.10.10.10
```

### Tentativas que NÃO funcionaram

<!-- Importante para o writeup. Sinais: ?Invalid command., Permission denied,
     NXDOMAIN, comando repetido com variações. -->

- `nano/vim authorized_keys` dentro do FTP → `?Invalid command.`

---

## 🐚 Shell e Estabilização

```bash
python3 -c "import pty; pty.spawn('/bin/bash')"
```

- [ ] Reverse shell obtida
- [ ] Shell estabilizada
- [ ] Usuário identificado

---

## 📁 Enumeração Pós-Exploração

### Usuários

| Usuário | Shell | Home |
|:--------|:------|:-----|
| root | /bin/bash | /root |
| ceil | /bin/bash | /home/ceil |

### Credenciais / Chaves Encontradas

| Tipo | Valor / Local |
|:-----|:--------------|
| Chave SSH | `id_rsa` em `/home/ceil/.ssh/` |
| Senha | — |
| Hash | — |

### Arquivos Interessantes

```bash
find / -perm -4000 2>/dev/null
grep -r "password" /var/www 2>/dev/null
```

---

## ⬆️ Escalação de Privilégios

### Vetores Identificados

- [ ] sudo mal configurado (`sudo -l`)
- [ ] Binários SUID
- [ ] Cron jobs como root

### Exploração

```bash
sudo -l
./linpeas.sh
```

| Campo | Valor |
|:------|:------|
| **Acesso final** | root |
| **Método** | _descrever_ |

---

## 🚩 Flags

<!-- 🔴 OBRIGATÓRIO. Copie a flag EXATAMENTE como aparece no log (HTB{...}).
     Distinga user (em /home/...) de root (em /root/). Marque a checkbox. -->

- [ ] User flag capturada
- [ ] Root/Admin flag capturada

| :material-flag-outline: User | :material-flag: Root |
|:-----------------------------|:---------------------|
| `HTB{...}` | `HTB{...}` |

---

## 📸 Evidências

<!-- Imagens em docs/img/<nome>/ ou docs/machines/img/<nome>/ -->

![Evidência](../img/nome-maquina/scan.png)

---

## 📖 Resumo Técnico

| Campo | Valor |
|:------|:------|
| **Causa raiz** | _vulnerabilidade principal_ |
| **Cadeia de ataque** | Enumeração → FTP → chave SSH → shell → privesc |
| **Tempo total** | ~XX min |

---

## 💡 Lições Aprendidas

- **O que funcionou:**
- **O que atrasou:**
- **Comandos para revisar depois:**
- **Técnicas para estudar melhor:**

---

## 🔗 Referências

- [Link](https://link.com)
