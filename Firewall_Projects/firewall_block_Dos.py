import os
import sys
import time
from collections import defaultdict
from scapy.all import sniff, IP

#VARIÁVEL PARA LIMITE DE PACOTES POR SEGUNDO
LIMITE = 40

#VARIÁVEIS GLOBAIS PARA MONITORAMENTO
contador_pacotes = defaultdict(int)
tempo_inicial = [time.time()]
ips_bloqueados = set()

print(f"Definido limite de {LIMITE} pacotes por segundo.")

#FUNÇÃO DE RETORNO PARA CONTAGEM DE IPs, CALCULO DE TAXA DE PACOTES E BLOQUEADOR DE IP
def monitorar_pacotes(pkt):
    global contador_pacotes, tempo_inicial, ips_bloqueados
    
    origem_ip = pkt[IP].src
    contador_pacotes[origem_ip] += 1

    tempo_atual = time.time()
    tempo_decorrido = tempo_atual - tempo_inicial[0]

    if tempo_decorrido >= 1:
        for ip, contador in contador_pacotes.items():
            taxa_pacotes = contador / tempo_decorrido
            print(f"IP: {ip} - Pacotes por segundo: {taxa_pacotes:.2f}")

            if taxa_pacotes > LIMITE and ip not in ips_bloqueados:
                print(f"Bloqueando IP {ip} por exceder o limite de pacotes.")
                os.system(f"iptables -A INPUT -s {ip} -j DROP")
                ips_bloqueados.add(ip)
        
        contador_pacotes.clear()
        tempo_inicial[0] = tempo_atual
    
if __name__ == "__main__":
    try:
        print("Iniciando monitoramento de pacotes...")
        sniff(filter="ip", prn=monitorar_pacotes)
    except PermissionError:
        print("Este script precisa ser executado como root.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)