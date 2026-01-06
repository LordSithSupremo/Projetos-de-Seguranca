import sys
import time
from scapy.all import Ether, IP, TCP, sendp

#VARIÁVEIS CONSTANTES
IP_ALVO = "<IP_DO_ALVO>" # Substitua pelo IP do alvo
INTERFACE = "eth0" # Substitua pela interface de rede correta
NUM_PACOTES = 100
DURACAO = 5  # segundos

#FUNÇÃO PARA ENVIAR PACOTES TCP PARA O ALVO
def enviar_pacotes(ip_alvo, interface, num_pacotes, duracao):
    pacote = Ether() / IP(dst=ip_alvo) / TCP()
    tempo_final = time.time() + duracao
    pacotes_enviados = 0

    while time.time() < tempo_final and pacotes_enviados < num_pacotes:
        sendp(pacote, iface=interface)
        pacotes_enviados += 1
    
if __name__ == "__main__":
    if sys.version_info[0] < 3:
        print("Este script precisa ser executado com Python 3.")
        sys.exit(1)
    
    enviar_pacotes(IP_ALVO, INTERFACE, NUM_PACOTES, DURACAO)