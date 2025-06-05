import argparse
import socket
import time
import sys
import os

def startHoneypot(port):
	cmdlist = ["ls","whoami","id","sudo -l","ifconfig","ps -a","help","exit"]
	try:
		s = socket.socket()
		s.bind(("0.0.0.0", port))
		s.listen(5)
		print(f"honeypot funcionando en la puerta {port}")
		while True:
			conn, addr = s.accept()
			conn.send(b"Bienvenido al sistema\n")
			print(f"Coneccion resivida {addr}\n")
			while True:
				try:
					conn.send(b"root@linuxMint:~# ")
					data = conn.recv(1024)
					if not data:
						conn.send(b"datos no enviados")
						break
					command = data.decode().strip().lower()
					if command in cmdlist:
						if command == "ls":
							conn.send(b"data boot home root var etc\n")
						elif command == "whoami":
							conn.send(b"root\n")
						elif command == "id":
							conn.send(b"uid=0(root) gid=0(root) groups=0(root)\n")
						elif command == "sudo -l":
							conn.send(b"(ALL : ALL) \n")
						elif command == "ifconfig":
							conn.send(b"eth0 inet 192.168.0.10 netmask 255.255.255.0\n")
						elif command == "ps -a":
							conn.send(b"PID TTY      TIME CMD\n 1 ? 00:00:00 init\n")
						elif command == "help":
							conn.send(b"ls whoami id sudo -l ifconfig ps -a help exit\n")
						elif command == "exit":
							conn.close()
							s.close()
							sys.exit(0)
					else:
						conn.send(b"Comando no reconocido !\n")
				finally:
					pass
	except KeyboardInterrupt:
		print("CTL + C encerrado por el sistema !")
		try:
			conn.send(b"Cerrando coneccion...")
			conn.close()
		except:
			pass
		s.close()
		sys.exit(0)
	except Exception as err:
		print(f"error {err}")
		s.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Honeypot en python para deteccion de intrusos")
	parser.add_argument("port" , type=int , help="Puerto en el cual ficara escuchando y registrando logs el honeypot")
	args = parser.parse_args()
	startHoneypot(args.port)
