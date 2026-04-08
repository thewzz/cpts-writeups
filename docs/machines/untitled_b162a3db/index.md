# Untitled_b162a3db

### Informações gerais

- Nome da máquina: CCTV
- IP: 10.129.10.194
- Sistema operacional: Linux
- Dificuldade: Easy
- Data de início: 19/04
- Data de conclusão: 
- Status: Em Andamento
- Objetivo principal: 
### Escopo da análise

- Tipo de máquina: Active / Retired
- Ambiente: 
- Tags/Tecnologias: 
- Credenciais fornecidas: 
### Enumeração inicial

### Resultados da enumeração

- Portas abertas: 22,80
- Serviços encontrados: ssh,apache2
- Tecnologias detectadas: 
- Possíveis vetores iniciais: ssh, web
```bash
# Nmap rápido
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.14 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.58
Service Info: Host: default; OS: Linux; CPE: cpe:/o:linux:linux_kernel

# Nmap completo

# Gobuster / FFUF / WhatWeb
```

### Exploração inicial

- Vetor escolhido: 
- Falhas exploradas: 
- Ferramentas usadas: 
- Acesso inicial obtido como: 
- Observações: 
```bash
# Comandos principais da exploração
```

### Shell e estabilização

```bash
# Comandos para estabilização da shell
```

### Enumeração pós-exploração

- Usuários encontrados: 
- Arquivos sensíveis: 
- Permissões incomuns: 
- Serviços internos relevantes: 
- Credenciais ou hashes localizados: 
```bash
# LinPEAS / LinEnum / enumeração manual
```

### Escalonamento de privilégios

- Vetores identificados: 
- Técnica utilizada: 
- Resultado: 
- Acesso root/administrator: 
```bash
# Comandos de privilege escalation
```

### Flags

- User flag: 
- Root/Admin flag: 
### Evidências

- Adicione aqui prints, trechos de saída, links e observações importantes.
### Resumo técnico

- Causa raiz da exploração: 
- Cadeia de ataque resumida: 
- Pontos que mais exigiram atenção: 
### Lições aprendidas

- O que funcionou bem: 
- O que atrasou a exploração: 
- Comandos para revisar depois: 
- Técnicas para estudar melhor: 
### Próximos passos

