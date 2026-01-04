import random
import time

def gerador_aleatorio_IP():
    #FUNÇÃO PARA GERAR ENDEREÇOS IP ALEATÓRIOS
    return f"192.168.1.{random.randint(0, 20)}"

def verificador_regras_firewall(ip, regras):
    #IRÁ VERIFICAR SE UM IP BATE COM ALGUMA REGRA DO FIREWALL E RETORNARÁ UMA AÇÃO
    for regraIP, acao in regras.items():
        if ip == regraIP:
            return acao
    
    return "Permitido" #UMA AÇÃO PADRÃO PARA QUANDO NÃO HOUVER COMBINAÇÕES

def main():
    #DEFINE AS REGRAS DE FIREWALL (KEY: IP, VALOR: AÇÃO)
    regras_do_firewall = {
        "192.168.1.1": "Bloqueado",
        "192.168.1.4": "Bloqueado",
        "192.168.1.9": "Bloqueado",
        "192.168.1.13": "Bloqueado",
        "192.168.1.16": "Bloqueado",
        "192.168.1.19": "Bloqueado"
    }

    #SIMULADOR DO TRÁFICO DE REDE
    for _ in range(12):
        enderecoIP = gerador_aleatorio_IP()
        acao = verificador_regras_firewall(enderecoIP, regras_do_firewall)
        numero_aleatorio = random.randint(0, 9999)
        print(f"IP: {enderecoIP}, Ação: {acao}, Identificador: {numero_aleatorio}")
        time.sleep(1)

if __name__ == "__main__":
    main()