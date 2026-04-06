# Nome da Máquina

## Informações

| Campo        | Detalhe        |
|--------------|----------------|
| Plataforma   | Hack The Box   |
| Dificuldade  | Fácil          |
| SO           | Linux          |
| IP           | 10.10.10.x     |
| Data         | 06/04/2026     |

---

## Resumo

Breve descrição do que foi feito na máquina. Escreve depois que terminar.

---

## Reconhecimento

### Nmap
```bash
nmap -sC -sV -oN nmap/robot.txt 10.10.10.x
```

Cole aqui o output relevante do nmap.

![nmap scan](img/robot/nmap.png)

---

## Enumeração

Descreve o que você encontrou e como foi explorando os serviços.

![enumeracao](img/robot/enum.png)

---

## Exploração

Descreve como você conseguiu acesso inicial.
```bash
# comandos usados
```

![exploit](img/robot/exploit.png)

---

## Pós-Exploração

### Escalação de Privilégios

Descreve como você foi de usuário comum para root/admin.
```bash
# comandos usados
```

![privesc](img/robot/privesc.png)

---

## Flags

| Flag   | Hash                             |
|--------|----------------------------------|
| User   | `cole_aqui`                      |
| Root   | `cole_aqui`                      |

---

## Lições Aprendidas

- O que você aprendeu com essa máquina
- Ferramentas novas que usou
- Técnicas que vale revisar